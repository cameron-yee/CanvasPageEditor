#!/usr/local/bin/python3
from colors import bcolors
import requests
import json
import auth
import pprint
from datetime import datetime, timedelta

#Returns a list of all users
def listUsers(p=False):
    users  = []
    isNext = True
    first = True

    url = 'https://bscs.instructure.com/api/v1/accounts/1/users?per_page=1000&page=1&sort=name&order=asc&include[]=last_login'
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

    if p:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(users)

    return users


#Prints user json repsonse object for searched user
def printUserInfo(search_term):
    users = listUsers()
    for user in users:
        if search_term.isdigit():
            if search_term.lower() == str(user['id']).lower():
                print(user)
        else:
            if search_term.lower() in user['name'].lower():
                print(user)


#Returns user json repsonse object for searched user
def getUserInfo(search_term):
    users = listUsers()
    for user in users:
        if search_term.isdigit():
            if search_term.lower() == str(user['id']).lower():
                return user
        else:
            if search_term.lower() in user['name'].lower():
                return user


#Prints out user enrollment json response objects for a searched user
def printUserEnrollments(search_term):
    user = getUserInfo(search_term)
    user_id = user['id']
    url = 'https://bscs.instructure.com/api/v1/users/{}/enrollments'.format(user_id)
    r = requests.get(url, headers=auth.headers)
    enrollments = r.json()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(enrollments)


#Returns dictionary of users with last activity overall and all enrolled courses with last activity in each course
#def getAllUserEnrollments():
#    users = listUsers()
#    user_enrollments = {}
#
#    for user in users:
#        user_id = user['id']
#        url = 'https://bscs.instructure.com/api/v1/users/{}/enrollments'.format(user_id)
#        r = requests.get(url, headers=auth.headers)
#        enrollments = r.json()
#        user_enrollments[user_id] = []
#        most_latest_activity = datetime(2000, 1, 1) #arbitrary old date
#
#        for enrollment in enrollments:
#            if enrollment['last_activity_at'] is not None:
#                activity = datetime.strptime(enrollment['last_activity_at'][:10], '%Y-%m-%d')
#                most_latest_activity = activity if activity > most_latest_activity else most_latest_activity
#                user_enrollments[user_id].append((enrollment['course_id'], datetime.strptime(enrollment['last_activity_at'][:10], '%Y-%m-%d')))
#
#        most_latest_activity = None if most_latest_activity == datetime(2000, 1, 1) else most_latest_activity
#        user_enrollments[user_id].insert(0, most_latest_activity)
#
#    return user_enrollments #Dict: key = user_id, values = [most_latest_activity, (course_id, latest_activity_in_course)]


def getAllUserEnrollments():
    users = listUsers()
    user_enrollments = {}

    for user in users:
        user_id = user['id']

        enrollments  = []
        isNext = True
        first = True

        url = 'https://bscs.instructure.com/api/v1/users/{}/enrollments'.format(user_id)
        r = requests.get(url, headers=auth.headers)

        try:
            while first:
                r = requests.get(r.links['current']['url'], headers=auth.headers)
                data = r.json()
                for enrollment in data:
                    enrollments.append(enrollment)
                first = False
            while isNext:
                r = requests.get(r.links['next']['url'], headers=auth.headers)
                data = r.json()
                for enrollment in data:
                    enrollments.append(enrollment)
        except KeyError:
            isNext = False

        last_login = datetime.strptime(user['last_login'][:10], '%Y-%m-%d' )if user['last_login'] is not None else None

        user_enrollments[user_id] = [last_login]

        for enrollment in enrollments:
            user_enrollments[user_id].append(enrollment['course_id'])

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(len(user_enrollments))
    return user_enrollments


#WARNING: THIS FUNCTION IS LIVE
#Deletes the specified uesr from our Canvas account
def deleteUser(user_id):
    user = getUserInfo(str(user_id))
    locked_users = [345, 81, 104, 356, 79, 156, 161, 98, 322, 170, 89, 654, 489, 160, 351, 154, 200, 159, 528, 153, 651, 481, 650, 649, 106, 352, 411, 191, 392, 527, 529, 530]
    if user_id not in locked_users and '@bscs.org' not in user['login_id']:
        #url = 'https://bscs.instructure.com/api/v1/accounts/1/users/{}'.format(user_id)
        #r = requests.delete(url, headers=auth.headers)
        print(bcolors.FAIL + 'User deleted: {}'.format(user_id) + bcolors.ENDC)
        return None
    else:
        print(bcolors.WARNING + 'User NOT deleted: {}.  This user is protected against deletion.'.format(user_id) + bcolors.ENDC)
        return user_id


#Determines whether a user should be deleted based on 3 criteria:
#   1. User's only enrollments are in courses that will be deleted
#   2. User is not enrolled in any course
#   3. User's last activity is greater than 1 year ago
def purgeUsers():
    courses_to_delete_users_from = [136, 138, 22, 105, 116, 113, 95, 104, 101, 103, 119, 134, 38, 54, 108, 114, 110, 50, 55, 49, 56, 129, 132, 127, 133, 31, 59, 32, 58, 99, 98, 43, 45]
    user_enrollments = getAllUserEnrollments()
    today = datetime.today()
    count = 0
    saved_from_death = []

    for key, values in user_enrollments.items(): 
        only_in_deleted_courses = True

        if values[0] is not None:
            time_since_last_activity = today - values[0]
            if time_since_last_activity.days > 365:
                saved = deleteUser(key)
                if saved is not None:
                    saved_from_death.append(saved)
                    continue
                else:
                   count += 1
                   continue
            else:
                for i in range(1, len(values)):
                    if values[i] not in courses_to_delete_users_from:
                        only_in_deleted_courses = False

            if only_in_deleted_courses:
                saved = deleteUser(key)
                if saved is not None:
                    saved_from_death.append(saved)
                    continue
                else:
                    count += 1
                    continue
        #else:
        #    deleteUser(key)
        #    count += 1

    print(bcolors.WARNING + '{} users deleted out of {} in Canvas'.format(count, len(user_enrollments)) + bcolors.ENDC)
    print(bcolors.OKGREEN + 'Saved from deletion: {}'.format(saved_from_death) + bcolors.ENDC)


#if __name__ == '__main__':
    #listUsers()
    #getUserInfoByName('Jonathan')
    #getAllUserEnrollments()
    #purgeUsers()
