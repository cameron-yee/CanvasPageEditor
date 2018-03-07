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

#CLI command definitions
def selectAction():
    parser = argparse.ArgumentParser(description='Pick action.')

    commands = {
        'uc': updateCoursePages,

    }
    
    parser.add_argument('command', choices=commands.keys())
    #
    args = parser.parse_args()

    commands[args.command]()
    

#Returns dictionary with subfolders as key and html files as values
def getHtmlFolders(top_directory):
    directories = [x[0] for x in os.walk(top_directory)]
    # print(directories)
    # directory_list = []

    # for directory in directories:
    #     print(directory)
    #     directory_dict[directory] = glob(directory + '{}'.format('/*.html'))
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(directory_dict)
    
    return directories


#Returns dictionary with subfolders as key and html files as values
def getHtmlFolders(course_id, headers, top_directory):
    directories = [x[0] for x in os.walk(top_directory)]
    directory_dict = {}

    for directory in directories:
        directory_dict[directory] = glob(directory + '{}'.format('/*.html'))
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(directory_dict)

def storeHtmlData(html_files):
    html_data = getHtmlData(html_files)
    html_dict = {}
    unset = []
    errors = False

    for i in range(len(html_files)):
        key = re.search('\d+_([^/]+.html$)', html_files[i])
        #sets the file 'url' without the 00_ as the key
        #stores both the full html file and the html data from the file
        if key:
            html_dict[str(key.group(1))] = html_files[i], html_data[i]
        else:
            unset.append(html_files[i])
            print(bcolors.FAIL + 'Unacceptable file names found.  Fix the following files: {}'.format(unset) + bcolors.ENDC)
            print(bcolors.WARNING + 'Make sure files follow the pattern: \'\\d+_([^/]+.html$)\'' + bcolors.ENDC)
            errors = True
        #sorts dictionary alphabetically by key
        # sorted_dict = OrderedDict(sorted(html_dict.items(), key=lambda t: t[0]))

    # unset = [x for x in unset if x != []]
    assert(errors == False)
    print(html_dict)
    return html_dict


def globHtml(directory):
    html_files = []
    html_files.append(glob(directory + '{}'.format('/*.html')))
    print(html_files)
    return html_files
    # sorted_dict = OrderedDict(sorted(html_dict.items(), key=lambda t: t[0]))
    # for dictionary in sorted_dict:
    #     print(dictionary)

    # print(sorted_dict)
    # return all_files



#NOT SURE IF THIS FUNCTION IS NECESSARY
#Sorts the html files in the same order that Canvas LMS API returns them
def sortHtmlFiles(paths):
    html_files = glob(str(path) + '/*.html')


#Gets every page in a course and appends the page url to a list
def getCoursePages(course_id, headers):
    # page = 1
    count = 0
    pages = []
    isNext = True
    first = True
    url = url_base + course_id + '/pages?per_page=50&page=1&sort=title&order=asc'
    r = requests.get(url, headers=headers, timeout=20)

    try:
        while first:
            r = requests.get(r.links['current']['url'], headers=headers)
            print(r.links['current']['url'])
            data = r.json()
            for page in data:
                pages.append(page['url'])
            first = False
        while isNext:
            r = requests.get(r.links['next']['url'], headers=headers)
            data = r.json()
            for page in data:
                pages.append(page['url'])
            count += 1
            print(r.links['next']['url'])
    except KeyError:
        isNext = False

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(pages)
    return pages


#Update content for each Canvas page in a given coures given the directory where the html files are stored
def updateCoursePages(course_id, headers, html_files):
    pages = getCoursePages(course_id, headers)
    sorted_dict = storeHtmlData(html_files)
    count = 0

    assert(len(pages) == len(sorted_dict))
    for key, value in sorted_dict.items():
        page_url = pages[count]
        html_content = value[1]
        updateIndividualPage(course_id, headers, page_url, value[0], value[1])
        count += 1
    print('Success')


#Prints json object for individual page
def getPageInformation(course_id, headers, page_url):
    url = url_base + course_id + '/pages/' + page_url
    r = requests.get(url, headers=headers)
    r.json
    x = json.loads(r.text)
    print(json.dumps(x, sort_keys=True, indent=4))


#Updates html body content for given Canvas page and html file, for updating entire course
def updateIndividualPage(course_id, headers, page_url, file_name, html_content=None):
    if html_content is not None:
        url = url_base + course_id + '/pages/' + page_url
        data = [('wiki_page[body]', html_content),]
        r = requests.put(url, headers=headers, data=data)
        print('Updating: {}'.format(page_url))
    else:
        url = url_base + course_id + '/pages/' + page_url
        with open(file_name, 'r') as f:
            html = f.read()
        data = [('wiki_page[body]', html),]
        r = requests.put(url, headers=headers, data=data)


#Create a new course in Canvas
def createNewCourse(headers, course_name):
    url = 'https://***REMOVED***.instructure.com/api/v1/accounts/1/courses'
    data = [('course[name]', course_name),]
    r = requests.post(url, headers=headers, data=data)


#Update course name
def updateCourseName(course_id, headers, new_course_name):
    url = url_base + course_id
    data = [('course[name]', new_course_name),]
    r = requests.put(url, headers=headers, data=data)


#Create a new module in a Canvas Course
def createNewModule(course_id, headers, module_name):
    url = url_base + course_id + '/modules'
    data = [('module[name]', module_name),]
    r = requests.post(url, headers=headers, data=data)


#Lists every item's information 
def listModuleItems(course_id, headers, module_name):
    module_id = getModuleId(course_id, headers, module_name)
    url = url_base + course_id + '/modules/' + module_id + '/items'
    data = [('module[name]', module_name),]
    r = requests.get(url, headers=headers, data=data)
    r.json
    x = json.loads(r.text)
    print(json.dumps(x, sort_keys=True, indent=4))


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


def doit(top_directory):
    directories = getHtmlFolders(top_directory)
    #list of dictionaries containing html files
    all_files = []
    for directory in directories:
        html_files = globHtml(directory)
        # html_dict = storeHtmlData(html_files)
        # all_files.append(html_dict)
    
    print(all_files)
    # html_folders = getHtmlFolders('/Users/cameronyee/Desktop/canvas/courses/mhs/courses')
    # all_html_files = []
    # for i in range(len(html_folders)):
    #     all_html_files.append(glob(html_folders[i] + '{}'.format('/*.html')))
    #     # x = appendFiles(all_html_files[i])
    #     # all_html_files.append(x)
    # for i in all_html_files:
    #     print(i)
    

if __name__  == '__main__':
    access_token = getAccessToken()
    headers = {"Authorization": "Bearer " + access_token}
    course_id = '122'
    # page_url = 'test'
    url_base = 'https://***REMOVED***.instructure.com/api/v1/courses/'
    # page_titles = ['Table of Contents','System Requirements','Using the Course','Lesson 1: Water All Around Us','Lesson 2: Surface Water','Lesson 3: Groundwater','Lesson 4: Watersheds','Lesson 5: Atmosphere','Lesson 6: Oceans','Lesson 7: Human Impacts on Water Resources']
    html_files = glob('/Users/cameronyee/Desktop/canvas/courses/mhs/courses/te/*.html')
    # module_name = 'Teacher Guide'
    # updateCoursePages(course_id, headers, html_files)
    # storeHtmlData(html_files)
    doit('/Users/cameronyee/Desktop/canvas/courses/mhs/courses/te')
    module_name = 'Teacher Guide'
    # updateCoursePages(course_id, headers, html_files)
    # getHtmlFolders(course_id, headers, '/Users/cameronyee/Desktop/canvas/courses/mhs/courses')
    storeHtmlData(course_id, headers, '/Users/cameronyee/Desktop/canvas/courses/mhs/courses')
    # storeHtmlData(html_files)

#NEED UPDATING:
    # selectAction

#FUNCTIONAL:
    # getCoursePages(course_id, headers)
    # getHtmlData(pages)
    # updateIndividualPage(course_id, headers, page_url, 'test.html')
    # createNewCourse('Canvas API Test Course', headers)
    # createNewModule('Test Module Creation', course_id, headers)
    # createNewPage('Test Page', 'test.html', course_id, headers)

