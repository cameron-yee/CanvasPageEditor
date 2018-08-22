#!/usr/local/bin/python3
#from colors import bcolors
import requests
import json
import auth
import pprint
from datetime import datetime, timedelta

#Create a new course in Canvas
def listUsers():
    #count = 0
    users  = []
    isNext = True
    first = True

    url = 'https://bscs.instructure.com/api/v1/accounts/1/users?per_page=1000&page=1&sort=name&order=asc'
    r = requests.get(url, headers=auth.headers)

    response = r.json()

    try:
        while first:
            r = requests.get(r.links['current']['url'], headers=auth.headers)
            # print(r.links['current']['url'])
            data = r.json()
            for user in data:
                users.append(user)
            first = False
        while isNext:
            r = requests.get(r.links['next']['url'], headers=auth.headers)
            data = r.json()
            for user in data:
                users.append(user)
            #count += 1
            # print(r.links['next']['url'])
    except KeyError:
        isNext = False

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(users)
    return users


def getUserInfoByName(name):
    users = listUsers()
    for user in users:
        if name in user['name']:
            print(user)


def getUserInfo(search_term):
    users = listUsers()
    for user in users:
        if search_term.isdigit():
            if search_term == str( user['id']):
                print(user)
        else:
            if search_term in user['name']:
                print(user)


def deleteDeprecatedUsers():
    locked_user_ids = []
    bscs_login_id = '@bscs.org'


def getUserEnrollments():
    users = listUsers()
    user_enrollments = {}

    for user in users:
        user_id = user['id']
        url = 'https://bscs.instructure.com/api/v1/users/{}/enrollments'.format(user_id)
        r = requests.get(url, headers=auth.headers)
        enrollments = r.json()
        user_enrollments[user_id] = []
        most_latest_activity = datetime(2000, 1, 1) #arbitrary old date

        for enrollment in enrollments:
            if enrollment['last_activity_at'] is not None:
                activity = datetime.strptime(enrollment['last_activity_at'][:10], '%Y-%m-%d')
                most_latest_activity = activity if activity > most_latest_activity else most_latest_activity
                user_enrollments[user_id].append((enrollment['course_id'], datetime.strptime(enrollment['last_activity_at'][:10], '%Y-%m-%d')))
                #pp = pprint.PrettyPrinter(indent=4)
                #pp.pprint(user_enrollments[user_id])

        most_latest_activity = None if most_latest_activity == datetime(2000, 1, 1) else most_latest_activity
        user_enrollments[user_id].insert(0, most_latest_activity)
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(user_enrollments)

    #pp.pprint(user_enrollments)
    return user_enrollments #Dict: key = user_id, values = [most_latest_activity, (course_id, latest_activity_in_course)]


def deleteUser(user_id):
    locked_users = [345, 79]
    if user_id not in locked_users:
        print('User deleted: {}'.format(user_id))


def purgeUsers():
    courses_to_be_deleted = []
    user_enrollments = getUserEnrollments()
    today = datetime.today()

    for key, values in user_enrollments.items(): 
        if values[0] is not None:
            time_since_last_activity = today - values[0]
            print(key, time_since_last_activity.days)
            if time_since_last_activity.days > 365:
               deleteUser(key)
               continue
            else:
                for i in range(1, len(values)):
                    if values[i][0] not in courses_to_be_deleted:
                        deleteUser(key)
                        continue
        else:
            deleteUser(key)


if __name__ == '__main__':
    #listUsers()
    #getUserInfoByName('Jonathan')
    #getUserEnrollments()
    purgeUsers()
