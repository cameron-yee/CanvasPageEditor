import requests
import json
import pprint
import re

def getCoursePages(course_id, headers):
    # page = 1
    count = 0
    pages = []
    isNext = True
    url = url_base + course_id + '/pages?per_page=100&page=1&sort=created_at&order=asc'
    r = requests.get(url, headers=headers, timeout=20)

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

def getHtmlData(pages):
    html_data = []
    for page in pages:
        with open(page + '.html', 'r') as f:
            contents = f.read
            html_data.append(contents) 
            f.close()
    print(html_data)


def getPageInformation(course_id, page_url, headers):
    url = url_base + course_id + '/pages/' + page_url
    r = requests.get(url, headers=headers)
    r.json
    x = json.loads(r.text)
    # print(json.dumps(x, sort_keys=True, indent=4))


def updateIndividualPage(course_id, headers, page_url, file_name):
    url = url_base + course_id + '/pages/' + page_url
    with open(file_name, 'r') as f:
        html = f.read()
    data = [('wiki_page[body]', html),]
    r = requests.put(url, headers=headers, data=data)


# def updateCoursePages(pages):
#     for page in pages:

def getAccessToken():
    with open('Token.txt', 'r') as f:
        token = f.read()
        f.close()
    return token


if __name__  == '__main__':
    access_token = getAccessToken()
    headers = {"Authorization": "Bearer " + access_token}
    course_id = '25'
    page_url = 'test'
    url_base = 'https://***REMOVED***.instructure.com/api/v1/courses/'

    # pages = getCoursePages(course_id, headers)
    updateIndividualPage(course_id, headers, page_url, 'test.html')