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
    print(bcolors.OKBLUE + '{} Updated'.format(page_name) + bcolors.ENDC)
    return page_url


#Updates html body content for given Canvas page and html file, for updating entire course
def updateIndividualPage(course_id, headers, page_url, file_path, html_content=None):
    if html_content is not None:
        url = url_base + course_id + '/pages/' + page_url
        data = [('wiki_page[body]', html_content),]
        r = requests.put(url, headers=headers, data=data)
        print(bcolors.OKBLUE + 'Updating: {}'.format(page_url) + bcolors.ENDC)
    else:
        url = url_base + course_id + '/pages/' + page_url
        with open(file_path, 'r') as f:
            html = f.read()
        data = [('wiki_page[body]', html),]
        r = requests.put(url, headers=headers, data=data)


#Creates pages in Canvas course modulec and adds html content to each page
def createPagesAndAddContent(course_id, headers, page_titles, html_files, module_name):
    assert(len(page_titles) == len(html_files))
    for i in range(len(page_titles)):
        page_url = createPageInModule(course_id, headers, page_titles[i], module_name)
        updateIndividualPage(course_id, headers, page_url, html_files[i])


#Gets token from hidden file so it will not show up on Git
def getAccessToken():
    token = auth.token
    return token


if __name__  == '__main__':
    course_id = '141'
    access_token = getAccessToken()
    headers = {"Authorization": "Bearer " + access_token}
    url_base = 'https://bscs.instructure.com/api/v1/courses/'
    page_titles = ['5.1 Making Links', '5.2 Making Links Continued', '5.3 Focus Question', '5.4 What Do You Think', '5.5 Try This', '5.6 Temperatures Around the Globe', '5.5 MNSTeLLA Video Analysis Process', '5.8 Video Viewing Basics', '5.9 A Classroom Conversation', '5.10 Identify Elicit and Probe Questions', '5.11 Identify Elicit and Probe Continued', '5.12 Identify Missed Opportunities to Probe']
    directory = '/Users/cyee/Desktop/canvas/courses/mnstella/courses/01_pe/02_ms_course_1/05_segment_5'
    html_files = glob(directory + '{}'.format('/*.html'), recursive=False)

    createPagesAndAddContent(course_id, headers, page_titles, html_files, 'Segment 5 - Analyzing Classroom Video: Elicit and Probe Questions')
