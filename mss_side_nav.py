import re

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

            span_pattern = '<span class="middle-school-science"></span>'
            new_span =  '<span class="page-title"></span>\n<span id="side-menu-selector" class="Middle School Science"></span>'
            final = re.sub(span_pattern, new_span, nnc)

            f.write(final)
            f.close()


if __name__ == '__main__':
    replace('test.html')
