__author__ = 'jpark3'

"""
 python2html function: Simply converts the string of the python_output (text editor) to a HTML format.
                       It assumes that the python_output is formatted.
                       Ex) If a user press 'enter', the python script should have inserted '\n' to the string
"""

def python2html(pyout):

    start_tag= '<html>\n\t<body>\n\t\t<p>'
    end_tag='</p>\n\t</body>\n</html>'
    html= start_tag + pyout + end_tag

    fout=open('output.html','w')
    fout.write(html)
    fout.close()

    return html

# Example code for python2html function
def example():
    in1='When you eat 3 cookies [parent variable, class identifier, param_start, param_end, function]' \
        ' you consume 150 [child variable,  class identifier] calories.'

    print python2html(in1)

example()

