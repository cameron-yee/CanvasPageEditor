"use strict"

const gulp = require('gulp');
const run = require('gulp-run');

//Doesn't work with relative path, file.path is undefined
const html_files = 'FULL_PATH_TO_HTML_FILES';

gulp.task('watch',
    () => {
        gulp
            .watch(html_files) 
            .on("change", (file) => {
                const capi = `python3 ~/Documents/CanvasPageEditor/canvas_page_editor.py ind ${file}`;
                return run(capi).exec();
            });
    }
);
