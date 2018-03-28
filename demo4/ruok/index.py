from pysqlite2 import dbapi2 as sqlite
import sys
from xml.dom.minidom import getDOMImplementation, parse, parseString
import urllib


#tehdään lomake
def tee_lomake(vanh, doc, cur):
    formi = doc.createElement("form")
    formi.setAttribute("method", "post")
    p = doc.createElement("p")

    sel = doc.createElement("select")
    sel.setAttribute("id", "list")
    sel.setAttribute("name", "lajit")
    label = doc.createElement("label")
    label.setAttribute("for", "list")
    label.appendChild(doc.createTextNode("Ruokalajit "))
    p.appendChild(label)

    opt = doc.createElement("option")
    opt.setAttribute("value", "0")
    arvo = "Lisää uusi ruokalaji"
    opt.appendChild(doc.createTextNode(arvo.decode("UTF-8")))
    sel.appendChild(opt)

    for rivi in cur:
        opt = doc.createElement("option")
        arvo = "%s" % rivi["nimi"]
        opt.setAttribute("value", str(rivi["ruokalajiID"]))
        opt.appendChild(doc.createTextNode(arvo.decode("UTF-8")))
        sel.appendChild(opt)

    submit_inp = doc.createElement("input")
    submit_inp.setAttribute("type", "submit")
    teksti = "Valitse"
    submit_inp.setAttribute("value", "%s" % teksti.decode("UTF-8"))
    submit_inp.setAttribute("name", "valitse")

    p.appendChild(sel)
    formi.appendChild(p)
    formi.appendChild(submit_inp)
    vanh.appendChild(formi)


#tehdään lomake, jossa lisätään tai muokataan ruokalaji
def tee_kenttalomake(vanh, doc, arvo):
    formi = doc.createElement("form")
    formi.setAttribute("method", "post")

    p1 = doc.createElement("p")
    p2 = doc.createElement("p")

    i1 = doc.createElement("input")
    i1.setAttribute("type", "text")
    i1.setAttribute("name", "nimi")
    i1.setAttribute("id", "nimi")
    l1 = doc.createElement("label")
    l1.setAttribute("for", "nimi")
    t1 = doc.createTextNode("Ruokalajin nimi ")
    l1.appendChild(t1)
    p1.appendChild(l1)
    p1.appendChild(i1)

    i2 = doc.createElement("input")
    i2.setAttribute("type", "text")
    i2.setAttribute("name", "kuvaus")
    i2.setAttribute("id", "kuvaus")
    l2 = doc.createElement("label")
    l2.setAttribute("for", "kuvaus")
    t2 = doc.createTextNode("Ruokalajin kuvaus ")
    l2.appendChild(t2)
    p2.appendChild(l2)
    p2.appendChild(i2)

    formi.appendChild(p1)
    formi.appendChild(p2)

    subinp = doc.createElement("input")
    subinp.setAttribute("type", "submit")
    teksti = "Lähetä"
    subinp.setAttribute("value", "%s" % teksti.decode("UTF-8"))
    subinp.setAttribute("name", "laheta")

    p3 = doc.createElement("input")
    p3.setAttribute("type", "hidden")
    p3.setAttribute("name", "muokattava")
    p3.setAttribute("value", arvo)

    formi.appendChild(subinp)
    formi.appendChild(p3)
    vanh.appendChild(formi)


#tarkistetaan, onko uusi nimi täytetty
def tarkista_nimi(vanh, doc, req):
    if req.form.getfirst("nimi") == "":
        teksti = " Ruokalajilla pitää olla nimi."
        viesti = doc.createTextNode(teksti.decode("UTF-8"))
        vanh.appendChild(viesti)
        return False
    return True


#muokataan ruokalajia tai lisätään uusi
def index(req):
    req.content_type = "text/html ;charset=utf-8"
    con = sqlite.connect( '/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()

    f = urllib.urlopen("http://users.jyu.fi/~helireki/wsovellukset15/demo4/sisalto.html")
    pohja = f.read()
    dom1 = parseString(pohja)

    bodi = dom1.getElementsByTagName("body")[0]
    tieto = dom1.createElement("h2")
    teksti = "Valitse muokattava ruokalaji listasta tai lisää uusi."
    tieto.appendChild(dom1.createTextNode(teksti.decode("UTF-8")))
    bodi.appendChild(tieto)

    sql = """
    SELECT nimi, ruokalajiID
    FROM ruokalaji
    """

    try:
        cur.execute(sql)
    except:
        req.write("Virhe tietokannan ruokalajien haussa: %s" % sys.exc_info()[0])

    tee_lomake(bodi, dom1, cur)

    if req.form.getfirst("valitse") == "Valitse":
        #tässä luodaan uusi formi, jossa näytetään tyhjät kentät tai tiedot riippuen lajit-parametrin arvosta
        if req.form.getfirst("lajit") == '0':
            h2 = dom1.createElement("h2")
            teksti = "Uuden ruokalajin lisääminen:"
            textnode = dom1.createTextNode(teksti.decode("UTF-8"))
            h2.appendChild(textnode)
            bodi.appendChild(h2)
            h3 = dom1.createElement("h3")
            teksti = "Uusi ruokalaji"
            textnode = dom1.createTextNode(teksti.decode("UTF-8"))
            h3.appendChild(textnode)
            bodi.appendChild(h3)
            tee_kenttalomake(bodi, dom1, '0')
        else:
            sql = """
            SELECT nimi, kuvaus
            FROM ruokalaji
            WHERE ruokalajiID = :arvo
            """

            arvo = req.form.getfirst("lajit")
            try:
                cur.execute(sql, {"arvo":arvo})
                ot = dom1.createElement("h3")
                nimi = ""
                kuvaus = ""
                for rivi in cur:
                    nimi = rivi["nimi"]
                    kuvaus = rivi["kuvaus"]
                h2 = dom1.createElement("h2")
                teksti = "Ruokalajin tietojen muokkaaminen:"
                textnode = dom1.createTextNode(teksti.decode("UTF-8"))
                h2.appendChild(textnode)
                bodi.appendChild(h2)
                textnode = dom1.createTextNode(nimi.decode("UTF-8"))
                ot.appendChild(textnode)
                bodi.appendChild(ot)
                tee_kenttalomake(bodi, dom1, arvo)

                #täytetään kentät oikeilla tiedoilla
                inputit = dom1.getElementsByTagName("input") #näistä  ensimmäinen ja viimeinen on nappuloita
                inputit[1].setAttribute("value", nimi.decode("UTF-8"))
                inputit[2].setAttribute("value", kuvaus.decode("UTF-8"))
            except:
                req.write("Virhe halutun ruokalajin haussa: %s" % sys.exc_info()[0])

    #käsitellään tietojen lisäys/muokkaus
    elif req.form.getfirst("laheta") == "Lähetä":
        #muokkaus
        mita_muokataan = req.form.getfirst("muokattava")
        if mita_muokataan != '0':
            sql = """
            UPDATE ruokalaji
            SET nimi = :nimi, kuvaus = :kuvaus
            WHERE ruokalajiID = :muokattava
            """
            nimi = req.form.getfirst("nimi")
            kuvaus = req.form.getfirst("kuvaus")
            muokattava = mita_muokataan

            h2 = dom1.createElement("h2")
            teksti = "Ruokalajin tietojen muokkaaminen:"
            textnode = dom1.createTextNode(teksti.decode("UTF-8"))
            h2.appendChild(textnode)
            bodi.appendChild(h2)
            ot = dom1.createElement("h3")
            nimiteksti = nimi

            if nimiteksti == "":
                try:
                    cur.execute("""SELECT nimi FROM ruokalaji WHERE ruokalajiID = :nro""", {"nro":mita_muokataan})
                except:
                    req.write("Virhe moukattavan ruokalajin nimen haussa: %s" % sys.exc_info()[0])
            for rivi in cur:
                nimiteksti = rivi["nimi"]
            textnode = dom1.createTextNode(nimiteksti.decode("UTF-8"))
            ot.appendChild(textnode)
            bodi.appendChild(ot)
            tee_kenttalomake(bodi, dom1, mita_muokataan)

            nimi_p = dom1.getElementsByTagName("p")[1]

            if tarkista_nimi(nimi_p, dom1, req):
                try:
                    cur.execute(sql, {"nimi":nimi, "kuvaus":kuvaus, "muokattava":muokattava})
                    con.commit()
                    #mita_muokataan sisältää oikean valuen, jonka perusteella saa oikean optionin, jonka lapsinode pitää päivittää
                    optionit = dom1.getElementsByTagName("option")
                    for opt in optionit:
                        if opt.getAttribute("value") == mita_muokataan:
                            pois = opt.childNodes[0]
                            opt.removeChild(pois)
                            uusi = dom1.createTextNode(nimi)
                            opt.appendChild(uusi)
                    teksti = "Muokkaus onnistui!"
                    req.write(teksti)
                    kuvaus_p = dom1.getElementsByTagName("p")[2]
                    inp = kuvaus_p.childNodes[1]
                    inp.setAttribute("value", kuvaus.decode("UTF-8"))
                    nimi_inp = nimi_p.childNodes[1]
                    nimi_inp.setAttribute("value", nimi.decode("UTF-8"))
                except:
                    req.write("Virhe halutun ruokalajin päivittämisessä: %s" % sys.exc_info()[0])
            else:
                kuvaus_p = dom1.getElementsByTagName("p")[2]
                inp = kuvaus_p.childNodes[1]
                inp.setAttribute("value", kuvaus.decode("UTF-8"))
        #uuden lisäys
        else:
            sql = """
            INSERT INTO ruokalaji (nimi, kuvaus)
            VALUES (:nimi, :kuvaus)
            """
            nimi = req.form.getfirst("nimi")
            kuvaus = req.form.getfirst("kuvaus")

            h2 = dom1.createElement("h2")
            teksti = "Uuden ruokalajin lisääminen:"
            textnode = dom1.createTextNode(teksti.decode("UTF-8"))
            h2.appendChild(textnode)
            bodi.appendChild(h2)
            h3 = dom1.createElement("h3")
            teksti = "Uusi ruokalaji"
            textnode = dom1.createTextNode(teksti.decode("UTF-8"))
            h3.appendChild(textnode)
            bodi.appendChild(h3)
            tee_kenttalomake(bodi, dom1, '0')

            nimi_p = dom1.getElementsByTagName("p")[1]

            if tarkista_nimi(nimi_p, dom1, req):
                try:
                    cur.execute(sql, {"nimi":nimi, "kuvaus":kuvaus})
                    con.commit()
                    opt = dom1.createElement("option")
                    opt.setAttribute("value", str(cur.lastrowid))
                    opt.appendChild(dom1.createTextNode(nimi.decode("UTF-8")))
                    sel = dom1.getElementsByTagName("select")[0]
                    sel.appendChild(opt)
                    teksti = "Lisäys onnistui!"
                    req.write(teksti)
                except:
                    req.write("Virhe uuden ruokalajin lisäämisessä: %s" % sys.exc_info()[0])
            else:
                kuvaus_p = dom1.getElementsByTagName("p")[2]
                inp = kuvaus_p.childNodes[1]
                inp.setAttribute("value", kuvaus.decode("UTF-8")) 
    con.close()
    return dom1.toxml("UTF-8")
