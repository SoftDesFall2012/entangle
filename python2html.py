__author__ = 'jpark3'


# python2html function: Simply converts the string of the python_output (text editor made in Tkinter) to a HTML format.

def python2html(pyout):

    output = pyout.replace("\n", "<br \>")  # add a break to a new line

    start_tag= '<body>\n\t\t<p>' # start html body
    end_tag='</p>\n</body>' #end html body

    html= start_tag + output + end_tag # combine everything in string

    fout=open('output.html','w') #save it in a html format
    fout.write(html)
    fout.close()

    return html

# Example code for python2html function
def example():
    in1="When you eat 3 cookies {'variable': '\"cookies\"', 'class': '\"TKAdjustableNumber\"', 'mini': '\"1\"', 'maxi': '\"100\"'} \n" \
         "you consume 150 calories."

    print python2html(in1)
'''
# Original in1
    in1='When you eat 3 cookies [parent variable, class identifier, param_start, param_end, function]\n'\
        ' you consume 150 [child variable,  class identifier] calories.'
'''



example()

