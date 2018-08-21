#!/usr/local/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from auth import email, canvas_password, google_password, google_email
import os, zipfile
from glob import glob

#extensions_folder = '/Users/cyee/Library/Application Support/Google/Chrome/Default/Extensions'
#ext_dir = '/Users/cyee/Downloads/dark'
#ext_file = '/Users/cyee/Downloads/mydark.zip'
#
#file_names = os.listdir(ext_dir)
#file_dict = {}
#for fn in file_names:
#    with open(os.path.join(ext_dir, fn), 'r') as f:
#        file_dict[fn] = f.read()
#
#    with (zipfile.ZipFile(ext_file), 'w') as zf:
#        for fn, content in file_dict.items():
#            zf.writestr(fn, content)

chrome_options = webdriver.ChromeOptions()
ext_dir = './extensions'
ext_files = glob(ext_dir + '/*.crx')

for f in ext_files:
    chrome_options.add_extension(f)
browser = webdriver.Chrome(chrome_options=chrome_options)
isChromeUp = False


def startChrome():
    try:
        global browser
        body = browser.find_element_by_tag_name('body')

        browser.get('https://www.google.com')
        sign_in = browser.find_element_by_id('gb_70').click()
        sign_in_email = browser.find_element_by_name('identifier')
        sign_in_email.send_keys(google_email + Keys.RETURN)
        time.sleep(1)
        sign_in_password = browser.find_element_by_name('password')
        sign_in_password.send_keys(google_password + Keys.RETURN)

        time.sleep(1)

        browser.get('https://bscs.instructure.com/courses')
        email_input = browser.find_element_by_id('pseudonym_session_unique_id')
        email_input.send_keys(email)
        password_input = browser.find_element_by_id('pseudonym_session_password')
        password_input.send_keys(canvas_password + Keys.RETURN)

        isChromeUp = True
        while isChromeUp:
            time.sleep(86400)
            on = False
        browser.quit()
        print('Program has ran for a day.  Shutting down.')
    except KeyboardInterrupt:
        browser.quit()

#
#Called in updateIndividualPage() in update() on line 214 of canvas_page_editor.py
#
def refreshPage(course_id, url):
    browser.get('https://bscs.instructure.com/courses/{cid}/pages/{url}'.format(cid=course_id, url=url))
    #email_input = browser.find_element_by_id('pseudonym_session_unique_id')
    #email_input.send_keys(email)
    #password_input = browser.find_element_by_id('pseudonym_session_password')
    #password_input.send_keys(canvas_password + Keys.RETURN)


if __name__ == '__main__':
    startChrome()
