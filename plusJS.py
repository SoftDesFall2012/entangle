__author__ = 'Nathan'

from string import *
from HTMLParser import *
import re

python2html_output = open('output.html').read()

def bodyInjector(python2html_output):

    ## Re-encode from byte to UTF-8 to make the string manipulateable ##
    python2html_outpututf8 = python2html_output.encode("UTF-8")

    ## Seperate injectable areas from rest of string ##
    forwards = python2html_output.split("{")
    backwards = python2html_output.split("}")

    front = forwards[0] # String up until injection point
    back = backwards[1] # String after injection point

    middle = forwards[1].split("}")

    inject = middle[0]  # Inject point with no curly braces on either end

    ## Properly format jsInject ##

    inject = "{" + inject + "}" # Adds curly braces to either end
    inject.replace('"', '\"')   # Makes sure double quotes are formatted properly
    jsInject = eval(inject)     # Converts str to dict

    ## Injection ##
    jsInjected = '<span data-var={variable} class ={class} data-min={mini} data-max ={maxi}>'.format(**jsInject)

    ## Re-composition ##

    bodyoutput = front + jsInjected + back
    bodyoutput = str (bodyoutput)

    return bodyoutput

def headerInjector(python2html_output):
    header = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> \n' \
    '<title>Tangle document</title> \n' \
    '<script type="text/javascript" src="Tangle.js"></script> \n' \
    '<link rel="stylesheet" href="TangleKit/TangleKit.css" type="text/css"> \n' \
    '<script type="text/javascript" src="TangleKit/mootools.js"></script> \n' \
    '<script type="text/javascript" src="TangleKit/sprintf.js"></script> \n' \
    '<script type="text/javascript" src="TangleKit/BVTouchable.js"></script> \n' \
    '<script type="text/javascript" src="TangleKit/TangleKit.js"></script> \n' \
    '<script type="text/javascript"> \n' \
    'function setUpTangle () { \n' \
    'var element = document.getElementById("example"); \n' \
    'var tangle = new Tangle(element, { \n' \
    'initialize: function () { \n' \
    'this.cookies = 4; \n' \
    'this.caloriesPerCookie = 50;\n' \
    '}, \n' \
    'update: function () { \n' \
    'this.calories = this.cookies * this.caloriesPerCookie; \n' \
    '} \n' \
    '}); \n' \
    '} \n' \
    '</script>'

    return header


start_tag= '<html>\n\t\t<header>' # start html body
end_header = '<\n<\header>'
end_tag='\n</html>' #end html body

output = start_tag + headerInjector(python2html_output) + end_header + bodyInjector(python2html_output) + end_tag

fout=open('outputjs.html','w') #save it in a html format
fout.write(output)
fout.close()

print output


'''


#print python2html_outpututf8.format('<span data-var="cookies" class = "TKAdjustableNumber" data-min="1" data-max = "100">')

#print python2html_outpututf8



class HTMLParse(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
    def handle_endtag(self, tag):
        print "End tag:", tag
    def handle_data(self, data):
        print "Data:", data


parse  = HTMLParse()
#parse.feed(python2html_output.read())
parse.handle_data(python2html_output.read())


class jsInjection(filename)

    def tanglekit(imput):
        body = imput
        head = "<script type="text/javascript" src="Tangle.js"></script><link rel="stylesheet" href="TangleKit/TangleKit.css" type="text/css">
        <script type="text/javascript" src="TangleKit/mootools.js"></script>
        <script type="text/javascript" src="TangleKit/sprintf.js"></script>
        <script type="text/javascript" src="TangleKit/BVTouchable.js"></script>
        <script type="text/javascript" src="TangleKit/TangleKit.js"></script>"
        append = head + body
        return append

'''