__author__ = 'Nathan'

from HTMLParser import *

python2html_output = open('output.html')

print(python2html_output)

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

'''
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