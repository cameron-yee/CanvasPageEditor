import requests
from glob import glob
import json
import pprint
import re
import os

def selectAction():
    questions = [
        inquirer.List('action',
                      message="What do you want to do?",
                      choices=['Create course', 'Create module', 'Create page', 'Update page'],
        ),
    ]
    answers = inquirer.prompt(questions)

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

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(pages)
    return pages


#Gets html body content for each page in course
def getHtmlData(pages):
    html_data = []
    for page in pages:
        with open(page + '.html', 'r') as f:
            contents = f.read
            html_data.append(contents) 
            f.close()
    print(html_data)


#Updates html body content for each Canvas page in a given coures given the directory where the html files are stored
def updateCoursePages(course_id, headers, html_files):
    pages = getCoursePages(course_id, headers)
    count = 0

    assert(len(pages) == len(html_files))
    for page_url in pages:
        updateIndividualPage(course_id, headers, page_url, html_files[count])
        count += 1


#Prints json object for individual page
def getPageInformation(course_id, page_url, headers):
    url = url_base + course_id + '/pages/' + page_url
    r = requests.get(url, headers=headers)
    r.json
    x = json.loads(r.text)
    print(json.dumps(x, sort_keys=True, indent=4))


#Updates html body content for given Canvas page and html file
def updateIndividualPage(course_id, headers, page_url, file_name):
    url = url_base + course_id + '/pages/' + page_url
    with open(file_name, 'r') as f:
        html = f.read()
    data = [('wiki_page[body]', html),]
    r = requests.put(url, headers=headers, data=data)


#Create a new course in Canvas
def createNewCourse(course_name, headers):
    url = 'https://***REMOVED***.instructure.com/api/v1/accounts/1/courses'
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
    with open('Token.txt', 'r') as f:
        token = f.read()
        f.close()
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
    access_token = getAccessToken()
    headers = {"Authorization": "Bearer " + access_token}
    course_id = '122'
    page_url = 'test'
    url_base = 'https://***REMOVED***.instructure.com/api/v1/courses/'
    page_titles = ['Table of Contents','System Requirements','Using the Course','Lesson 1: Water All Around Us','Lesson 2: Surface Water','Lesson 3: Groundwater','Lesson 4: Watersheds','Lesson 5: Atmosphere','Lesson 6: Oceans','Lesson 7: Human Impacts on Water Resources']
    html_files = glob('/Users/cameronyee/Desktop/canvas/courses/mhs/courses/mhs_te/*.html')
    module_name = 'Teacher Guide'

    print(html_files)
    # getCoursePages(course_id, headers)
    updateCoursePages(course_id, headers, html_files)

#NEED UPDATING:
    # selectAction()

#FUNCTIONAL:
    # getCoursePages(course_id, headers)
    # getHtmlData(pages)
    # updateIndividualPage(course_id, headers, page_url, 'test.html')
    # createNewCourse('Canvas API Test Course', headers)
    # createNewModule('Test Module Creation', course_id, headers)
    # createNewPage('Test Page', 'test.html', course_id, headers)

