#!python
import urllib.request
import re


def get_title(html): return re.findall(
    '<title>(.*?)</title>', html, flags=re.DOTALL)[0].strip()


url = 'https://bitbucket.org/'

fp = urllib.request.urlopen(url)
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

print(mystr)

print(get_title(mystr))
