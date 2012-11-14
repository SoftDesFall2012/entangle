__author__ = 'jpark3'

"""
 python2html function: Simply converts the string of the python_output (text editor made in Tkinter) to a HTML format.

"""

def python2html(pyout):
    '''
        for a in pyout:
            if a == '\':
                print 'hello'


        start_tag= '<html>\n\t<body>\n\t\t<p>'
        end_tag='</p>\n\t</body>\n</html>'

        html= start_tag + pyout + end_tag
    '''

    output = pyout.replace("\n", "<br \>")
    return output

'''
    fout=open('output.html','w')
    fout.write(html)
    fout.close()

    return html
'''
# Example code for python2html function
def example():
    in1='When you eat 3 cookies [parent variable, class identifier, param_start, param_end, function]\n' \
        ' you consume 150 [child variable,  class identifier] calories.'

    print python2html(in1)

example()

