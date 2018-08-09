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

There are many other possibilities.  All available option can be seen by using the --help flag.

```bash
$ capi --help
$ capi uc -h
```
