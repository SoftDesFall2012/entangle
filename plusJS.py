__author__ = 'Nathan'

def tanglekit(imput):
    body = imput
    head = "<script type="text/javascript" src="Tangle.js"></script><link rel="stylesheet" href="TangleKit/TangleKit.css" type="text/css">
    <script type="text/javascript" src="TangleKit/mootools.js"></script>
    <script type="text/javascript" src="TangleKit/sprintf.js"></script>
    <script type="text/javascript" src="TangleKit/BVTouchable.js"></script>
    <script type="text/javascript" src="TangleKit/TangleKit.js"></script>"
    append = head + body
    return append

