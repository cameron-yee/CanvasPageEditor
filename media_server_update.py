import ftplib
from shutil import copyfile
import os
from glob import glob
import re
from colors import bcolors

def upload_css(course):
    try: 
        session = ftplib.FTP('***REMOVED***', '***REMOVED***', '***REMOVED***')
        session.cwd('media/canvas/{}/css'.format(course))
        f = '/Users/cyee/Desktop/canvas/courses/{}/resources/styles/css/concat/concat.css'.format(course)
        local_file = copyfile(f, './concat.css')
        session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
        os.remove('./concat.css')
        session.quit()
        print(bcolors.WARNING + 'CSS Uploaded' + bcolors.ENDC)
    except (ftplib.error_perm, FileNotFoundError):
        print(bcolors.FAIL + 'No concat.css file' + bcolors.ENDC)


def upload_js(course):
    try:
        session = ftplib.FTP('***REMOVED***', '***REMOVED***', '***REMOVED***')
        session.cwd('media/canvas/{}/js'.format(course))
        f = '/Users/cyee/Desktop/canvas/courses/{}/resources/js/concat/concat.js'.format(course)
        local_file = copyfile(f, './concat.js')
        session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
        os.remove('./concat.js')
        session.quit()
        print(bcolors.WARNING + 'JS Uploaded' + bcolors.ENDC)
    except (ftplib.error_perm, FileNotFoundError):
        print(bcolors.FAIL + 'No concat.js file' + bcolors.ENDC)


def upload_html(course):
    try:
        session = ftplib.FTP('***REMOVED***', '***REMOVED***', '***REMOVED***')
        session.cwd('media/canvas/{}/html'.format(course))
        html_folder = '/Users/cyee/Desktop/canvas/courses/{}/resources/html/*.html'.format(course)
        html_menus = glob(html_folder)
        for menu in html_menus:
            r = re.search('[^/]+.html$', menu)
            menu_name = r.group(0)
            local_file = copyfile(menu, './{}'.format(menu_name))
            session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
            os.remove('./{}'.format(menu_name))
        session.quit()
        print(bcolors.WARNING + 'HTML Uploaded' + bcolors.ENDC)
    except (ftplib.error_perm, FileNotFoundError):
        print(bcolors.FAIL + 'No HTML file' + bcolors.ENDC)


def upload_all(course):
    upload_css(course)
    upload_js(course)
    upload_html(course)
    print(bcolors.OKBLUE + 'DONE' + bcolors.ENDC)

if __name__ == '__main__':
    upload_css('3dmss')

