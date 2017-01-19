#!/usr/bin/python3

from upload.jdidicom import JDIAE


title='JDIPRINTER'
port=104


myAE=JDIAE(ae_title=title, port=port)

while True:
    try:
        myAE.start()
    except:
        myAE.quit()
