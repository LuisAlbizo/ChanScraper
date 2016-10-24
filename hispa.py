from basic import *

print(bs(r.get("https://www.hispachan.org/g").content,"html.parser").prettify())


