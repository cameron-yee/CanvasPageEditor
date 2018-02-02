import requests
import json
import pprint
import re
# import inquirer

#Not sure how to download inquirer
def selectAction():
    questions = [
        inquirer.List('action',
                      message="What do you want to do?",
                      choices=['Create course', 'Create module', 'Create page', 'Update page']
        ),
    ]
    answers = inquirer.prompt(questions)

#Gets every page in a course and appends the page url to a list
def getCoursePages(course_id, headers):
    # page = 1
    count = 0
    pages = []
    isNext = True
    url = url_base + course_id + '/pages?per_page=1&page=1&sort=created_at&order=asc'
    r = requests.get(url, headers=headers, timeout=20)

    #
    #TODO: currently gets every page except last page.  Need to find how to include last page in loop
    #
    try:
        while isNext:
            r = requests.get(r.links['next']['url'], headers=headers)
            data = r.json()
            for page in data:
                pages.append(page['url'])
            count += 1
            # print(r.links['next']['url'])
    except KeyError:
        # print(r.links['last']['url'])
        # page_no = re.match('&page=[0-9]+', r.links['last']['url'])
        # print(page_no)
        # page_no = re.match('[0-9]+', page_no)
        # print(page_no)
        # r = requests.get(url_base + course_id + 'pages?page=' + page_no)
        # print(r.links)
        # page = r.json()
        # pages.append(page[0])
        isNext = False

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(pages)
    return pages
    # print(count)


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
def updateCoursePages(pages, headers):
    # url_pages = '?per_page=50&page=' + str(page) + '&workflow_state=active'
    pages_html = []
    for page_url in pages:
        url = url_base + course_id + '/pages/' + page + '?wiki_page[body]=' + updated_html
        r = requests.get(url, headers=headers)
        data = r.json()
        pages_html.append(data['body'])
    for body in pages_html:
        print(pages_html)
    
    # print(json.dumps(pages, sort_keys=True, indent=4))


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


#Create a new page in a Canvas Course
def createNewPage(page_title, html_file, course_id, headers):
    url = url_base + course_id + '/pages'
    with open(html_file, 'r') as f:
        body = f.read()
        f.close()
    data = [('wiki_page[title]', page_title), ('wiki_page[body]', body),]
    r = requests.post(url, headers=headers, data=data)


#Gets token from hidden file so it will not show up on Git
def getAccessToken():
    with open('Token.txt', 'r') as f:
        token = f.read()
        f.close()
    return token


if __name__  == '__main__':
    access_token = getAccessToken()
    headers = {"Authorization": "Bearer " + access_token}
    course_id = '122'
    page_url = 'test'
    url_base = 'https://***REMOVED***.instructure.com/api/v1/courses/'
    updateCourseName('Earth\'s Water Systems Teacher Guide', course_id, headers)

#NEED UPDATING:
    #getCoursePages(course_id, headers)
    # selectAction()

#FUNCTIONAL:
    # getHtmlData(pages)
    # updateIndividualPage(course_id, headers, page_url, 'test.html')
    # createNewCourse('Canvas API Test Course', headers)
    # createNewModule('Test Module Creation', course_id, headers)
    # createNewPage('Test Page', 'test.html', course_id, headers)

