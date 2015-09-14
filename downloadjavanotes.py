import mechanize
from time import sleep
from zipfile import ZipFile
import os
import sys
import tempfile
import shutil


br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)

# br.set_debug_http(True)
# br.set_debug_redirects(True)
# br.set_debug_responses(True)

br.open('https://50-001.wikispaces.com/Class+Schedule')

myfiles=[]
for l in br.links():
    if "dl=0" in str(l):
        l.absolute_url = str(l.url)[:-4] + 'dl=1'
        myfiles.append(l)

for l in myfiles:
    sleep(1) 
    br._factory.is_html = True
    br.click_link(l)
    response = br.follow_link(l)
    open(l.text + '.zip', 'w').write(response.read())
    print "Downloaded " + l.text + ".zip"

    zip_path = os.path.abspath(l.text + '.zip')
    with ZipFile(zip_path, 'r') as zip_file:
        files = zip_file.namelist()
        zip_file.extractall(os.path.join(os.getcwd(), l.text), files)
    os.remove(zip_path)
    print "Sucessfully extracted '{}' to '{}'".format(l.text + ".zip", os.getcwd() + "/" + l.text)
