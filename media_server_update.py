import ftplib
from shutil import copyfile
import os
from glob import glob
import re
from colors import bcolors
from auth import server, user, password, remote_base, local_base
import paramiko

def upload_css_sftp(course, sub_course=None):
    try:
        port = 22

        if sub_course is not None:
            sub_course = '/{}'.format(sub_course)
        else:
            sub_course = ''

        local_css_path = '{}/{}/resources{}/styles/css/concat/concat.css'.format(local_base, course, sub_course)
        remote_css_path = '{}/{}{}/css/concat.css'.format(remote_base, course, sub_course)

        transport = paramiko.Transport((server, port))
        transport.connect(username=user, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_css_path, remote_css_path)

        sftp.close()
        transport.close()
        print(bcolors.WARNING + 'CSS Uploaded' + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No concat.css file' + bcolors.ENDC)


def upload_js_sftp(course, sub_course=None):
    try:
        port = 22

        if sub_course is not None:
            sub_course = '/{}'.format(sub_course)
        else:
            sub_course = ''

        local_js_path = '{}/{}/resources{}/js/concat/concat.js'.format(local_base, course, sub_course)
        remote_js_path = '{}/{}{}/js/concat.js'.format(remote_base, course, sub_course)

        transport = paramiko.Transport((server, port))
        transport.connect(username=user, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_js_path, remote_js_path)

        sftp.close()
        transport.close()
        print(bcolors.WARNING + 'JS Uploaded' + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No concat.js file' + bcolors.ENDC)


def upload_html_sftp(course, sub_course=None):
    try:
        port = 22

        if sub_course is not None:
            sub_course = '/{}'.format(sub_course)
        else:
            sub_course = ''

        html_folder = '{}/{}/resources{}/html/*.html'.format(local_base, course, sub_course)
        html_menus = glob(html_folder)

        transport = paramiko.Transport((server, port))
        transport.connect(username=user, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        for menu in html_menus:
            r = re.search('[^/]+.html$', menu)
            menu_name = r.group(0)
            remote_html_path = '{rb}/{c}{sc}/html/{m}'.format(rb=remote_base, c=course, sc=sub_course, m=menu_name)
            sftp.put(menu, remote_html_path)
            print(bcolors.WARNING + '{} Uploaded'.format(menu_name) + bcolors.ENDC)

        print(bcolors.FAIL + 'No HTML file' + bcolors.ENDC) if html_menus == [] else print('')

        sftp.close()
        transport.close()
    except:
        print(bcolors.FAIL + 'No HTML file' + bcolors.ENDC)
        raise


def upload_css(course, sub_course=None):
    try: 
        if sub_course is not None:
            sub_course = '/{}'.format(sub_course)
        else:
            sub_course = ''

        session = ftplib.FTP(server, user, password)
        session.cwd('{}/{}{}/css'.format(remote_base, course, sub_course))
        f = '{}/{}/resources{}/styles/css/concat/concat.css'.format(local_base, course, sub_course)
        local_file = copyfile(f, './concat.css')
        session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
        os.remove('./concat.css')
        session.quit()
        print(bcolors.WARNING + 'CSS Uploaded' + bcolors.ENDC)
    except (ftplib.error_perm, FileNotFoundError):
        print(bcolors.FAIL + 'No concat.css file' + bcolors.ENDC)


def upload_js(course, sub_course=None):
    try:
        if sub_course is not None:
            sub_course = '/{}'.format(sub_course)
        else:
            sub_course = ''

        session = ftplib.FTP(server, user, password)
        session.cwd('{}/{}{}/js'.format(remote_base, course, sub_course))
        f = '{}/{}/resources{}/js/concat/concat.js'.format(local_base, course, sub_course)
        local_file = copyfile(f, './concat.js')
        session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
        os.remove('./concat.js')
        session.quit()
        print(bcolors.WARNING + 'JS Uploaded' + bcolors.ENDC)
    except (ftplib.error_perm, FileNotFoundError):
        print(bcolors.FAIL + 'No concat.js file' + bcolors.ENDC)


def upload_html(course, sub_course=None):
    try:
        if sub_course is not None:
            sub_course = '/{}'.format(sub_course)
        else:
            sub_course = ''

        session = ftplib.FTP(server, user, password)
        session.cwd('{}/{}{}/html'.format(remote_base, course, sub_course))
        html_folder = '{}/{}/resources{}/html/*.html'.format(local_base, course, sub_course)
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


def upload_all(course, sub_course=None):
    upload_css(course, sub_course)
    upload_css_sftp(course, sub_course)
    upload_js(course, sub_course)
    upload_js_sftp(course, sub_course)
    upload_html(course, sub_course)
    upload_html_sftp(course, sub_course)
    print(bcolors.OKBLUE + 'DONE' + bcolors.ENDC)


if __name__ == '__main__':
    #upload_css('vatl')
    #upload_css_sftp('vatl')
    #upload_js('vatl')
    #upload_js_sftp('vatl')
    #upload_html('vatl')
    upload_html_sftp('vatl')

