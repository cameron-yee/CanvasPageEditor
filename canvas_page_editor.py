import requests
from glob import glob
import json
import pprint
import re
import os
import argparse
import auth
from collections import OrderedDict
from colors import bcolors
from media_server_update import *

#TODO: Add variable types to improve readability using typing.py lib
#import typing

#CLI command definitions
def selectAction():
    parser = argparse.ArgumentParser(description='Pick action.')
    subparsers = parser.add_subparsers(help='sub-command help')

    #commands for updating entire course
    parser_uc = subparsers.add_parser('uc', help='Commands to use when updateCoursePages')
    parser_uc.add_argument('top_directory', help='Enter the directory that contains the html files, or subfolders that contain the html files', type=str)
    parser_uc.add_argument('cid', help='Enter course ID', nargs='?', default=None, type=str) #nargs allows default to work
    parser_uc.set_defaults(which='uc')

    #commands for updating individual course page
    parser_ind = subparsers.add_parser('ind', help='Commands to use when updateIndividualPage')
    #parser_ind.add_argument('-url','--page_url', action='store', help='Enter the last section of the url that the page is on', type=str)
    parser_ind.add_argument('file_path', help='Enter the path to file on your local device', type=str)
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
    
    args = parser.parse_args()
    return args


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
    return html_files


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
    info_lists = []
    directories = getHtmlFolders(top_directory)

    #if course_id is not None:
        #urls = getCoursePages(course_id, headers) #List of all urls of canvas pages in given course

        #Glob html will work different if html files are not stored in sub folders
    if not directories:
        html_files = globHtml(top_directory)
        #html_dict = storeHtmlData(html_files[0], urls) #globHtml returns list of lists with one list
    else:
        for i in range(len(directories)):
            html_info = globHtml(directories[i])
            info_lists.append(html_info[0])
        list_of_files = [x for x in info_lists if x != []]
        for ls in list_of_files:
            for f in ls:
                html_files.append(f)
    
    skipped = []
    count = 0
    for f in html_files:
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
def updateIndividualPage(course_id, headers, file_path):
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

    def update(page_url, course_id, html_content):
        url = url_base + course_id + '/pages/' + page_url
        data = [('wiki_page[body]', html_content),]
        status = checkPageExistsInCanvas(url)
        if status == 200:
            r = requests.put(url, headers=headers, data=data)
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


#Update course name
def updateCourseName(new_course_name, course_id, headers):
    url = url_base + course_id
    data = [('course[name]', new_course_name),]
    r = requests.put(url, headers=headers, data=data)


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


#Create a new page in a Canvas Course
def createNewPage(course_id, headers, page_name, file_path):
    url = url_base + course_id + '/pages'
    with open(file_path, 'r') as f:
        body = f.read()
        f.close()
    data = [('wiki_page[title]', page_name), ('wiki_page[body]', body),]
    r = requests.post(url, headers=headers, data=data)


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
       updateCoursePages(args.top_directory)
    if args.which == 'ind':
       course_id = args.cid
       #Always passing course_id even if None to avoid another if statement
       updateIndividualPage(course_id, headers, args.file_path)
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
