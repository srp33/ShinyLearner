from httplib2 import Http
from urllib import urlencode

#tagName = sys.argv[1]

h = Http()
data = dict(name="Joe", comment="A test comment")

resp, content = h.request("https://github.com/srp33/ShinyLearner/releases", "GET")
print resp
#print content
#resp, content = h.request("https://github.com/srp33/ShinyLearner/releases", "GET", urlencode(data))
#resp, content = h.request("https://github.com/srp33/ShinyLearner/releases/tag/alpha1", "POST", urlencode(data))
