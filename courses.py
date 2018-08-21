from colors import bcolors
import requests
import json
import auth

#Create a new course in Canvas
def createNewCourse(course_name, headers):
    url = 'https://bscs.instructure.com/api/v1/accounts/1/courses'
    data = [('course[name]', course_name),]
    r = requests.post(url, headers=headers, data=data)


#uc argparser
#Update course name
def updateCourseName(new_course_name, course_id, headers):
    url = auth.url_base + course_id
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
    url = auth.url_base + course_id
    r_old = requests.get(url, headers=headers)
    old_data = r_old.json()
    old_course_code = old_data['course_code']

    data_update = [('course[course_code]', new_course_code),]
    r_update = requests.put(url, headers=headers, data=data_update)

    print(bcolors.BOLD + 'Updated course code for course {}'.format(course_id) + bcolors.ENDC) 
    print(bcolors.WARNING + 'Old course code: {}'.format(old_course_code) + bcolors.ENDC) 
    print(bcolors.WARNING + 'New course code: {}'.format(new_course_code) + bcolors.ENDC) 
