import re
from canvas_page_editor import *
import os

def replace(filename):
    with open(filename, 'r') as f:
        contents = f.read()
        f.close()

        with open(filename, 'w') as f:
            id_pattern = '<div class="col-xs-12 col-lg-10">'
            new_id = '<div id="mss-content" class="col-xs-12 col-md-9 col-lg-10">'
            nc = re.sub(id_pattern, new_id, contents)

            side_nav_pattern = '(<!-- Side\s*[\s\S]*?(?=\n.*?<!--|$))'
            side_nav = '<!-- Side Navigation -->\n\t<div class="col-xs-12 col-md-3 col-lg-2">\n\t\t<div id="side-menu"></div>\n\t</div>\n\n\t<!-- Course Navigation -->\n\t<div id="course-menu" class="col-xs-12 col-md-3 col-lg-2" style="display: none;">\n\t\t<div class="course-menu"></div>\n\t</div>'
            nnc = re.sub(side_nav_pattern, side_nav, nc)

            span_pattern = 'class="Middle School Science"'
            new_span =  'class="Science and Society"'
            final = re.sub(span_pattern, new_span, nnc)

            print(final)
            f.write(final)
            f.close()


def updateAllFiles(top_directory):
    folders = getHtmlFolders(top_directory)
    file_paths = []
    
    for f in folders:
        files = globHtml(f)
        for paths in files:
            for file_path in paths:
                m = re.search('\d[\d.]+[^/].html$', file_path)
                file_paths.append(file_path)
                print('Updating: {}'.format(m))
                replace(file_path)
    return file_paths


def prefixFiles(file_paths):
    for f in file_paths:
        m = re.search('(\d[\d.]+)_SS_([^/]+.html)$', f)
        if m is not None:
            new_name = m.group(1) + '_ss_ch_4_' + m.group(2)
            new_file_path = re.sub('\d[^/]+.html$', new_name, f)
            os.rename(f, new_file_path)
            print(new_file_path)


if __name__ == '__main__':
    updateAllFiles('/Users/cameronyee/Desktop/canvas/courses/mss/courses/student_edition/html/04_science_and_society')
    




