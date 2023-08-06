#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import cgitb; cgitb.enable()
import cgi

import os
import sys
import json
import glob

from datetime import datetime as dt

HTML = '''
<html>
 <head>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
 <title>  </title>
 </head>
 <body>
 <center>

 <h1> csv2graph2web </h1>
  <font size="2"><a href="https://github.com/mastnk/csv2graph2web">Powered by csv2graph2web</a> </font>
 <hr />

{main}

 </center>
 </body>
</html>
'''

def save_image( dirname, filename, file ):
    dirname = 'graphs/' + dirname
    if( not os.path.exists( dirname ) ):
        os.mkdir( dirname )
    os.chmod( dirname, 0o777 )

    filename = os.path.join( dirname, filename )
    with open( filename, 'wb' ) as fout:
        while( True ):
            chunk = file.read(100000)
            if( not chunk ): break
            fout.write( chunk )
    os.chmod( filename, 0o777 )

    res = {'dirname': dirname, 'filename': filename, 'res': 'OK' }
    print("Content-Type: application/json; charset=UTF-8")
    print("")
    print(json.dumps(res))
    sys.exit()

form = cgi.FieldStorage()

try:
    form_file = form['file'].file
except:
    form_file = None

try:
    form_filename = form['filename'].value
except:
    form_filename = None

try:
    form_dirname = form['dirname'].value
except:
    form_dirname = None

main = ''
if( form_file is not None and
    form_filename is not None and
    form_dirname is not None ):
        save_image( form_dirname, form_filename, form_file )

elif( form_dirname is not None ):
    main += '<H2>{}</H2>\n'.format( form_dirname )
    main += '<a href="cgw.cgi">Back to index</a><br />\n'
    li = [ 'graphs', form_dirname, '*' ]
    files = sorted(glob.glob( os.path.join( *li ) ))
    for file in files:
        main += '<a href="{}"><img src="{}"></a>\n'.format( file, file )
    main += '<br /><a href="cgw.cgi">Back to index</a>\n'

else:
    dirnames = glob.glob( 'graphs/*' )
    dirtime = {}
    for dirname in dirnames:
        target = os.path.join( dirname, '*.png' )
        dirtime[dirname] = max( [os.path.getmtime(f) for f in glob.glob(target)] )

    dirnames.sort(key=lambda k: dirtime[k])

    for dirname in dirnames[::-1]:
        timestamp = dt.fromtimestamp( dirtime[dirname] ).strftime('%Y/%m/%d %H:%M:%S')
        n = dirname.split('/')
        main += '<h3><a href="cgw.cgi?dirname={}">{} [{}]</a></h3>\n'.format( n[1], n[1], timestamp )

print("Content-Type: text/html; charset=UTF-8")
print("")
print(HTML.format(main=main))

