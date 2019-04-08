import re
import requests

text = requests.get("http://117.136.240.193:10003/").text

for u in re.findall('[\'|"](/.*?)[\'|"]',text):
    print u ,1
