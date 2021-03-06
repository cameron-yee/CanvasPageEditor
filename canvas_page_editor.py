import pprint
import argparse
import auth

#local file imports
from colors import bcolors
from media_server_update import *
import chrome
from file_functions import getHtmlFolders, globHtml
from pages import updateIndividualPage, updateCoursePages, updatePageName, getPageInformation
from courses import updateCourseName, updateCourseCode, listCourses, deleteCourses, setDefaultCourseUsersPassword
from users import listUsers, printUserInfo, purgeUsers, printUserEnrollments, deleteUser

#TODO: Add variable types to improve readability using typing.py lib
#import typing

#CLI command definitions
def selectAction():
    parser = argparse.ArgumentParser(description='Pick action.')
    subparsers = parser.add_subparsers(help='sub-command help')

    #commands for updating entire course
    parser_uc = subparsers.add_parser('uc', help='Commands to use when updateCoursePages')
    parser_uc.add_argument('-n','--name', help='Change course name', action='store', nargs='?', default=None)
    parser_uc.add_argument('-c','--code', help='Change course code', action='store', nargs='?', default=None)
    parser_uc.add_argument('top_directory', help='Enter the directory that contains the html files, or subfolders that contain the html files', nargs='?', default=None, type=str)
    parser_uc.add_argument('cid', help='Enter course ID', nargs='?', default=None, type=str) #nargs allows default to work
    parser_uc.set_defaults(which='uc')

    #commands for updating individual course page
    parser_ind = subparsers.add_parser('ind', help='Commands to use when updateIndividualPage')
    #parser_ind.add_argument('-url','--page_url', action='store', help='Enter the last section of the url that the page is on', type=str)
    parser_ind.add_argument('file_path', help='Enter the path to file on your local device', type=str)
    parser_ind.add_argument('-nn', '--newname', action='store', nargs='?', default=None)
    parser_ind.add_argument('cid', help="Enter course ID", nargs='?', default=None, type=str)
    parser_ind.set_defaults(which='ind')

    #commands for updating media server
    parser_static = subparsers.add_parser('static', help='Commands to use when pushing static files to media server')
    parser_static.add_argument('-c', '--css', action='count', help='Update css file on media server')
    parser_static.add_argument('-j', '--js', action='count', help='Update js file on media server')
    parser_static.add_argument('-ht', '--html', action='count', help='Update html menu on media server')
    parser_static.add_argument('-i','--img', action='store', help='Local image path to upload', type=str)
    parser_static.add_argument('course_prefix', help='Enter the prefix of the course', type=str)
    parser_static.add_argument('-sc', '--subcourse', action='store', help='Update css file on media server', type=str)
    parser_static.add_argument('-f','--folder', action='store', help='Folder to upload img to in AWS', type=str)
    parser_static.set_defaults(which='static')

    #commands for using with chrome reload
    parser_chrome = subparsers.add_parser('chrome', help='Commands to use when using capi with chromerefresh')
    parser_chrome.add_argument('watchpath', help="Path to watch for content changes", type=str)
    parser_chrome.set_defaults(which='chrome')

    #commands for users
    parser_users = subparsers.add_parser('users', help='Commands to use when doing user specific tasks')
    parser_users.add_argument('-ll', '--list', action='count', help="Lists all users in Canvas instance")
    parser_users.add_argument('-s', '--search', action='store', help="Name or ID of user to search for", type=str)
    parser_users.add_argument('-p', '--purge', action='count', help="Command to remove old and unwanted users from Canvas instance.")
    parser_users.add_argument('-e', '--enrollments', action='count', help="List enrollments for user that was searched for.")
    parser_users.add_argument('-d', '--delete', action='store', help="ID of user to DELETE", type=int)
    parser_users.set_defaults(which='users')

    #commands for courses information
    parser_courses = subparsers.add_parser('courses', help='Commands to use when getting course info')
    parser_courses.add_argument('-ll', '--list', action='count', help="Add flag to view all courses")
    parser_courses.add_argument('-dc', '--deletecourses', action='count', help="If present, will delete list of courses that are marked for deletion.")
    parser_courses.add_argument('-sp', '--setpassword', action='store', help="Enter password to set for users in course.", type=str)
    parser_courses.add_argument('cid', help="Enter course ID", nargs='?', default=None, type=str)
    parser_courses.set_defaults(which='courses')
    
    args = parser.parse_args()
    return args


if __name__  == '__main__':
    args = selectAction()

    if args.which == 'uc':
       if args.name is not None:
           course_id = args.top_directory #If args.name is given, top_directory argument will be the givin course id because only 2 arguments will be given
           updateCourseName(str(args.name), course_id, auth.headers) 
       elif args.code is not None: 
           course_id = args.top_directory #If args.code is given, top_directory argument will be the givin course id because only 2 arguments will be given
           updateCourseCode(str(args.code), args.top_directory, auth.headers) 
       else:
           updateCoursePages(args.top_directory, args.cid)

    if args.which == 'ind':
       course_id = args.cid
       #Always passing course_id even if None to avoid another if statement
       updateIndividualPage(course_id, auth.headers, args.file_path) if args.newname is None else updateIndividualPage(course_id, auth.headers, args.file_path, args.newname)

    if args.which == 'static':
        course = args.course_prefix
        if args.css is not None:
            #upload_css_aws(course, args.subcourse)
            upload_css_sftp(course, args.subcourse)
        if args.js is not None:
            #upload_js_aws(course, args.subcourse)
            upload_js_sftp(course, args.subcourse)
        if args.html is not None:
            #upload_html_aws(course, args.subcourse)
            upload_html_sftp(course, args.subcourse)
        if args.img is not None:
            upload_img_aws(args.img, course, args.folder, args.subcourse)
        if args.css is None and args.js is None and args.html is None and args.img is None:
            upload_all(course, args.subcourse)
            print('Updated {} static files'.format(course))

    if args.which == 'chrome':
        course_id = None

        chrome.startChrome()
        auth.chromeUp = True
        chrome.watch(args.watchpath)

    if args.which == 'users':
        if args.list is not None:
            listUsers(True)
        elif args.purge is not None:
            confirm = input('Enter Canvas admin password to initiate THE PURGE: ')
            purgeUsers() if confirm == auth.canvas_password else print('PURGE DENIED. Invalid password.')
        elif args.delete is not None:
            confirm = input('Enter Canvas admin password to delete user: ')
            deleteUser(args.delete) if confirm == auth.canvas_password else print('ACTION DENIED. Invalid password.')
        elif args.enrollments is not None:
            printUserEnrollments(args.search)
        else:
            printUserInfo(args.search)

    if args.which == 'courses':
        if args.list is not None:
            listCourses()
        if args.deletecourses is not None:
            confirm = input('Enter Canvas admin password to delete courses: ')
            deleteCourses() if confirm == auth.canvas_password else print('ACTION DENIED. Invalid password.')
        if args.setpassword is not None and args.cid is not None:
            setDefaultCourseUsersPassword(args.cid, args.setpassword)

