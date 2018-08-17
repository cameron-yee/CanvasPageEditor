# CAPI

## Installation/Set up

1. Clone repository into a local folder

```bash
$ git clone https://github.com/cameron-yee/CanvasPageEditor.git
```

2. Set alias for CLI functionality in ~/.bash&UnderBar;profile or ~/.bashrc

```
alias capi=python3 canvas_page_editor.py
```

NOTE: Make sure that Python3 is installed

3. Setup auth.py file for sensitive information
    * Create string variables in auth.py:
    **To use Canvas LMS API**
        TODO: Canvas LMS requires OAuth2 authentication.  This has not been set up yet.
        * token: developer key for Canvas LMS
    **For media server functions:**
        * aws_access_key_id: login id to access AWS media server through SFTP
        * aws_secret_access_key: login key to access AWS media server through SFTP
        * tinify_api_key: API key to interact with TinyPNG/TinyJPG API (No official functionality yet in CAPI)
        * server: media server address
        * user: media server username
        * password: media server password
        * remote_base: current directory for interacting with media server after SFTP or FTP connection
        * local_base: path to local files for media server upload
        * email: email to login to Canvas LMS
        * canvas_password: password to login to Canvas LMS

     **For Chrome livereload:**
        * google_email: email to login to Google account
        * google_passowrd: password to login to Google account

4. Before use, create a virtual environment in the top directory of the repository (or use Pipenv or Docker).

```bash
$ virtualenv venv
$ source venv/bin/activate
```

5. Install requirements

```bash
$ pip3 install -r requirements.txt
```

## Canvas API usage

For html files that are to be uploaded to Canvas, put the following tag at the top of the file:

```html
<span url="<PAGE URL in CANVAS>" courses="<COURSE IDs THAT PAGE BELONGS TO>"></span>

<!-- EXAMPLE -->
<span url="test-page" courses="12, 35"></span>
```

In Terminal, navigate to the CAPI local repository.  Some possible uses:

Update entire course with the content from local html files
```bash
$ capi uc /path/to/html_files_folder
```

Update individual page
```bash
$ capi ind /path/of/html_file
```

Update course name
```bash
$ capi uc --name <new-course-page> <course-id>
```

NOTE: It is also possible to use CAPI without adding the url and courses tag to the top of the file.  If doing so, the course id must be included as a CLI argument.

There are many other possibilities.  All available option can be seen by using the --help flag.

```bash
$ capi --help
$ capi uc -h
```

## Usage with gulp.js

1. Install the latest version of NodeJS and gulp.js
2. Place gulpfile.js in folder above html files.  Edit the path to the html files in the gulpfile.js file.
3. In terminal, navigate to the folder that contains the gulpfile.js file.
4. Run

```bash
$ gulp watch
```

5. Open a html file in the directory that gulp is watching and save it.  Terminal will output the normal capi ind print statements if setup right.

NOTE: This will only work if the html files contain both the url and courses tag at the top of the files.

## Chrome livereload

1. Download ChromeDriver (NOT the browser) here: <https://sites.google.com/a/chromium.org/chromedriver/downloads>
2. In auth.py, add variables for: email, password, google&UnderBar;email, google&UnderBar;password.  All four variable values should be stored as strings.  The values are:
    * email: email used to login to Canvas
    * password: password used to login to Canvas
    * google&UnderBar;email: email used to login to Google account
    * google&UnderBar;password: password used to login to Google account
3. OPTIONAL: Add chrome extensions to Chrome on startup.
    * Download extension .crx file from: <https://chrome-extension-downloader.com/>
    * Place .crx file in ./extensions directory

To use livereload run:

```bash
$ capi chrome <path-to-watch-folder>
```

Now, when an event is detected in the watched folder, the file that triggered the event will be passed to updateIndividualPage() to be updated in Canvas, and the browser will navigate to the file page on Canvas.

The &lt;path-to-watch-folder&gt; is the file directory that stores the html files for the canvas course.  In order for this to work, the files MUST have the url and courses tags at the top of the files.  The program will continue to run if a file is missing the tag, but Canvas will not be updated on file save and the browser will not be updated.

TODO: Eventually this should support both Firefox and Safari at a minimum.

## Media Server Usage

```bash
$ capi static --html <directory> -sc <subcourse_directory>
$ capi static --css <directory> -sc <subcourse_directory>
$ capi static --js <directory> -sc <subcourse_directory>
```

See source code to see how directories are expected to be organized.  This functionality is highly specified for our specific use.
Although not included in this repository, it is possible to run this as a gulp task after minifying css/js files.

Useful Documentation:

[File event watching](https://pythonhosted.org/watchdog/)
[Webdriver capabilities](https://selenium-python.readthedocs.io/)
[Amazon S3 with python](https://boto3.readthedocs.io/en/latest/guide/s3-example-creating-buckets.html)
[CLI functionality](https://docs.python.org/3/library/argparse.html)

