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
    parser_uc.add_argument('cid', help='Enter course ID', default='', type=str)
    parser_uc.set_defaults(which='uc')

    #commands for updating individual course page
    parser_ind = subparsers.add_parser('ind', help='Commands to use when updateIndividualPage')
    parser_ind.add_argument('-url','--page_url', action='store', help='Enter the last section of the url that the page is on', type=str)
    parser_ind.add_argument('file_path', help='Enter the path to file on your local device', type=str)
    parser_ind.add_argument('cid', help="Enter course ID", default="", type=str)
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


# def ucArgs():
#     parser = argparse.ArgumentParser(description='Arguments required for updateCoursePages()')
#     parser.add_argument('top_directory', help="Enter the directory that contains the html files, or subfolders that contain the html files", type=str)
#     uc_args = parser.parse_args()
#     return uc_args
    

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

    # sorted_dict = OrderedDict(sorted(html_dict.items(), key=lambda t: t[0]))
    # for dictionary in sorted_dict:
    #     print(dictionary)

    # print(sorted_dict)
    # return all_files


#Gets html body content for each page in course
#List will be in the correct index order as html_files because both are lists and html_data is being appended in the same order as html_files
#TODO: I don't like that both html_files and html_data are lists.  It seems inefficient.  Combine into one Dict?
def getHtmlData(html_files):
    html_data = []
    for html_file in html_files:
        if html_file is not None:
            with open(html_file, 'r') as f:
                contents = f.read()
                m = re.search('<span url="([^\n]+)"></span>', contents)
                local_url_var = m.group(1) if m is not None else None
                html_data.append((contents, local_url_var)) #appends Type: tuple
                f.close()

    return html_data


#Returns a dictionary of all course pages sorted alphabetically with html file path and html content as values
def storeHtmlData(html_files, urls):
    html_data = getHtmlData(html_files) #Type List: [(html_content, file_url_variable)]
    html_dict = {}
    sorted_dict = {}
    unset = []
    errors = False

    for i in range(len(html_files)):
        key = re.search('\d+_([^/]+.html$)', html_files[i])
        #sets the file 'url' without the 00_ as the key
        #stores both the full html file and the html data from the file
        #key must be a valid url
        #TODO: 1st conditional supports our naming convention, but may be better to see if file name contains url anywhere in file name
        if key in urls:
            html_dict[str(key.group(1)).replace('_','-')] = html_files[i], html_data[i][0], html_data[i][1] #key = file path, html content, file url string variable
        elif html_data[i][1] is not None:
            key = (html_data[i][1])
            html_dict[key] = html_files[i], html_data[i][0], html_data[i][1]
        else:
            print(bcolors.FAIL + 'URL is not in file name and no URL is provided in file for {}'.format(html_files[i]) + bcolors.ENDC)

        #sorts dictionary alphabetically by key with lambda function for sort
        sorted_dict = OrderedDict(sorted(html_dict.items(), key=lambda t: t[1]))

    # assert(errors == False)
    return sorted_dict #TYPE: key: file path, html content


#Ensures that files are matched to urls, fails if file name is not a url in course
def matchFilesToUrls(urls,html_dict):
    matched_dict = {}
    skipped = urls #type: Array
    count = 0
    for html_dict_key, values in html_dict.items():
        mut_key = html_dict_key.replace('_','-')
        m = re.search('^[^/.]+', mut_key) #Is this regex necessary? if url = mut_key?
        for url in urls:
            if m is not None:
                if url == m.group(0):
                    matched_dict[count] = url, html_dict_key
                    skipped.remove(url)
                    count += 1
            elif values[2] == url:                          #If url variable in page is the same as Canvas page url
                matched_dict[count] = url, html_dict_key
                skipped.remove(url)
                count += 1 

    return matched_dict, skipped


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

    canvas_pages = getCoursePages(course_id, headers)
    urls = [] #List of all urls of canvas pages in given course
    for page_url in canvas_pages:
        urls.append(page_url)

    #Glob html will work different if html files are not stored in sub folders
    if not directories:
        html_files = globHtml(top_directory)
        html_dict = storeHtmlData(html_files[0], urls) #globHtml returns list of lists with one list
    else:
        for i in range(len(directories)):
            html_info = globHtml(directories[i])
            info_lists.append(html_info[0])
        list_of_files = [x for x in info_lists if x != []]
        for ls in list_of_files:
            for f in ls:
                html_files.append(f)
        html_dict = storeHtmlData(html_files, urls)

    #because Canvas sorts different than Python
    #sorted_urls = sorted(urls, key=lambda t: t[0])
    match = matchFilesToUrls(urls, html_dict)
    matched_dict = match[0]

#    try:
        #assert(len(urls) == len(html_dict))
    count = 0
    for key, values in matched_dict.items():
        url = matched_dict[count][0]
        path = html_dict[matched_dict[count][1]][0]
        content = html_dict[matched_dict[count][1]][1]
        updateIndividualPage(course_id, headers, path, url, content) 
        count += 1
    print(bcolors.BOLD + 'Success!' + bcolors.ENDC)
    print(bcolors.WARNING + '{0} pages updated out of {1}'.format(count, len(canvas_pages)) + bcolors.ENDC)
    print(bcolors.FAIL + 'Pages skipped: {}'.format(match[1]) + bcolors.ENDC)
#    except AssertionError:
#        count = 0
#        print(len(html_dict), len(urls))
#        for key, value in html_dict.items():
#            print(key, bcolors.WARNING + urls[count] + bcolors.ENDC)
#            count += 1


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


#DEPRECATED
#Updates html body content for each Canvas page in a given coures given the directory where the html files are stored
# def updateCoursePages(course_id, headers, html_files):
#     pages = getCoursePages(course_id, headers)
#     count = 0

#     assert(len(pages) == len(html_files))
#     for page_url in pages:
#         updateIndividualPage(course_id, headers, page_url, html_files[count])
#         count += 1


#Prints json object for individual page
def getPageInformation(course_id, page_url, headers):
    url = url_base + course_id + '/pages/' + page_url
    r = requests.get(url, headers=headers)
    r.json
    x = json.loads(r.text)
    print(json.dumps(x, sort_keys=True, indent=4))


#Updates html body content for given Canvas page and html file, for updating entire course
def updateIndividualPage(course_id, headers, file_path, page_url=None, html_content=None):
    #Gets url from span in page if exists
    def getUrlVar():
        with open(file_path, 'r') as f:
            contents = f.read()
            m = re.search('<span url="([^\n]+)"></span>', contents)
            if m is not None:
                page_url = m.group(1)
                return page_url
            else:
                return None

    def update(page_url):
        url = url_base + course_id + '/pages/' + page_url
        if html_content is not None:
            data = [('wiki_page[body]', html_content),]
            r = requests.put(url, headers=headers, data=data)
            print(bcolors.OKBLUE + 'Updating: {}'.format(page_url) + bcolors.ENDC) if r.status_code == 200 else print(bcolors.FAIL + 'Request Error: {}\nPage: {}'.format(r.status_code,page_url) + bcolors.ENDC)
        else:
            with open(file_path, 'r') as f:
                html = f.read()
            data = [('wiki_page[body]', html),]
            r = requests.put(url, headers=headers, data=data)
            f.close()

    #updates using url in file if no url is specified in CLI command
    if page_url is None:
        page_url = getUrlVar()
        update(page_url=page_url) if page_url is not None else print('No URL variable provided in file')
    else:
        update(page_url)


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
def createNewPage(course_id, headers, page_name, html_file):
    url = url_base + course_id + '/pages'
    with open(html_file, 'r') as f:
        body = f.read()
        f.close()
    data = [('wiki_page[title]', page_name), ('wiki_page[body]', body),]
    r = requests.post(url, headers=headers, data=data)


#Gets token from hidden file so it will not show up on Git
def getAccessToken():
    token = auth.token
    return token


#Creates pages in Canvas course modulec and adds html content to each page
def createPagesAndAddContent(course_id, headers, page_titles, html_files, module_name):
    assert(len(page_titles) == len(html_files))
    for i in range(len(page_titles)):
        page_url = createPageInModule(course_id, headers, page_titles[i], module_name)
        updateIndividualPage(course_id, headers, page_url, html_files[i])


#Creates pages in Canvas course and adds html content to each page
def createPagesAndAddContent(course_id, headers, page_titles, html_files):
    assert(len(page_titles) == len(html_files))
    for i in range(len(page_titles)):
        page_url = createPage(course_id, headers, page_titles[i])
        updateIndividualPage(course_id, headers, page_url, html_files[i])


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
       if args.page_url is not None:
           updateIndividualPage(course_id, headers, args.file_path, args.page_url)
       else:
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

    #update_all(course)











    # page_url = 'test'
    # html_files = glob('/Users/cameronyee/Desktop/canvas/courses/mhs/courses/te/*.html')
    # page_titles = ['Table of Contents','System Requirements','Using the Course','Lesson 1: Water All Around Us','Lesson 2: Surface Water','Lesson 3: Groundwater','Lesson 4: Watersheds','Lesson 5: Atmosphere','Lesson 6: Oceans','Lesson 7: Human Impacts on Water Resources']
    # module_name = 'Teacher Guide'
    # updateCoursePages(course_id, headers, html_files)
    # storeHtmlData(html_files)
    # module_name = 'Teacher Guide'
