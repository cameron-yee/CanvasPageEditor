import ftplib
from shutil import copyfile
import os
from glob import glob
from colors import bcolors
from auth import server, user, password, remote_base, local_base, aws_secret_access_key, aws_access_key_id, tinify_api_key

#sftp
import paramiko

#aws
import boto3

#tinypng api
import tinify

###Test web livereload functionality
#from selenium import webdriver
#from selenium.webdriver import ChromeOptions, Chrome

def upload_css_sftp(course, sub_course=None):
    try:
        port = 22

        if sub_course is not None:
            sub_course_local = 'courses/{}/'.format(sub_course)
            sub_course_remote = '/{}'.format(sub_course)
        else:
            sub_course = ''
            sub_course_local = ''
            sub_course_remote = ''

        local_css_path = '{lb}/{c}/{scl}resources/styles/css/concat/concat.css'.format(lb=local_base, c=course, scl=sub_course_local)
        remote_css_path = '{rb}/{c}{scr}/css/concat.css'.format(rb=remote_base, c=course, scr=sub_course_remote)

        transport = paramiko.Transport((server, port))
        transport.connect(username=user, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_css_path, remote_css_path)

        sftp.close()
        transport.close()
        print(bcolors.WARNING + 'CSS Uploaded via SFTP (OLD MEDIA)' + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No concat.css file' + bcolors.ENDC)


def upload_js_sftp(course, sub_course=None):
    try:
        port = 22

        if sub_course is not None:
            sub_course_local = 'courses/{}/'.format(sub_course)
            sub_course_remote = '/{}'.format(sub_course)
        else:
            sub_course = ''
            sub_course_local = ''
            sub_course_remote = ''

        local_js_path = '{lb}/{c}/{scl}resources/js/concat/concat.js'.format(lb=local_base, c=course, scl=sub_course_local)
        remote_js_path = '{rb}/{c}{scr}/js/concat.js'.format(rb=remote_base, c=course, scr=sub_course_remote)

        transport = paramiko.Transport((server, port))
        transport.connect(username=user, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_js_path, remote_js_path)

        sftp.close()
        transport.close()
        print(bcolors.WARNING + 'JS Uploaded via SFTP (OLD MEDIA)' + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No concat.js file' + bcolors.ENDC)


def upload_html_sftp(course, sub_course=None):
    try:
        port = 22

        if sub_course is not None:
            sub_course_local = 'courses/{}/'.format(sub_course)
            sub_course_remote = '/{}'.format(sub_course)
        else:
            sub_course = ''
            sub_course_local = ''
            sub_course_remote = ''

        html_folder = '{lb}/{c}/{scl}resources/html/*.html'.format(lb=local_base, c=course, scl=sub_course_local)
        html_menus = glob(html_folder)

        transport = paramiko.Transport((server, port))
        transport.connect(username=user, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        for menu in html_menus:
            menu_name = os.path.basename(menu)
            remote_html_path = '{rb}/{c}{scr}/html/{m}'.format(rb=remote_base, c=course, scr=sub_course_remote, m=menu_name)
            sftp.put(menu, remote_html_path)
            print(bcolors.WARNING + '{} Uploaded via SFTP (OLD MEDIA)'.format(menu_name) + bcolors.ENDC)

        print(bcolors.FAIL + 'No HTML file' + bcolors.ENDC) if html_menus == [] else print('')

        sftp.close()
        transport.close()
    except:
        print(bcolors.FAIL + 'No HTML file' + bcolors.ENDC)
        raise


def upload_html_aws(course, sub_course=None):
    try:
        if sub_course is not None:
            sub_course_local = 'courses/{}/'.format(sub_course)
        else:
            sub_course = ''
            sub_course_local = ''

        s3 = boto3.resource('s3')
        html_folder = '{lb}/{c}/{scl}resources/html/*.html'.format(lb=local_base, c=course, scl=sub_course_local)
        html_menus = glob(html_folder)

        for menu in html_menus:
            data = open(menu,'rb')
            menu_name = os.path.basename(menu)

            s3.Bucket('media-bscs-org').put_object(Key='canvas/{c}/{sc}/html/{m}'.format(c=course, sc=sub_course, m=menu_name), Body=data)
            data.close()
            print(bcolors.WARNING + '{}: HTML Uploaded to AWS'.format(menu_name) + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No HTML file' + bcolors.ENDC)
        raise


def upload_js_aws(course, sub_course=None):
    try:
        if sub_course is not None:
            sub_course_local = 'courses/{}/'.format(sub_course)
        else:
            sub_course = ''
            sub_course_local = ''


        local_js_path = '{lb}/{c}/{scl}resources/js/concat/concat.js'.format(lb=local_base, c=course, scl=sub_course_local)
        data = open(local_js_path, 'rb')

        s3 = boto3.resource('s3')
        s3.Bucket('media-bscs-org').put_object(Key='canvas/{c}/{sc}/js/concat.js'.format(c=course, sc=sub_course), Body=data)
        data.close()
        print(bcolors.WARNING + 'JS Uploaded to AWS' + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No JS file' + bcolors.ENDC)
        raise


def upload_js_aws(course, sub_course=None):
    try:
        if sub_course is not None:
            sub_course_local = 'courses/{}/'.format(sub_course)
        else:
            sub_course = ''
            sub_course_local = ''


        local_js_path = '{lb}/{c}/{scl}resources/js/concat/concat.js'.format(lb=local_base, c=course, scl=sub_course_local)
        data = open(local_js_path, 'rb')

        s3 = boto3.resource('s3')
        s3.Bucket('media-bscs-org').put_object(Key='canvas/{c}/{sc}/js/concat.js'.format(c=course, sc=sub_course), Body=data)
        data.close()
        print(bcolors.WARNING + 'JS Uploaded to AWS' + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No JS file' + bcolors.ENDC)
        raise


def upload_css_aws(course, sub_course=None):
    try:
        if sub_course is not None:
            sub_course_local = 'courses/{}/'.format(sub_course)
        else:
            sub_course = ''
            sub_course_local = ''


        local_css_path = '{lb}/{c}/{scl}resources/styles/css/concat/concat.css'.format(lb=local_base, c=course, scl=sub_course_local)
        data = open(local_css_path, 'rb')

        s3 = boto3.resource('s3')
        s3.Bucket('media-bscs-org').put_object(Key='canvas/{c}/{sc}/css/concat.css'.format(c=course, sc=sub_course), Body=data)
        data.close()
        print(bcolors.WARNING + 'CSS Uploaded to AWS' + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No CSS file' + bcolors.ENDC)
        raise


def upload_img_aws(img_path, course, folder, sub_course=None):
    image_name = os.path.basename(img_path)
    key = '/{c}/{sc}/{f}/{i}'.format(c=course,sc=sub_course,f=folder,i=image_name) if sub_course is not None else '/{c}/{f}/{i}'.format(c=course,f=folder,i=image_name)
    print(key)

    #tinify.key = tinify_api_key
    #unoptimized_img = tinify.from_file(img_path)
    #unoptimized_img.to_file('/Users/cyee/Downloads/astro_opt.jpg')
    
    s3 = boto3.resource('s3')
    #for bucket in s3.buckets.all():
    #    for key in bucket.objects.all():
    #        print(key.key)

    data = open(img_path, 'rb')
    #s3.Bucket('media-bscs-org').put_object(Key='astronaut.jpg', Body=data)
    s3.Bucket('media-bscs-org').put_object(Key=key, Body=data)

    data.close()
    print(bcolors.WARNING + 'IMG uploaded to AWS' + bcolors.ENDC)


def upload_all(course, sub_course=None):
    upload_css_sftp(course, sub_course)
    upload_css_aws(course, sub_course)
    upload_js_sftp(course, sub_course)
    upload_js_aws(course, sub_course)
    upload_html_sftp(course, sub_course)
    upload_html_aws(course, sub_course)
    print(bcolors.OKBLUE + 'DONE' + bcolors.ENDC)


if __name__ == '__main__':
    #upload_css('vatl')
    #upload_css_sftp('vatl')
    #upload_js('vatl')
    #upload_js_sftp('vatl')
    #upload_html('vatl')
    #upload_html_sftp('vatl')
    #upload_all('3dmss', 'pd')
    #refresh_chrome()
    #command_input()
    upload_img_aws('/Users/cyee/Downloads/astronaut.jpg','3dmss','images','se')
    #upload_css_aws('3dmss', 'se')













#def refresh_chrome():
#    browser = webdriver.Chrome()
#    browser.get('http://seleniumhq.org/')
#
#
#def command_input():
#    inp = input('Enter course: ')
#    upload_all(inp)
#    command_input()
#
#
#def stay_up():
#    while up == True:
#        pass




#def upload_css(course, sub_course=None):
#    try: 
#        if sub_course is not None:
#            sub_course_local = 'courses/{}/'.format(sub_course)
#            sub_course_remote = '/{}'.format(sub_course)
#        else:
#            sub_course = ''
#            sub_course_local = ''
#            sub_course_remote = ''
#
#        session = ftplib.FTP(server, user, password)
#        session.cwd('{rb}/{c}{scr}/css'.format(rb=remote_base, c=course, scr=sub_course_remote))
#        f = '{lb}/{c}/{scl}resources/styles/css/concat/concat.css'.format(lb=local_base, c=course, scl=sub_course_local)
#        local_file = copyfile(f, './concat.css')
#        session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
#        os.remove('./concat.css')
#        session.quit()
#        print(bcolors.WARNING + 'CSS Uploaded' + bcolors.ENDC)
#    except (ftplib.error_perm, FileNotFoundError):
#        print(bcolors.FAIL + 'No concat.css file' + bcolors.ENDC)


#def upload_js(course, sub_course=None):
#    try:
#        if sub_course is not None:
#            sub_course_local = 'courses/{}/'.format(sub_course)
#            sub_course_remote = '/{}'.format(sub_course)
#        else:
#            sub_course = ''
#            sub_course_local = ''
#            sub_course_remote = ''
#
#        session = ftplib.FTP(server, user, password)
#        session.cwd('{rb}/{c}{scr}/js'.format(rb=remote_base, c=course, scr=sub_course_remote))
#        f = '{lb}/{c}/{scl}resources/js/concat/concat.js'.format(lb=local_base, c=course, scl=sub_course_local)
#        local_file = copyfile(f, './concat.js')
#        session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
#        os.remove('./concat.js')
#        session.quit()
#        print(bcolors.WARNING + 'JS Uploaded' + bcolors.ENDC)
#    except (ftplib.error_perm, FileNotFoundError):
#        print(bcolors.FAIL + 'No concat.js file' + bcolors.ENDC)


#def upload_html(course, sub_course=None):
#    try:
#        if sub_course is not None:
#            sub_course_local = 'courses/{}/'.format(sub_course)
#            sub_course_remote = '/{}'.format(sub_course)
#        else:
#            sub_course = ''
#            sub_course_local = ''
#            sub_course_remote = ''
#
#        session = ftplib.FTP(server, user, password)
#        session.cwd('{rb}/{c}{scr}/html'.format(rb=remote_base, c=course, scr=sub_course_remote))
#
#        html_folder = '{lb}/{c}/{scl}resources/html/*.html'.format(lb=local_base, c=course, scl=sub_course_local)
#        html_menus = glob(html_folder)
#
#        for menu in html_menus:
#            r = re.search('[^/]+.html$', menu)
#            menu_name = r.group(0)
#            local_file = copyfile(menu, './{}'.format(menu_name))
#            session.storbinary('STOR {}'.format(local_file), open(local_file,'rb'))
#            os.remove('./{}'.format(menu_name))
#        session.quit()
#        print(bcolors.WARNING + 'HTML Uploaded to FTP' + bcolors.ENDC)
#    except (ftplib.error_perm, FileNotFoundError):
#        print(bcolors.FAIL + 'No HTML file' + bcolors.ENDC)
