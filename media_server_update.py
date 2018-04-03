import ftplib
from shutil import copyfile
import os
from glob import glob
import re

def upload_css(course):
    session = ftplib.FTP('***REMOVED***', '***REMOVED***', '***REMOVED***')
    session.cwd('media/canvas/{}/css'.format(course))
    print(session.pwd())
    f = '/Users/cameronyee/Desktop/canvas/courses/{}/resources/styles/css/concat/concat.css'.format(course)
    local_file = copyfile(f, './concat.css')
    session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
    os.remove('./concat.css')
    session.quit()


def upload_js(course):
    session = ftplib.FTP('***REMOVED***', '***REMOVED***', '***REMOVED***')
    session.cwd('media/canvas/{}/js'.format(course))
    print(session.pwd())
    f = '/Users/cameronyee/Desktop/canvas/courses/{}/resources/js/concat/concat.js'.format(course)
    local_file = copyfile(f, './concat.js')
    session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
    os.remove('./concat.js')
    session.quit()


def upload_html(course):
    session = ftplib.FTP('***REMOVED***', '***REMOVED***', '***REMOVED***')
    session.cwd('media/canvas/{}/html'.format(course))
    print(session.pwd())
    html_folder = '/Users/cameronyee/Desktop/canvas/courses/{}/resources/html/*.html'.format(course)
    html_menus = glob(html_folder)
    print(html_menus)
    for menu in html_menus:
        r = re.search('[^/]+.html$', menu)
        menu_name = r.group(0)
        local_file = copyfile(menu, './{}'.format(menu_name))
        session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
        os.remove('./{}'.format(menu_name))
    session.quit()


def upload_all(course):
    upload_css(course)
    upload_js(course)
    upload_html(course)

if __name__ == '__main__':
    upload_all('mss')



