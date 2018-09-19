#!/usr/local/bin/python3
from glob import glob
import sys
import auth

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from canvas_page_editor import updateIndividualPage

#Chrome functions EXPERIMENTAL
#browser = None
#chromeUp = False


def setExtensions():
    chrome_options = webdriver.ChromeOptions()
    ext_dir = './extensions'
    ext_files = glob(ext_dir + '/*.crx')

    for f in ext_files:
        chrome_options.add_extension(f)

    return chrome_options


def startChrome():
    try:
        auth.browser = webdriver.Chrome(chrome_options=setExtensions())
        auth.browser.get('https://www.google.com')
        sign_in = auth.browser.find_element_by_id('gb_70').click()
        sign_in_email = auth.browser.find_element_by_name('identifier').send_keys(auth.google_email + Keys.RETURN)
        time.sleep(1)
        sign_in_password = auth.browser.find_element_by_name('password').send_keys(auth.google_password + Keys.RETURN)
        time.sleep()

        auth.browser.get('https://bscs.instructure.com/courses')
        email_input = auth.browser.find_element_by_id('pseudonym_session_unique_id')
        email_input.send_keys(auth.email)
        password_input = auth.browser.find_element_by_id('pseudonym_session_password')
        password_input.send_keys(auth.canvas_password + Keys.RETURN)

        auth.chromeUp = True
    except Exception as e:
        #global auth.browser
        #auth.browser.close()
        print(e)
        sys.exit()


def refreshPage(course_id, url):
    #global auth.browser
    auth.browser.get('https://bscs.instructure.com/courses/{cid}/pages/{url}'.format(cid=course_id, url=url))


class MySyncHandler(FileSystemEventHandler):

    def on_modified(self, event):
        filename = event.src_path
        updateIndividualPage(None, auth.headers, filename)


## main loop
def watch(watchpath):
    observer = Observer()
    observer.schedule(MySyncHandler(), watchpath, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
#END CHROME

