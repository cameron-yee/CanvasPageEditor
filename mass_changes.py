#!/usr/local/bin/python3
import re
from canvas_page_editor import *
from glob import glob
from colors import bcolors
import os

#def replace(filename):
#    with open(filename, 'r') as f:
#        contents = f.read()
#        f.close()
#
#        with open(filename, 'w') as f:
#            #id_pattern = '<div class="col-xs-12 col-lg-10">'
#            #new_id = '<div id="mss-content" class="col-xs-12 col-md-9 col-lg-10">'
#            #nc = re.sub(id_pattern, new_id, contents)
#
#            side_nav_pattern = '(<!-- Course\s*[\s\S]*?(?=\n.*?<!--|$))'
#            side_nav = ''
#            nc = re.sub(side_nav_pattern, side_nav, contents)
#
#            side_nav_pattern = '(<!-- Side\s*[\s\S]*?(?=\n.*?<!--|$))'
#            side_nav = '<!-- Side Navigation -->\n\t<div class="col-xs-12 col-md-3 col-lg-2">\n\t\t<div id="side-menu"></div>\n\t</div>\n\t<!-- Course Navigation -->\n\t<div id="course-menu" class="col-xs-12 col-md-3 col-lg-2" style="display: none;">\n\t\t<div class="course-menu"></div>\n\t</div>\n'
#
#            final = re.sub(side_nav_pattern, side_nav, nc)
#
#            #span_pattern = 'class="Middle School Science"'
#            #new_span =  'class="Science and Society"'
#            #final = re.sub(span_pattern, new_span, nnc)
#
#            #print(side_nav)
#            f.write(final)
#            f.close()
#
#
#def updateAllFiles(top_directory):
#    folders = getHtmlFolders(top_directory)
#    file_paths = []
#    
#    for f in folders:
#        files = globHtml(f)
#        for paths in files:
#            for file_path in paths:
#                m = re.search('\d[\d.]+[^/].html$', file_path)
#                file_paths.append(file_path)
#                print('Updating: {}'.format(m))
#                replace(file_path)
#    return file_paths
#
#
#def prefixFiles(file_paths):
#    for f in file_paths:
#        pattern = '\d+$'
#        m = re.search('(\d[\d.]+)_SS_([^/]+.html)$', f)
#        if m is not None:
#            new_name = m.group(1) + '_ss_ch_4_' + m.group(2)
#            new_file_path = re.sub('\d[^/]+.html$', new_name, f)
#            os.rename(f, new_file_path)
#            print(new_file_path)
#
#
#########################################
#    #MNSTeLLA Functions
#########################################
#
#
#def getFolders(top_directory):
#    segment_folder_names = os.listdir(top_directory)
#    sf_paths = []
#    for name in segment_folder_names:
#        sf_paths.append(top_directory + '/' + name)
#
#    sf_paths.sort()
#    return sf_paths
#
#
#def getFolderFiles(directory):
#    files = glob(directory + '{}'.format('/*.html'))
#    return files
#
#
##def getSegNum(path):
##    pat = '\d+$'
##    m = re.search(pat, path)
##    seg_num = m.group(0)
##    return seg_num
#
#
##Returns order in directory of file (ex. 01_welcome would return 1
##def getPageNum(f):
##    fname = f.split('/')[-1]
##    pat = '^\d{2}'
##    m = re.search(pat,fname)
##    page_num = m.group(0)
##    if page_num[0] == '0':
##        page_num = page_num[1]
##    return page_num
##
##
##def getPrefix(f, seg_num):
##    page_num = getPageNum(f)
##    prefix = '{}'.format('_') + seg_num + '{}'.format('_dot_') + page_num
##    return prefix
#
#
#def addTEContent(filepath):
#    with open(filepath, 'r') as f:
#        raw_contents = f.read()
#        f.close()
#
#        contents = '\t\t\t\t\t\t'.join(raw_contents.splitlines(True))
#
#        with open(filepath, 'w') as f:
#            span_pattern = '<span class="remove-page-title"></span>'
#            add_to_top = '<a href="#" class="btn btn-primary student-toggle" role="button">\n\tParticipant View\n\t<span class="screenreader-only">Toggle Participant View</span>\n</a>\n<a href="#" class="btn btn-primary teacher-toggle" role="button">\n\tFacilitator View\n\t<span class="screenreader-only">Toggle Facilitator View</span>\n</a>\n\n<span class="remove-page-title"></span>\n\n<!--Student View-->\n<div class="grid-row teacher-wrap-around-top-margin-adjust">\n\t<div id="student-view" class="col-xs-12 col-lg-6">\n\t\t<div class="***REMOVED***-accordion ***REMOVED***-student-accordion" aria-multiselectable="false">\n\t\t\t<div class="***REMOVED***-accordion-section">\n\t\t\t\t<a id="student-view-heading" class="***REMOVED***-accordion-section-title active-accordion" aria-expanded="true" href="#***REMOVED***-accordion-0">Participant View</a>\n\t\t\t\t<div id="***REMOVED***-accordion-0" class="***REMOVED***-accordion-section-content-wrapper open">\n\t\t\t\t\t<div class="***REMOVED***-accordion-section-content">'
#
#            add_to_bottom = '\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n\n\t<!--Teacher Content-->\n\t<div class="col-xs-12 col-lg-6">\n\t\t<div class="***REMOVED***-accordion" aria-multiselectable="false">\n\t\t\t<div class="***REMOVED***-accordion-section">\n\t\t\t\t<a class="***REMOVED***-accordion-section-title active-accordion" href="#***REMOVED***-accordion-1" aria-expanded="true">Action</a>\n\t\t\t\t<div id="***REMOVED***-accordion-1" class="***REMOVED***-accordion-section-content-wrapper open">\n\t\t\t\t\t<div class="***REMOVED***-accordion-section-content">\n\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n</div>'
#
#            nc = re.sub(span_pattern, add_to_top, contents)
#            #nc = contents.replace(span_pattern, add_to_top, 1)
#            f.write(nc + add_to_bottom)
#            f.close()
#
#       # with open(filepath, 'a') as f:
#       #     add_to_bottom = '\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t<div>\n\n\t<!--Teacher Content-->\n\t<div class="col-xs-12 col-lg-6">\n\t\t<div class="***REMOVED***-accordion" aria-multiselectable="false">\n\t\t\t<div class="***REMOVED***-accordion-section">\n\t\t\t\t<a class="***REMOVED***-accordion-section-title active-accordion" href="#***REMOVED***-accordion-1" aria-expanded="true">Action</a>\n\t\t\t\t<div id="***REMOVED***-accordion-1" class="***REMOVED***-accordion-section-content-wrapper open">\n\t\t\t\t\t<div class="***REMOVED***-accordion-section-content">\n\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n</div>'
#       #     f.write(add_to_bottom)
#       #     f.close()
#
#
#def rename(sf_paths):
#    for path in sf_paths:
#        files = getFolderFiles(path)
#        seg_num = getSegNum(path)
#        for f in files:
#            page_num = getPageNum(f)
#            prefix = getPrefix(f, seg_num)
#
#            fname = f.split('/')[-1]
#            #pattern for full name of file
#            pat = '(^\d{2})(_[^/]+.html$)'
#            m = re.search(pat, fname)
#            new_name = m.group(1) + prefix + m.group(2)
#            new_path = os.path.dirname(f) + '{}'.format('/') + new_name
#
#            addTEContent(f)
#            os.rename(f,new_path)
#            print(bcolors.WARNING + 'UPDATED: ' + bcolors.ENDC + bcolors.OKBLUE + new_name + bcolors.ENDC)



############################################
    #READY FOR MNSTLLA COURSE 2 FE TRANSFER
############################################


#Seaperch change
def getFolderFiles(directory):
    files = glob(directory + '{}'.format('/*.html'))
    return files


def getFolders(top_directory):
    segment_folder_names = os.listdir(top_directory)
    sf_paths = []
    for name in segment_folder_names:
        sf_paths.append(top_directory + '/' + name)

    sf_paths.sort()
    return sf_paths


def addTEContent(filepath):
    with open(filepath, 'r') as f:
        raw_contents = f.read()

        rpt_pattern = '<span class="remove-page-title"></span>\n'
        remove = ''
        contents = re.sub(rpt_pattern, remove, raw_contents)

        nc = '\t\t\t\t\t\t\t'.join(contents.splitlines(True))

        #(<!-- Course\s*[\s\S]*?(?=\n.*?<!--|$))
        side_menu_pattern = '(<div class="content-box">[\S\s]*?(?=(\n*?<div class="col-xs-12 col-md-9 col-lg-10 main-content-section">)))'
        m = re.search(side_menu_pattern, nc)
        ncc = re.sub(side_menu_pattern, remove, nc)
        pat = str(m.group(2))
        nccc = re.sub(pat, remove, ncc)

        span_pattern = '<span url="[^\n]+"></span>'
        r = re.search(span_pattern, nccc)
        m = str(r.group(0))
        full_data = re.sub('">','" courses="11">', m)
        f.close()

        with open(filepath, 'w') as f:
            add_to_top = '<span class="remove-page-title"></span>\n{}\n\n<div class="grid-row">\n\t<div class="col-xs-5 off-xs-7 col-lg-4 off-lg-8">\n\t\t<a href="#" class="btn btn-primary student-toggle" role="button">\n\t\t\tSwitch to Student View\n\t\t\t<span class="screenreader-only">Toggle Student View</span>\n\t\t</a>\n\t\t<a href="#" class="btn btn-primary teacher-toggle" role="button">\n\t\t\tSwitch to Teacher View\n\t\t\t<span class="screenreader-only">Toggle Teacher View</span>\n\t\t</a>\n\t</div>\n</div>\n\n<div class="content-box">\n\t<div class="grid-row">\n\t\t<div class="col-xs-12 col-lg-2">\n\t\t\t<div class="side-menu"></div>\n\t\t</div>\n\n\t\t<div class="col-xs-12 col-lg-10">\n\n\t\t\t<!--Student View-->\n\t\t\t<div class="grid-row">\n\t\t\t\t<div id="student-view" class="col-xs-12 col-lg-6">\n\t\t\t\t\t<div class="bscs-accordion bscs-student-accordion" aria-multiselectable="false">\n\t\t\t\t\t\t<div class="bscs-accordion-section">\n\t\t\t\t\t\t\t<a id="student-view-heading" class="bscs-accordion-section-title active-accordion" href="#bscs-accordion-1" aria-expanded="true">Student View</a>\n\t\t\t\t\t\t\t<div id="bscs-accordion-1" class="bscs-accordion-section-content-wrapper open">\n\t\t\t\t\t\t\t\t<div class="bscs-accordion-section-content">\n\t\t\t\t\t\t\t\t\t<div class="col-xs-12 main-content-section">\n'.format(full_data)

            add_to_bottom = '\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\n\t\t\t\t<!--Teacher Content-->\n\t\t\t\t<div class="col-xs-12 col-lg-6">\n\t\t\t\t\t<div class="bscs-accordion" aria-multiselectable="false">\n\t\t\t\t\t\t<div class="bscs-accordion-section">\n\t\t\t\t\t\t\t<a class="bscs-accordion-section-title active-accordion" href="#bscs-accordion-3" aria-expanded="false">Where are we in the storyline?</a>\n\t\t\t\t\t\t\t<div id="bscs-accordion-3" class="bscs-accordion-section-content-wrapper closed">\n\t\t\t\t\t\t\t\t<div class="bscs-accordion-section-content">\n\t\t\t\t\t\t\t\t\tComing Soon\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class="bscs-accordion" aria-multiselectable="false">\n\t\t\t\t\t\t<div class="bscs-accordion-section">\n\t\t\t\t\t\t\t<a class="bscs-accordion-section-title active-accordion" href="#bscs-accordion-4" aria-expanded="false">Phenomenon for this lesson</a>\n\t\t\t\t\t\t\t<div id="bscs-accordion-4" class="bscs-accordion-section-content-wrapper closed">\n\t\t\t\t\t\t\t\t<div class="bscs-accordion-section-content">\n\t\t\t\t\t\t\t\t\tComing Soon\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class="bscs-accordion" aria-multiselectable="false">\n\t\t\t\t\t\t<div class="bscs-accordion-section">\n\t\t\t\t\t\t\t<a class="bscs-accordion-section-title active-accordion" href="#bscs-accordion-5" aria-expanded="false">Main Learning Goal</a>\n\t\t\t\t\t\t\t<div id="bscs-accordion-5" class="bscs-accordion-section-content-wrapper closed">\n\t\t\t\t\t\t\t\t<div class="bscs-accordion-section-content">\n\t\t\t\t\t\t\t\t\tComing Soon\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\n\t\t\t\t\t<div class="bscs-accordion" aria-multiselectable="false">\n\t\t\t\t\t\t<div class="bscs-accordion-section">\n\t\t\t\t\t\t\t<a class="bscs-accordion-section-title active-accordion" href="#bscs-accordion-6" aria-expanded="false">Teacher Moves During Lesson</a>\n\t\t\t\t\t\t\t<div id="bscs-accordion-6" class="bscs-accordion-section-content-wrapper closed">\n\t\t\t\t\t\t\t\t<div class="bscs-accordion-section-content">\n\t\t\t\t\t\t\t\t\tComing Soon\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n</div>'

            ncccc = re.sub(span_pattern, add_to_top, nccc)
            #nc = contents.replace(span_pattern, add_to_top, 1)
            f.write(ncccc + add_to_bottom)
            ##f.write(r.group(0) + nc + add_to_bottom)
            f.close()


if __name__ == '__main__':
    #updateAllFiles('/Users/cyee/Documents/canvas/courses/mss/courses/student_edition/html/04_science_and_society')
    sf_paths = getFolders('/Users/cyee/Documents/canvas/courses/3dmss/courses/te/course/04_tog')
    for path in sf_paths:
        files = getFolderFiles(path)
        for f in files:
            addTEContent(f)

            print(bcolors.WARNING + 'UPDATED: ' + bcolors.ENDC + bcolors.OKBLUE + path + bcolors.ENDC)
    




       # with open(filepath, 'a') as f:
#       #     add_to_bottom = '\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t<div>\n\n\t<!--Teacher Content-->\n\t<div class="col-xs-12 col-lg-6">\n\t\t<div class="bscs-accordion" aria-multiselectable="false">\n\t\t\t<div class="bscs-accordion-section">\n\t\t\t\t<a class="bscs-accordion-section-title active-accordion" href="#bscs-accordion-1" aria-expanded="true">Action</a>\n\t\t\t\t<div id="bscs-accordion-1" class="bscs-accordion-section-content-wrapper open">\n\t\t\t\t\t<div class="bscs-accordion-section-content">\n\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t</div>\n</div>'
#       #     f.write(add_to_bottom)
#       #     f.close()
#
#            #span_pattern = '<span class="remove-page-title"></span>\n\n'
#            #remove = ''
#
#            #nc = re.sub(span_pattern, remove, contents)
#            #f.write(nc)
#            #f.close()

