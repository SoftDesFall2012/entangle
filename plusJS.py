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

    header = open('header.txt').read()

    strpheader = header.rstrip('/script>')
    strpheader = header.rstrip('<')

    finalheader = strpheader+

    <script type="text/javascript">

    function setUpTangle () {

        var element = document.getElementById("example");

    var tangle = new Tangle(element, {
        initialize: function () {
        this.cookies = 4;
    this.caloriesPerCookie = 50;
    },
    update: function () {
        this.calories = this.cookies * this.caloriesPerCookie;
    }
    });
    }

# Assembly of output

start_tag= '<html>\n\t\t<header>' # Start html body
end_header = '\n</header>\n'
end_tag='\n</html>' # End html body

output = start_tag + headerInjector(python2html_output) + end_header + bodyInjector(python2html_output) + end_tag

fout=open('outputjs.html','w') # Save it in a html format
fout.write(output)
fout.close()

print output

