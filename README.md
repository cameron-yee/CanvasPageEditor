# CAPI

## Installation/Set up

1. Clone repository into a local folder

```bash
$ git clone https://github.com/cameron-yee/CanvasPageEditor.git
```

2. Set alias for CLI functionality in ~/.bash_profile or ~/.bashrc

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
