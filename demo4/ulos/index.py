import urllib
from xml.dom.minidom import getDOMImplementation, parse, parseString


#Kirjaudutaan ulos sovelluksesta
def index(req):
    req.session.delete()
    req.content_type = "text/html ;charset=utf-8"
    
    f = urllib.urlopen("http://users.jyu.fi/~helireki/wsovellukset15/demo4/sisalto.html")
    pohja = f.read()
    dom1 = parseString(pohja)

    bodi = dom1.getElementsByTagName("body")[0]
    p = dom1.createElement("p")
    teksti = dom1.createTextNode("Olet kirjautunut ulos.")
    p.appendChild(teksti)
    bodi.appendChild(p)

    return dom1.toxml("UTF-8")

