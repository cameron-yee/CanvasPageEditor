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



## Usage

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

The &lt;path-to-watch-folder&gt; is the file directory that stores the html files for the canvas course.  In order for this to work, the files MUST have the url and courses tags at the top of the files.  The program will continue to run if a file is missing the tag, but Canvas will not be updated on file save and the browser will not be updated.

TODO: Eventually this should support both Firefox and Safari at a minimum.


