#!/usr/local/bin/python3
from colors import bcolors
import requests
import json
import auth
import pprint

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
    

def listCourses():
    courses  = []
    isNext = True
    first = True

    url = 'https://bscs.instructure.com/api/v1/courses?per_page=1000&page=1&sort=name&order=asc'
    r = requests.get(url, headers=auth.headers)

    response = r.json()

    try:
        while first:
            r = requests.get(r.links['current']['url'], headers=auth.headers)
            # print(r.links['current']['url'])
            data = r.json()
            for course in data:
                courses.append(course)
            first = False
        while isNext:
            r = requests.get(r.links['next']['url'], headers=auth.headers)
            data = r.json()
            for course in data:
                courses.append(course)
    except KeyError:
        isNext = False

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(courses)
    return courses


#Manual hardcoded list of courses required
def deleteCourses():
    courses_to_delete = [136, 138, 22, 116, 113, 95, 104, 101, 103, 119, 134, 38, 54, 108, 114, 110, 50, 55, 49, 56, 129, 132, 127, 133, 31, 59, 32, 58, 99, 98, 107]
    #vp_courses = [43, 45] #KEEP Course delete users
    
    #courses = listCourses()
    
    for course_id in courses_to_delete:
        url = auth.url_base + str(course_id)
        data = [('event', 'delete'),]
        r = requests.delete(url, headers=auth.headers, data=data)
        print(bcolors.FAIL + 'COURSE DELETED: {}'.format(course_id) + bcolors.ENDC)


def getCourseUsers(course_id):
    users  = []
    isNext = True
    first = True

    url = 'https://bscs.instructure.com/api/v1/courses/{course_id}/users?per_page=1000&page=1'.format(course_id=course_id)
    r = requests.get(url, headers=auth.headers)

    response = r.json()

    try:
        while first:
            r = requests.get(r.links['current']['url'], headers=auth.headers)
            data = r.json()
            for user in data:
                users.append(user)
            first = False
        while isNext:
            r = requests.get(r.links['next']['url'], headers=auth.headers)
            data = r.json()
            for user in data:
                users.append(user)
    except KeyError:
        isNext = False

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(users)
    return users


#Returns list of login_ids for users in a course; excludes locked users
def getAllCourseUserLoginIDs(course_id):
    users = getCourseUsers(course_id)
    login_ids = []

    locked_users = [345, 81, 104, 356, 79, 156, 161, 98, 322, 170, 89, 654, 489, 160, 351, 154, 200, 159, 528, 153, 651, 650, 649, 106, 352, 411, 191, 392, 527, 529, 530]

    for user in users:
        print(user)
        url = 'https://bscs.instructure.com/api/v1/users/{}/logins'.format(user['id'])
        r = requests.get(url, headers=auth.headers)
        user_login = r.json()
        if user['id'] not in locked_users and '@bscs.org' not in user['login_id']:
            login_ids.append(user_login[0]['id'])

    return login_ids


#Sets new login password for all users in course except locked users
def setDefaultCourseUsersPassword(course_id, new_password):
    user_login_ids = getAllCourseUserLoginIDs(course_id)

    for user_login_id in user_login_ids:
        url = 'https://bscs.instructure.com/api/v1/accounts/1/logins/{}'.format(user_login_id)
        data = [('login[password]', new_password)]
        r = requests.put(url, headers=auth.headers, data=data)
        try: 
            if r.json()['errors']:
                print(user_login_id, r.json())
        except KeyError:
            pass

    print(bcolors.WARNING + 'All passwords for users in course {} set to "{}"'.format(course_id, new_password) + bcolors.ENDC)


#def createNewLoginForCourseUsers(course_id, new_login_password):
#    users = getCourseUsers(course_id)
#    locked_users = [345, 81, 104, 356, 79, 156, 161, 98, 322, 170, 89, 654, 489, 160, 351, 154, 200, 159, 528, 153, 651, 650, 649, 106, 352, 411, 191, 392, 527, 529, 530]
#
#    url = 'https://bscs.instructure.com/api/v1/accounts/1/logins/'
#
#    for user in users:
#        if user['id'] not in locked_users and '@bscs.org' not in user['login_id']:
#            data = [('user[id]', str(user['id'])), ('login[unique_id]', '{}'.format(user['login_id'])), ('login[password]', new_login_password)]
#            r = requests.post(url, headers=auth.headers, data=data)
#
#            print(r)
#            print(bcolors.WARNING + 'This password: "{}" will work for all users in course {}'.format(new_login_password, course_id) + bcolors.ENDC)


#if __name__ == '__main__':
    #getCourseUsers(181)
    #deleteCourses()
    #getAllCourseUserLoginIDs(187)
    #setDefaultCourseUsersPassword(187, 'passwordtest')
    #kcreateNewLoginForCourseUsers(187, 'test')
