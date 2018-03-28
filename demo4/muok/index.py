import urllib
from pysqlite2 import dbapi2 as sqlite
import sys
from xml.dom.minidom import getDOMImplementation, parse, parseString


def tee_lomake(vanh, doc, cur):
    formi = doc.createElement("form")
    formi.setAttribute("method", "post")
    p1 = doc.createElement("p")
    p2 = doc.createElement("p")
    p3 = doc.createElement("p")
    p4 = doc.createElement("p")

    i1 = doc.createElement("input")
    i2 = doc.createElement("input")
    i3 = doc.createElement("input")

    i1.setAttribute("type", "text")
    i1.setAttribute("name", "nimi")
    i1.setAttribute("id", "nimi")

    i2.setAttribute("type", "text")
    i2.setAttribute("name", "kuvaus")
    i2.setAttribute("id", "kuvaus")

    i3.setAttribute("type", "text")
    i3.setAttribute("name", "hlo")
    i3.setAttribute("id", "hlo")

    l1 = doc.createElement("label")
    t1 = doc.createTextNode("Reseptin nimi ")
    l1.appendChild(t1)
    l2 = doc.createElement("label")
    t2 = doc.createTextNode("Reseptin kuvaus ")
    l2.appendChild(t2)
    l3 = doc.createElement("label")
    teksti = "Henkilömäärä "
    t3 = doc.createTextNode("%s" % teksti.decode("UTF-8"))
    l3.appendChild(t3)
    l4 = doc.createElement("label")

    l1.setAttribute("for", "nimi")
    l1.setAttribute("for", "kuvaus")
    l1.setAttribute("for", "hlo")

    p1.appendChild(l1)
    p1.appendChild(i1)
    p2.appendChild(l2)
    p2.appendChild(i2)
    p3.appendChild(l3)
    p3.appendChild(i3)
    p4.appendChild(l4)


    p5 = doc.createElement("p")
    i5 = doc.createElement("input")
    i5.setAttribute("type", "text")
    i5.setAttribute("name", "vaihe1")
    i5.setAttribute("id", "vaihe1")
    l5 = doc.createElement("label")
    l5.setAttribute("for", "vaihe1")
    t5 = doc.createTextNode("1. vaihe ")
    l5.appendChild(t5)
    p5.appendChild(l5)
    p5.appendChild(i5)

    p6 = doc.createElement("p")
    i6 = doc.createElement("input")
    i6.setAttribute("type", "text")
    i6.setAttribute("name", "vaihe2")
    i6.setAttribute("id", "vaihe2")
    l6 = doc.createElement("label")
    l6.setAttribute("for", "vaihe2")
    t6 = doc.createTextNode("2. vaihe ")
    l6.appendChild(t6)
    p6.appendChild(l6)
    p6.appendChild(i6)

    p7 = doc.createElement("p")
    i7 = doc.createElement("input")
    i7.setAttribute("type", "text")
    i7.setAttribute("name", "vaihe3")
    i7.setAttribute("id", "vaihe3")
    l7 = doc.createElement("label")
    l7.setAttribute("for", "vaihe3")
    t7 = doc.createTextNode("3. vaihe ")
    l7.appendChild(t7)
    p7.appendChild(l7)
    p7.appendChild(i7)

    p8 = doc.createElement("p")
    i8 = doc.createElement("input")
    i8.setAttribute("type", "text")
    i8.setAttribute("name", "vaihe4")
    i8.setAttribute("id", "vaihe4")
    l8 = doc.createElement("label")
    l8.setAttribute("for", "vaihe4")
    t8 = doc.createTextNode("4. vaihe ")
    l8.appendChild(t8)
    p8.appendChild(l8)
    p8.appendChild(i8)

    p9 = doc.createElement("p")
    i9 = doc.createElement("input")
    i9.setAttribute("type", "text")
    i9.setAttribute("name", "vaihe5") 
    i9.setAttribute("id", "vaihe5")
    l9 = doc.createElement("label")
    l9.setAttribute("for", "vaihe5")
    t9 = doc.createTextNode("5. vaihe ")
    l9.appendChild(t9)
    p9.appendChild(l9)
    p9.appendChild(i9)

    p10 = doc.createElement("p")
    i10 = doc.createElement("input")
    i10.setAttribute("type", "text")
    i10.setAttribute("name", "vaihe6")
    i10.setAttribute("id", "vaihe6")
    l10 = doc.createElement("label")
    l10.setAttribute("for", "vaihe6")
    t10 = doc.createTextNode("6. vaihe ")
    l10.appendChild(t10)
    p10.appendChild(l10)
    p10.appendChild(i10)

    p11 = doc.createElement("p")
    i11 = doc.createElement("input")
    i11.setAttribute("type", "text")
    i11.setAttribute("name", "vaihe7")
    i11.setAttribute("id", "vaihe7")
    l11 = doc.createElement("label")
    l11.setAttribute("for", "vaihe7")
    t11 = doc.createTextNode("7. vaihe ")
    l11.appendChild(t11)
    p11.appendChild(l11)
    p11.appendChild(i11)

    p12 = doc.createElement("p")
    i12 = doc.createElement("input")
    i12.setAttribute("type", "text")
    i12.setAttribute("name", "vaihe8")
    i12.setAttribute("id", "vaihe8")
    l12 = doc.createElement("label")
    l12.setAttribute("for", "vaihe8")
    t12 = doc.createTextNode("8. vaihe ")
    l12.appendChild(t12)
    p12.appendChild(l12)
    p12.appendChild(i12)

    p13 = doc.createElement("p")
    i13 = doc.createElement("input")
    i13.setAttribute("type", "text")
    i13.setAttribute("name", "vaihe9")
    i13.setAttribute("id", "vaihe9")
    l13 = doc.createElement("label")
    l13.setAttribute("for", "vaihe9")
    t13 = doc.createTextNode("9. vaihe ")
    l13.appendChild(t13)
    p13.appendChild(l13)
    p13.appendChild(i13)

    p14 = doc.createElement("p")
    i14 = doc.createElement("input")
    i14.setAttribute("type", "text")
    i14.setAttribute("name", "vaihe10")
    i14.setAttribute("id", "vaihe10")
    l14 = doc.createElement("label")
    l14.setAttribute("for", "vaihe10")
    t14 = doc.createTextNode("10. vaihe ")
    l14.appendChild(t14)
    p14.appendChild(l14)
    p14.appendChild(i14)

    formi.appendChild(p1)
    formi.appendChild(p2)
    formi.appendChild(p3)
    formi.appendChild(p4)

    otsikko = doc.createElement("p")
    tekst = doc.createTextNode("Ohjeen vaiheet:")
    labeli = doc.createElement("label")
    labeli.appendChild(tekst)
    otsikko.appendChild(labeli)

    formi.appendChild(otsikko)
    formi.appendChild(p5)
    formi.appendChild(p6)
    formi.appendChild(p7)
    formi.appendChild(p8)
    formi.appendChild(p9)
    formi.appendChild(p10)
    formi.appendChild(p11)
    formi.appendChild(p12)
    formi.appendChild(p13)
    formi.appendChild(p14)


    psub = doc.createElement("p")

    inp = doc.createElement("input")
    inp.setAttribute("type", "submit")
    teksti = "Tallenna"
    inp.setAttribute("value", "%s" % teksti.decode("UTF-8"))
    inp.setAttribute("name", "tallenna")

    psub.appendChild(inp)
    formi.appendChild(psub)

    vanh.appendChild(formi)

    sel = doc.createElement("select")
    sel.setAttribute("id", "list")
    sel.setAttribute("name", "lajit")
    label = doc.createElement("label")
    label.setAttribute("for", "list")
    label.appendChild(doc.createTextNode("Ruokalajit "))
    p4.appendChild(label)
    for rivi in cur:
        opt = doc.createElement("option")
        arvo = "%s" % rivi["nimi"]
        opt.setAttribute("value", str(rivi["ruokalajiID"]))
        opt.appendChild(doc.createTextNode(arvo.decode("UTF-8")))
        sel.appendChild(opt)

    p4.appendChild(sel)


#tarkistetaan, onko henkilömäärä oikea
def tarkista_hlo(vanh, doc, req):
    if req.form.getfirst("hlo") == "":
        t = " Henkilömäärän on oltava 1 tai enemmän."
        teksti = doc.createTextNode("%s" % t.decode("UTF-8"))
        vanh.appendChild(teksti)
        return False
    try:
        maara = int(req.form.getfirst("hlo"))
        if maara < 1:
            t = " Henkilömäärän on oltava 1 tai enemmän."
            teksti = doc.createTextNode("%s" % t.decode("UTF-8"))
            vanh.appendChild(teksti)
            return False
        return True
    except:
        t = " Henkilömäärän on oltava vain numeroita."
        teksti = doc.createTextNode("%s" % t.decode("UTF-8"))
        vanh.appendChild(teksti)
        return False


#tarkistetaan, onko reseptillä nimi
def tarkista_resnimi(vanh, doc, req):
    if req.form.getfirst("nimi") == "":
        t = " Reseptillä on oltava nimi."
        teksti = doc.createTextNode("%s" % t.decode("UTF-8"))
        vanh.appendChild(teksti)
        return False
    return True


#muutetaan reseptin tietoja käyttäjän syöttämien tietojen perusteella
def index(req):
    req.content_type = "text/html ;charset=utf-8"
    con = sqlite.connect( '/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()

    sql = """
    SELECT nimi, ruokalajiID
    FROM ruokalaji
    """

    try:
        cur.execute(sql)
    except:
        req.write("Virhe tietokannan ruokalajien haussa: %s" % sys.exc_info()[0])

    f = urllib.urlopen("http://users.jyu.fi/~helireki/wsovellukset15/demo4/sisalto.html")
    pohja = f.read()
    dom1 = parseString(pohja)

    bodi = dom1.getElementsByTagName("body")[0]
    h2 = dom1.createElement("h2")
    t = "Muokkaa reseptiä."
    teksti = dom1.createTextNode('%s' % t.decode("UTF-8"))
    h2.appendChild(teksti)
    bodi.appendChild(h2)

    nimi_otsikko = dom1.createElement("h3")
    bodi.appendChild(nimi_otsikko)

    tee_lomake(bodi, dom1, cur)

    res_id = req.form.getfirst("id")

    sql = """
    SELECT resepti.nimi, resepti.kuvaus, resepti.henkilomaara, resepti.ruokalajiID, ohje.vaihenro, ohje.ohjeteksti
    FROM resepti LEFT OUTER JOIN ohje
    ON resepti.reseptiID = :ide AND resepti.reseptiID = ohje.reseptiID
    ORDER BY ohje.vaihenro
    """

    try:
        cur.execute(sql, {"ide":res_id})
    except:
        req.write("Virhe reseptin tietojen haussa: %s" % sys.exc_info()[0])
        cur = {}

    hlo_p = dom1.getElementsByTagName("p")[2]
    nimi_p = dom1.getElementsByTagName("p")[0]
    kuvaus_p = dom1.getElementsByTagName("p")[1]

    nimi_inp = nimi_p.childNodes[1]
    kuvaus_inp = kuvaus_p.childNodes[1]
    hlo_inp = hlo_p.childNodes[1]
    optionit = dom1.getElementsByTagName("option")
    ruoka_opt = ""
    vaiheboksit = dom1.getElementsByTagName("input") #1. vaihe löytyy 4. inputista listassa
    i = 3
    montako_vaihetta = 0
    onko_nimi = False

    for rivi in cur:
        nimiteksti = rivi["nimi"].decode("UTF-8")
        nimi_inp.setAttribute("value", nimiteksti)

        if not onko_nimi:
            nimi_otsikko.appendChild(dom1.createTextNode(nimiteksti))
            onko_nimi = True

        kuvaus_inp.setAttribute("value", rivi["kuvaus"].decode("UTF-8"))
        hlo_inp.setAttribute("value", "%s" % rivi["henkilomaara"])
        #valitaan oikea option ja laitetaan se valituksi
        if ruoka_opt == "":
            for opt in optionit:
                if opt.getAttribute("value") == str(rivi["ruokalajiID"]):
                    ruoka_opt = opt
                    opt.setAttribute("selected", "selected")
                    break
        try:
            teksti = rivi["ohjeteksti"]
            vaiheboksit[i].setAttribute("value", "%s" % teksti.decode("UTF-8"))
            i += 1
            montako_vaihetta += 1
        except:
            continue

    if req.form.getfirst("tallenna") == "Tallenna":
        onko_hlo = tarkista_hlo(hlo_p, dom1, req)
        onko_nimi = tarkista_resnimi(nimi_p, dom1, req)
        if onko_hlo and onko_nimi:
            res_nimi = req.form.getfirst("nimi")
            res_kuvaus = req.form.getfirst("kuvaus")
            res_hlo = req.form.getfirst("hlo")
            res_ruok = req.form.getfirst("lajit")

            sql = """
            UPDATE resepti
            SET nimi = :nimi, kuvaus = :kuvaus, henkilomaara = :hlo, ruokalajiID = :ruokaid
            WHERE reseptiID = :ide
            """

            vastineet = {"nimi":res_nimi, "kuvaus":res_kuvaus, "hlo":res_hlo, "ruokaid":res_ruok, "ide":res_id}
            try:
                cur.execute(sql, vastineet)
                nimi_inp.setAttribute("value", res_nimi.decode("UTF-8"))
                kuvaus_inp.setAttribute("value", res_kuvaus.decode("UTF-8"))
                hlo_inp.setAttribute("value", res_hlo)
                for opt in optionit:
                    if opt.getAttribute("value") == res_ruok:
                        ruoka_opt = opt
                        opt.setAttribute("selected", "selected")
                        break
            except:
                req.write("Virhe reseptin muokkauksessa 1: %s" % sys.exc_info()[0])
                con.rollback()

            sql = """
            UPDATE ohje
            SET ohjeteksti = :teksti
            WHERE reseptiID = :ide AND vaihenro = :nro
            """
            eka_uusi = 0

            for i in range(montako_vaihetta):
                teksti = req.form.getfirst("vaihe%s" % str(i+1))
                ide = res_id
                nro = i+1

                try:
                    cur.execute(sql, {"teksti":teksti, "ide":ide, "nro":nro})
                    vaiheboksit[i+3].setAttribute("value", teksti.decode("UTF-8"))
                except:
                    req.write("Virhe reseptin muokkauksessa 2: %s" % sys.exc_info()[0])
                    con.rollback()
                eka_uusi = nro + 1

            #tähän uusien vaiheiden lisäys
            sql = """
            INSERT INTO ohje (ohjeteksti, reseptiID, vaihenro)
            VALUES (:ohjeteksti, :res_id, :vaihe)
            """
            if eka_uusi == 0:
                eka_uusi = 1

            #tässä on ratkaisu, että otetaan vain peräkkäiset ohjekohdat mukaan
            vaiheet = []
            for i in range(10):
                teksti = req.form.getfirst("vaihe%s" % str(i + eka_uusi), "")
                if teksti != "":
                    vaiheet.append(teksti)
                else:
                    break

            for alkio in vaiheet:
                vastineet = {"vaihe":eka_uusi, "res_id":res_id, "ohjeteksti":alkio}
                try:
                    cur.execute(sql, vastineet)
                    vaiheboksit[3+eka_uusi-1].setAttribute("value", teksti.decode("UTF-8")) 
                except:
                    req.write("Virhe vaiheiden lisäyksessa: %s" % sys.exc_info()[0])
                    con.rollback()
                eka_uusi += 1

            con.commit()
            req.write("Muokkaus onnistui!")
            nimi_otsikko.removeChild(nimi_otsikko.childNodes[0])
            nimi_otsikko.appendChild(dom1.createTextNode(res_nimi.decode("UTF-8")))

       #laitetaan jo syötetyt tiedot näkyviin
        else:
            res_nimi = req.form.getfirst("nimi").decode("UTF-8")
            res_kuvaus = req.form.getfirst("kuvaus").decode("UTF-8")
            res_hlo = req.form.getfirst("hlo").decode("UTF-8")
            res_ruok = req.form.getfirst("lajit").decode("UTF-8")

            vaiheet = []
            for i in range(10):
                teksti = req.form.getfirst("vaihe%s" % str(i+1), "")
                vaiheet.append(teksti)

            inputit = dom1.getElementsByTagName("input") #näistä viimeinen on nappula
            inputit[0].setAttribute("value", res_nimi)
            inputit[1].setAttribute("value", res_kuvaus)
            inputit[2].setAttribute("value", res_hlo)

            for i in range(7):
                inputit[i+3].setAttribute("value", (vaiheet[i].decode("UTF-8")))

    con.close()
    return dom1.toxml("UTF-8")
