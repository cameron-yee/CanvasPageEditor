import os
from colors import bcolors
import json
import auth
import requests
import re
from file_functions import getHtmlFolders, globHtml
import chrome

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


def updateCoursePages(top_directory, course_id):
    html_files = []
    directories = getHtmlFolders(top_directory)

    for i in range(len(directories)):
        directory_html_files = globHtml(directories[i])
        for f in directory_html_files:
            if f not in html_files: html_files.append(f)

    skipped = []
    count = 0
    for f in sorted(html_files):
        success_status = updateIndividualPage(course_id, auth.headers, f)
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
        try: 
            with open(file_path, 'r') as f:
                contents = f.read()
                patterns = ['<span url="([^\n]+)" courses="([^\n]+)"></span>', '<span url="([^\n]+)"></span>', '<span courses="([^\n]+)"></span>']
                for i in range(len(patterns)):
                    m = re.search(patterns[i], contents)
                    if m is not None:
                        return m.groups(), i, contents

            return None, None, contents
            #print('No variables provided in command or file for: {}'.format(file_path))
        except IsADirectoryError:
            pass

    def checkPageExistsInCanvas(url):
        r = requests.get(url, headers=headers)
        return r.status_code

    #TODO: This isn't working as expected
    success = True
    def fail():
        success = False

    #Updates page title
    def changePageName(old_page_url, course_id):
        url = auth.url_base + course_id + '/pages/' + old_page_url
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
        url = auth.url_base + course_id + '/pages/' + page_url
        data = [('wiki_page[body]', html_content),]
        status = checkPageExistsInCanvas(url)
        if status == 200:
            r = requests.put(url, headers=headers, data=data)
            if auth.chromeUp:
                chrome.refreshPage(course_id, page_url)
            print(bcolors.OKBLUE + 'Updating: {} for course {}'.format(page_url, course_id) + bcolors.ENDC) if r.status_code == 200 else print(bcolors.FAIL + 'Request Error: {}\nPage: {}'.format(r.status_code,page_url) + bcolors.ENDC)
        else:
            #TODO: This isn't working
            print('Received {} response for {}'.format(status, page_url))
            success = False

    try:
        page_info = getPageInfo()
        if page_info[0] is not None:
            pattern_match_case = page_info[1]
    except TypeError as e:
        print(e)

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

########################################################################################################################
###########################                        END FUNCTIONING CODE                      ###########################
########################################################################################################################

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
