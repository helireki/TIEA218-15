from mod_python import apache, Session
from mod_python import util
from xml.dom.minidom import getDOMImplementation, parse, parseString
import urllib


#tutkitaan, onko sivulle tulija kirjautunut vai ei
#näytetään kirjautumissivu, jos ei
def handler(req):
    try:
        if req.session["kirjautunut"] == "ok":
            return apache.OK
    except:
        f = urllib.urlopen("http://users.jyu.fi/~helireki/wsovellukset15/demo4/kirjaudu.html")
        pohja = f.read()
        dom1 = parseString(pohja)
        form = util.FieldStorage(req)
        tunnus = form.getfirst("tunnus")
        salasana = form.getfirst("salasana")
        if tunnus == "tiea218@foo.example" and salasana == "salasana":
            req.session["kirjautunut"] = "ok"
            req.session.save()
            return apache.OK
        req.content_type = "text/html ;charset=utf-8"
        
        bodi = dom1.getElementsByTagName("body")[0]
        viesti = ""
        if form.getfirst("kirjaudu") == "Kirjaudu":
            if tunnus != "tiea218@foo.example":
                viesti = "Käyttäjätunnusta ei löytynyt. "
            elif salasana != "salasana":
                viesti += "Käyttäjätunnus oli oikea, mutta salasana väärä. "
            p = dom1.createElement("p")
            viesti += "Syötä tunnus ja salasana uudelleen."
            p.appendChild(dom1.createTextNode(viesti.decode("UTF-8")))
            bodi.appendChild(p)
        req.write(dom1.toxml("UTF-8"))

    return apache.DONE
