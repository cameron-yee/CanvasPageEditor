import requests
from glob import glob
import json
import pprint
import re
import os
import argparse
import auth
from collections import OrderedDict

#local file imports
from colors import bcolors
from media_server_update import *

#chrome imports
#from capichrome import browser, refreshPage, startChrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

#TODO: Add variable types to improve readability using typing.py lib
#import typing

#CLI command definitions
def selectAction():
    parser = argparse.ArgumentParser(description='Pick action.')
    subparsers = parser.add_subparsers(help='sub-command help')

    #commands for updating entire course
    parser_uc = subparsers.add_parser('uc', help='Commands to use when updateCoursePages')
    parser_uc.add_argument('-n','--name', help='Change course name', action='store', nargs='?', default=None)
    parser_uc.add_argument('-c','--code', help='Change course code', action='store', nargs='?', default=None)
    parser_uc.add_argument('top_directory', help='Enter the directory that contains the html files, or subfolders that contain the html files', nargs='?', default=None, type=str)
    parser_uc.add_argument('cid', help='Enter course ID', nargs='?', default=None, type=str) #nargs allows default to work
    parser_uc.set_defaults(which='uc')

    #commands for updating individual course page
    parser_ind = subparsers.add_parser('ind', help='Commands to use when updateIndividualPage')
    #parser_ind.add_argument('-url','--page_url', action='store', help='Enter the last section of the url that the page is on', type=str)
    parser_ind.add_argument('file_path', help='Enter the path to file on your local device', type=str)
    parser_ind.add_argument('-nn', '--newname', action='store', nargs='?', default=None)
    parser_ind.add_argument('cid', help="Enter course ID", nargs='?', default=None, type=str)
    parser_ind.set_defaults(which='ind')

    #commands for updating media server
    parser_static = subparsers.add_parser('static', help='Commands to use when pushing static files to media server')
    parser_static.add_argument('-c', '--css', action='count', help='Update css file on media server')
    parser_static.add_argument('-j', '--js', action='count', help='Update js file on media server')
    parser_static.add_argument('-ht', '--html', action='count', help='Update html menu on media server')
    parser_static.add_argument('-i','--img', action='store', help='Local image path to upload', type=str)
    parser_static.add_argument('course_prefix', help='Enter the prefix of the course', type=str)
    parser_static.add_argument('-sc', '--subcourse', action='store', help='Update css file on media server', type=str)
    parser_static.add_argument('-f','--folder', action='store', help='Folder to upload img to in AWS', type=str)
    parser_static.set_defaults(which='static')

    #commands for using with chrome reload
    parser_chrome = subparsers.add_parser('chrome', help='Commands to use when using capi with chromerefresh')
    parser_chrome.add_argument('watchpath', help="Path to watch for content changes", type=str)
    parser_chrome.set_defaults(which='chrome')
    
    args = parser.parse_args()
    return args


#Chrome functions EXPERIMENTAL
browser = None
chromeUp = False
def startChrome():
    global browser
    browser = webdriver.Chrome()
    browser.get('https://bscs.instructure.com/courses')
    email_input = browser.find_element_by_id('pseudonym_session_unique_id')
    email_input.send_keys(auth.email)
    password_input = browser.find_element_by_id('pseudonym_session_password')
    password_input.send_keys(auth.canvas_password + Keys.RETURN)
    chromeUp = True


def refreshPage(course_id, url):
    global browser
    browser.get('https://bscs.instructure.com/courses/{cid}/pages/{url}'.format(cid=course_id, url=url))


class MySyncHandler(FileSystemEventHandler):

    def on_modified(self, event):
        filename = event.src_path
        updateIndividualPage(None, headers, filename)


## main loop
def watch(watchpath):
    observer = Observer()
    observer.schedule(MySyncHandler(), watchpath, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
#END CHROME


#Returns list of sub direct subfolders from given directory
def getHtmlFolders(top_directory):
    final_directories = []
    raw_directories = [x for x in os.walk(top_directory)]
    processed_directories = raw_directories[0][1]

    for directory in processed_directories:
          final_directories.append('{}/{}'.format(top_directory, directory)) 

    final_directories.append(top_directory) #Allows for floating html files in top dir
    return final_directories

#Returns a list of all html file paths in a given folder
def globHtml(directory):
    html_files = []
    html_files.append(glob(directory + '{}'.format('/**/*.html'), recursive=True))
    return html_files[0]


#Gets every page in a course and appends the page url to a list
def getCoursePages(course_id, headers):
    # page = 1
    count = 0
    urls  = []
    isNext = True
    first = True
    url = url_base + course_id + '/pages?per_page=300&page=1&sort=title&order=asc'
    r = requests.get(url, headers=headers, timeout=20)

    try:
        while first:
            r = requests.get(r.links['current']['url'], headers=headers)
            # print(r.links['current']['url'])
            data = r.json()
            for page in data:
                urls.append(page['url'])
            first = False
        while isNext:
            r = requests.get(r.links['next']['url'], headers=headers)
            data = r.json()
            for page in data:
                urls.append(page['url'])
            count += 1
            # print(r.links['next']['url'])
    except KeyError:
        isNext = False

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(pages)
    return urls


def updateCoursePages(top_directory):
    html_files = []
    directories = getHtmlFolders(top_directory)

    for i in range(len(directories)):
        directory_html_files = globHtml(directories[i])
        for f in directory_html_files:
            if f not in html_files: html_files.append(f)

    skipped = []
    count = 0
    for f in sorted(html_files):
        success_status = updateIndividualPage(course_id, headers, f)
        count += success_status
        if success_status == 0: skipped.append(os.path.basename(f))

    print(bcolors.BOLD + 'Success!' + bcolors.ENDC) 
    if course_id is not None:
        urls = getCoursePages(course_id, headers) #List of all urls of canvas pages in given course
        print(bcolors.WARNING + '{0} pages updated out of {1} course pages'.format(count, len(urls)) + bcolors.ENDC)

    print(bcolors.WARNING + '{0} pages updated out of {1} given files'.format(count, len(html_files)) + bcolors.ENDC)
    print(bcolors.FAIL + 'Pages skipped: {}'.format(skipped) + bcolors.ENDC)


#Prints json object for individual page
def getPageInformation(course_id, page_url, headers):
    url = url_base + course_id + '/pages/' + page_url
    r = requests.get(url, headers=headers)
    r.json
    x = json.loads(r.text)
    print(json.dumps(x, sort_keys=True, indent=4))


#Updates html body content for given Canvas page and html file, for updating entire course
#Returns either 0 or 1 depending on if update was successful
def updateIndividualPage(course_id, headers, file_path, page_name=None):
    def getPageInfo():
        with open(file_path, 'r') as f:
            contents = f.read()
            patterns = ['<span url="([^\n]+)" courses="([^\n]+)"></span>', '<span url="([^\n]+)"></span>', '<span courses="([^\n]+)"></span>']
            for i in range(len(patterns)):
                m = re.search(patterns[i], contents)
                if m is not None:
                    return m.groups(), i, contents

        return None, None, contents
        #print('No variables provided in command or file for: {}'.format(file_path))

    def checkPageExistsInCanvas(url):
        r = requests.get(url, headers=headers)
        return r.status_code

    #TODO: This isn't working as expected
    success = True
    def fail():
        success = False

    #Updates page title
    def changePageName(old_page_url, course_id):
        url = url_base + course_id + '/pages/' + old_page_url
        name_data = [('wiki_page[title]', page_name),]
        r_name = requests.put(url, headers=headers, data=name_data)
        r_name_data = r_name.json()
        new_url = r_name_data['url']

        def updatePageUrl(new_url):
            page_info = getPageInfo()
            contents = page_info[2]
            old_url = page_info[0][0] if page_info[1] is not 2 else print(bcolors.FAIL + 'No URL provided in file.' + bcolors.ENDC)
            updated_url_tag = 'url="{}" courses="{}"'.format(new_url, page_info[0][1])
            updated_contents = re.sub('url="[^\n]+"', updated_url_tag, contents)
            with open(file_path, 'w') as f:
                f.write(updated_contents)
                f.close()
            print(bcolors.WARNING + 'Page name changed to {} for url: {} (OLD URL) in course {}\nWARNING: THE PAGE URL HAS CHANGED TO: {}'.format(page_url, old_url, course_id, new_url) + bcolors.ENDC) if r_name.status_code == 200 else print(bcolors.FAIL + 'Request Error: {}\nPage: {}'.format(r_name.status_code,page_url) + bcolors.ENDC)

        updatePageUrl(new_url)
        return new_url

    def update(page_url, course_id, html_content):
        page_url = changePageName(page_url, course_id) if page_name is not None else page_url
        url = url_base + course_id + '/pages/' + page_url
        data = [('wiki_page[body]', html_content),]
        status = checkPageExistsInCanvas(url)
        if status == 200:
            r = requests.put(url, headers=headers, data=data)
            if chromeUp:
                refreshPage(course_id, page_url)
            print(bcolors.OKBLUE + 'Updating: {} for course {}'.format(page_url, course_id) + bcolors.ENDC) if r.status_code == 200 else print(bcolors.FAIL + 'Request Error: {}\nPage: {}'.format(r.status_code,page_url) + bcolors.ENDC)
        else:
            #TODO: This isn't working
            print('Received {} response for {}'.format(status, page_url))
            success = False

    page_info = getPageInfo()
    if page_info[0] is not None:
        pattern_match_case = page_info[1]

    html_content = page_info[2]

    course_ids = []
    if course_id is None and page_info[0] is None:
        print('No course_id variable provided in file for {}'.format(os.path.basename(file_path)))
        return 0
    elif course_id is None:
        #TODO: Refactor this UUUUUUUUUUUUUgly code
        course_ids = page_info[0][1] if pattern_match_case == 0 else page_info[0][0] #Checks which regex case was hit in file
        course_ids = course_ids.split(',')
        course_ids = [item.replace(' ','') for item in course_ids] #So ' ' in list don't matter
    else:
        course_ids.append(course_id)

    #Checks our naming convention for url in file name
    def getPageUrlFromFile():
        m = re.search('\d+_([^/]+).html$',file_path)
        if m is not None:
            file_name = m.group(1)
            url = file_name.replace('_','-')
            return url

        return None

    #updates using url in file if no url is specified in CLI command
    if page_info[0] is not None:
        page_url = page_info[0][0] if pattern_match_case != 2 else getPageUrlFromFile() #Match is always 1st regex group
        for course in course_ids:
            str(course)
            update(page_url, course, html_content) if page_url is not None else fail()
    else:
        page_url = getPageUrlFromFile()
        for course in course_ids:
            str(course)
            update(page_url, course, html_content) if page_url is not None else fail()

    #Count of successes for updateCourse
    #UpdateIndividual must return 0, not fail function
    if success == False:
        print('Error uploading page: {}'.format(page_url))
        return 0

    return 1


#Create a new course in Canvas
def createNewCourse(course_name, headers):
    url = 'https://bscs.instructure.com/api/v1/accounts/1/courses'
    data = [('course[name]', course_name),]
    r = requests.post(url, headers=headers, data=data)


#uc argparser
#Update course name
def updateCourseName(new_course_name, course_id, headers):
    url = url_base + course_id
    r_old = requests.get(url, headers=headers)
    old_data = r_old.json()
    old_course_name = old_data['name']

    data_update = [('course[name]', new_course_name),]
    r_update = requests.put(url, headers=headers, data=data_update)

    print(bcolors.BOLD + 'Updated course name for course {}'.format(course_id) + bcolors.ENDC) 
    print(bcolors.WARNING + 'Old course name: {}'.format(old_course_name) + bcolors.ENDC) 
    print(bcolors.WARNING + 'New course name: {}'.format(new_course_name) + bcolors.ENDC) 


#uc argparser
#Update course code
def updateCourseCode(new_course_code, course_id, headers):
    url = url_base + course_id
    r_old = requests.get(url, headers=headers)
    old_data = r_old.json()
    old_course_code = old_data['course_code']

    data_update = [('course[course_code]', new_course_code),]
    r_update = requests.put(url, headers=headers, data=data_update)

    print(bcolors.BOLD + 'Updated course code for course {}'.format(course_id) + bcolors.ENDC) 
    print(bcolors.WARNING + 'Old course code: {}'.format(old_course_code) + bcolors.ENDC) 
    print(bcolors.WARNING + 'New course code: {}'.format(new_course_code) + bcolors.ENDC) 


#Create a new page in a Canvas Course
def updatePageName(course_id, headers, page_name, file_path):
    url = url_base + course_id + '/pages'

    r_old = requests.get(url, headers=headers)
    old_data = r_old.json()
    old_course_name = old_data['name']

    with open(file_path, 'r') as f:
        body = f.read()
        f.close()
    data = [('wiki_page[title]', page_name), ('wiki_page[body]', body),]
    r = requests.post(url, headers=headers, data=data)


#########################################################################################################################
#
########## END FUNCTIONAL FUNCTIONS, functions below may work, but have not been updated or optimized ###################
#
#########################################################################################################################


#Create a new module in a Canvas Course
def createNewModule(module_name, course_id, headers):
    url = url_base + course_id + '/modules'
    data = [('module[name]', module_name),]
    r = requests.post(url, headers=headers, data=data)


#Returns the id for the wanted module
def getModuleId(course_id, headers, module_name):
    url = url_base + course_id + '/modules'
    data = [('include[]', 'items'),]
    r = requests.get(url, headers=headers, data=data)
    data = r.json()
    for i in range(len(data)):
        if(data[i]['name'] == module_name):
            return str(data[i]['id'])
        else:
            return 'No Module Found'


#Create a new page within a Canvas course module
def createPageInModule(course_id, headers, page_name, module_name):
    module_id = getModuleId(course_id, headers, module_name)
    url = url_base + course_id + '/modules/' + module_id + '/items'
    page_url = page_name.lower()
    page_url = page_url.replace(' ', '-')
    data = [('module_item[type]', 'Page'),
            ('module_item[title]', page_name),
            ('module_item[page_url]', page_url)]
    r = requests.post(url, headers=headers, data=data)
    return page_url


#TODO: Using old version of updateIndividualPage
#Creates pages in Canvas course modulec and adds html content to each page
def createPagesAndAddContent(course_id, headers, page_titles, html_files, module_name):
    assert(len(page_titles) == len(html_files))
    for i in range(len(page_titles)):
        page_url = createPageInModule(course_id, headers, page_titles[i], module_name)
        updateIndividualPage(course_id, headers, page_url, html_files[i])


#TODO: Using old version of updateIndividualPage
#Creates pages in Canvas course and adds html content to each page
def createPagesAndAddContent(course_id, headers, page_titles, html_files):
    assert(len(page_titles) == len(html_files))
    for i in range(len(page_titles)):
        page_url = createPage(course_id, headers, page_titles[i])
        updateIndividualPage(course_id, headers, page_url, html_files[i])


##################################################################################################
#Logistics code below


#Gets token from hidden file so it will not show up on Git
def getAccessToken():
    token = auth.token
    return token


if __name__  == '__main__':
    args = selectAction()
    access_token = getAccessToken()
    headers = {"Authorization": "Bearer " + access_token}
    # course_id = '122'
    url_base = 'https://bscs.instructure.com/api/v1/courses/'

    if args.which == 'uc':
       course_id = args.cid
       if args.name is not None:
           course_id = args.top_directory #If args.name is given, top_directory argument will be the givin course id because only 2 arguments will be given
           updateCourseName(str(args.name), course_id, headers) 
       elif args.code is not None: 
           course_id = args.top_directory #If args.code is given, top_directory argument will be the givin course id because only 2 arguments will be given
           updateCourseCode(str(args.code), args.top_directory, headers) 
       else:
           updateCoursePages(args.top_directory)
    if args.which == 'ind':
       course_id = args.cid
       #Always passing course_id even if None to avoid another if statement
       updateIndividualPage(course_id, headers, args.file_path) if args.newname is None else updateIndividualPage(course_id, headers, args.file_path, args.newname)
    if args.which == 'static':
        course = args.course_prefix
        if args.css is not None:
            upload_css_aws(course, args.subcourse)
            upload_css_sftp(course, args.subcourse)
        if args.js is not None:
            upload_js_aws(course, args.subcourse)
            upload_js_sftp(course, args.subcourse)
        if args.html is not None:
            upload_html_aws(course, args.subcourse)
            upload_html_sftp(course, args.subcourse)
        if args.img is not None:
            upload_img_aws(args.img, course, args.folder, args.subcourse)
        if args.css is None and args.js is None and args.html is None and args.img is None:
            upload_all(course, args.subcourse)
            print('Updated {} static files'.format(course))
    if args.which == 'chrome':
        course_id = None

        startChrome()
        chromeUp = True
        watch(args.watchpath)

#Function specifically for MNSTL One Time Use
#def updatePageTitles(course_id, headers, pattern):
#    urls = getCoursePages(course_id, headers)
#    for url in urls:
#        m = re.search(pattern, url)
#        num = m.group(1)
#        re.sub(pattern, '{num}.', url)
#        print(page)
#        break
#
