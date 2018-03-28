#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgitb
cgitb.enable()
import cgi
import random
from xml.dom.minidom import getDOMImplementation, parseString
import urllib

#lisätään tyhjä ruutu taulukkoon
def lisaa_ruutu(vanhempi, nro):
    solu = dom1.createElement("td")
    nappi = dom1.createElement("input")
    nappi.setAttribute("type", "submit")
    nappi.setAttribute("name", "ruutu")
    arvo = "%d" % nro
    nappi.setAttribute("value", arvo)
    nappi.setAttribute("class", "tyhja")
    p1 = dom1.createElement("p")
    p1.setAttribute("class", "ruutu")
    solu.appendChild(p1)
    p1.appendChild(nappi)
    vanhempi.appendChild(solu)

    p = dom1.createElement("p")
    piilo = dom1.createElement("input")
    piilo.setAttribute("type", "hidden")
    piilo.setAttribute("name", "ruudut")
    piilo.setAttribute("value", arvo)
    piilo.setAttribute("class", "piilo")
    p.appendChild(piilo)
    form = dom1.getElementsByTagName("table")[0]
    form.appendChild(p)

#lisätään miina taulukkoon
def lisaa_miina(vanh, nro):
    solu = dom1.createElement("td")
    miina = dom1.createElement("input")
    miina.setAttribute("type", "submit")
    miina.setAttribute("name", "ruutu")
    arvo = "m%d" % nro
    miina.setAttribute("value", arvo)
    miina.setAttribute("class", "miina")
    p1 = dom1.createElement("p")
    p1.setAttribute("class", "ruutu")
    solu.appendChild(p1)
    p1.appendChild(miina)
    vanh.appendChild(solu)

    p = dom1.createElement("p")
    piilo = dom1.createElement("input")
    piilo.setAttribute("type", "hidden")
    piilo.setAttribute("name", "ruudut")
    piilo.setAttribute("value", arvo)
    piilo.setAttribute("class", "piilo")
    p.appendChild(piilo)
    form = dom1.getElementsByTagName("table")[0]
    form.appendChild(p)

#tutkitaan tuleeko annettuun kohtaan miinaa
def tuleeko_miina(kohta, lista):
    for t in lista:
        if (t == kohta):
            return True

#poista parametrinä oleva elementti
def luo_tyhja(vanh, nro):
    solu = dom1.createElement("td")
    vanh.appendChild(solu)
   
    arvo = "%d" % nro
    p = dom1.createElement("p")
    piilo = dom1.createElement("input")
    piilo.setAttribute("type", "hidden")
    piilo.setAttribute("name", "ruudut")
    piilo.setAttribute("value", arvo)
    piilo.setAttribute("class", "piilo")
    p.appendChild(piilo)
    form = dom1.getElementsByTagName("table")[0]
    form.appendChild(p)
    

print """Content-type: text/html;charset=UTF-8
"""

form = cgi.FieldStorage()
ruutu_arvot = form.getlist("ruudut")

#luetaan html-pohja ja alustetaan dom
f = urllib.urlopen("http://users.jyu.fi/~helireki/cgi-bin/miinalauta.html")
pohja = f.read()
dom1 = parseString(pohja)

#vaihdetaan otsikko jos tarpeen
otsikko = "Ruudukko"
teksti = form.getfirst("teksti", "")
if (len(teksti) > 0):
    otsikko = teksti.decode("UTF-8")

h1 = dom1.getElementsByTagName("h1")[0]
h1.removeChild(h1.childNodes[0])
h1.appendChild(dom1.createTextNode(otsikko))

#ohjeet
ohje = dom1.getElementsByTagName("p")[0]
viesti = "Kerro luotavan miinaruudukon koko. Ruudukko on yhtä monta ruutua leveä kuin korkea."
ohje.appendChild(dom1.createTextNode(viesti.decode("UTF-8")))

#määritetään taulukon mahdollinen koko
kokos = form.getfirst("x", "")
if kokos == "":
    koko = 0
else:
    try:
        koko = int(kokos)
    except:
        koko = 0

#arvotaan miinojen paikat
miinojen_lkm = koko*koko/3
miinojen_paikat = []
i = 0
while (i < miinojen_lkm):
    kohta = random.randint(0, koko*koko-1)
    poistu = False
    for j in range(len(miinojen_paikat)):
        if miinojen_paikat[j] == kohta:
            poistu = True
    if (poistu):
        continue

    miinojen_paikat.append(kohta)
    i = i+1

bodi = dom1.getElementsByTagName("body")[0]
poisto = form.getfirst("ruutu", "")

#luodaan ruudukko, jos koko sallittu ja validi
if koko >= 6 and koko <= 12:
    ruutu = 0
    taulu = dom1.createElement("table")
    tb = dom1.createElement("tbody")
    taulu.appendChild(tb)
    formi = dom1.createElement("form")
    formi.setAttribute("action", "")
    formi.setAttribute("method", "post")
    bodi.appendChild(formi)
    formi.appendChild(taulu)
    
    #pidetään taulukon kokoa yllä
    ruudukon_koko = dom1.createElement("input")
    ruudukon_koko.setAttribute("type", "hidden")
    arvo = "%d" % koko
    ruudukon_koko.setAttribute("value", arvo)
    ruudukon_koko.setAttribute("name", "koko")
    p1 = dom1.createElement("p")
    p1.appendChild(ruudukon_koko)
    formi.appendChild(p1)

    miinat = 0
    harmaat = 0
    
    #tallennetaan otsikko
    opiilo = dom1.createElement("input")
    opiilo.setAttribute("type", "hidden")
    opiilo.setAttribute("name", "nyk_otsikko")
    opiilo.setAttribute("value", otsikko)
    formi.appendChild(opiilo)

    #luodaan taulukon isäsltö
    for i in range(koko):
        rivi = dom1.createElement("tr")
        tb.appendChild(rivi)
        for j in range(koko):
            ruutu = ruutu + 1
            if (tuleeko_miina(ruutu, miinojen_paikat)):
                lisaa_miina(rivi, miinat)
                miinat = miinat + 1
            else:
                lisaa_ruutu(rivi, harmaat)
                harmaat = harmaat + 1

#jos ruudukon koko ei ole validi
elif kokos != "":
    p = dom1.createElement("p")
    p.appendChild(dom1.createTextNode("Ruudukon koko ei ole validi."))
    bodi.appendChild(p)

#kun on klikattu taulukon ruutua
elif poisto != "":
    taulu = dom1.createElement("table")
    tb = dom1.createElement("tbody")
    taulu.appendChild(tb)
    formi = dom1.createElement("form")
    formi.setAttribute("action", "")
    formi.setAttribute("method", "post")
    formi.appendChild(taulu)

    bodi.appendChild(formi)
    koko = int(form.getlist("koko")[0])

    #pidetään ruudukon kokoa yllä
    ruudukon_koko = dom1.createElement("input")
    ruudukon_koko.setAttribute("type", "hidden")
    arvo = "%d" % koko
    ruudukon_koko.setAttribute("value", arvo)
    ruudukon_koko.setAttribute("name", "koko")
    p1 = dom1.createElement("p")
    p1.appendChild(ruudukon_koko)
    formi.appendChild(p1)

    otsikko = form.getlist("nyk_otsikko")[0].decode("UTF-8")
    
    #muutetan otsikkoa
    opiilo = dom1.createElement("input")
    opiilo.setAttribute("type", "hidden")
    opiilo.setAttribute("name", "nyk_otsikko")
    opiilo.setAttribute("value", otsikko)
    formi.appendChild(opiilo)

    h1 = dom1.getElementsByTagName("h1")[0]
    h1.removeChild(h1.childNodes[0])
    h1.appendChild(dom1.createTextNode(otsikko))

    miinat = 0
    harmaat = 0
    kohta = 0
 
    #luodaan taulukon sisältö
    for i in range(koko):
        rivi = dom1.createElement("tr")
        tb.appendChild(rivi)
        for j in range(koko):
            if (ruutu_arvot[kohta] ==  poisto):
                kohta = kohta + 1
                luo_tyhja(rivi, -1)
                continue
            else:
                if ruutu_arvot[kohta][0] == 'm':
                    lisaa_miina(rivi, miinat)
                    miinat = miinat + 1
                else:
                    if ruutu_arvot[kohta] == '-1':
                        luo_tyhja(rivi, -1)
                    else:
                        lisaa_ruutu(rivi, harmaat)
                        harmaat = harmaat + 1
            kohta = kohta + 1

print dom1.toxml("UTF-8")
