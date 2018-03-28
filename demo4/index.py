from pysqlite2 import dbapi2 as sqlite
import sys
from xml.dom.minidom import getDOMImplementation, parse, parseString
import urllib

#tulostetaan kannassa olevat resptien nimet
def index(req):
    req.content_type = "text/html ;charset=utf-8"
    con = sqlite.connect( '/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row

    f = urllib.urlopen("http://users.jyu.fi/~helireki/wsovellukset15/demo4/sisalto.html")
    pohja = f.read()
    dom1 = parseString(pohja)

    sql = """
    SELECT resepti.nimi, resepti.reseptiID, ohje.vaihenro, ohje.ohjeteksti
    FROM resepti LEFT OUTER JOIN ohje
    ON resepti.reseptiID = ohje.reseptiID
    ORDER BY resepti.nimi, resepti.reseptiID, ohje.vaihenro
    """

    cur = con.cursor()
    try:
        cur.execute(sql)
    except:
        req.write("Virhe reseptien tietojen haussa: %s" % sys.exc_info()[0])

    bodi = dom1.getElementsByTagName("body")[0]
    ul = dom1.createElement("ul")
    edellinen = 0
    ohjelista = ""
    for rivi in cur:
        nimi = rivi["Nimi"]
        vaihe = rivi["Ohjeteksti"]
        res_id = rivi["ReseptiID"]
        if res_id != edellinen:
            li = dom1.createElement("li")
            teksti = dom1.createTextNode('%s' % nimi.decode("UTF-8"))
            linkki = dom1.createElement("a")
            osoite = "http://users.jyu.fi/~helireki/wsovellukset15/demo4/muok/?id=%s" % res_id
            linkki.setAttribute("href", osoite)
            linkki.appendChild(teksti)
            li.appendChild(linkki)
            ul.appendChild(li)
        try:
            teksti = dom1.createTextNode('%s' % vaihe.decode("UTF-8"))
            if edellinen != res_id:
                li2 = dom1.createElement("li")
                ol = dom1.createElement("ol")
                ohjelista = ol
                li2.appendChild(ol)
                li3 = dom1.createElement("li")
                li3.appendChild(teksti)
                ol.appendChild(li3)
                ul.appendChild(li2)
                edellinen = res_id
            else:
                li3 = dom1.createElement("li")
                ol.appendChild(li3)
                li3.appendChild(teksti)
        except:
            continue
    bodi.appendChild(ul)

    con.close()
    req.write(dom1.toxml("UTF-8"))
