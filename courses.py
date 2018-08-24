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
    #count = 0
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
            #count += 1
            # print(r.links['next']['url'])
    except KeyError:
        isNext = False

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(courses)
    return courses


#Manual hardcoded list of courses required
def deleteCourses():
    courses_to_delete = [136, 138, 22, 105, 116, 113, 95, 104, 101, 103, 119, 134, 38, 54, 108, 114, 110, 50, 55, 49, 56, 129, 132, 127, 133, 31, 59, 32, 58, 99, 98, 107]
    vp_courses = [43, 45] #KEEP Course delete users
    
    #courses = listCourses()
    
    for course_id in courses_to_delete:
        url = auth.base_url + str(course_id)
        r = requests.delete(url, headers=auth.headers)
        print(bcolors.FAIL + 'COURSE DELETED: {}'.format(course_id) + bcolors.ENDC)
