from pysqlite2 import dbapi2 as sqlite


#tässä vähän kummallinen ratkaisu palautusten suhteen, koska ohjelma ei palauttanut mitään, jos return
#oli ihan lopussa??

#lisätään ruokalajin muokkaukset tai ihan uusi ruokalaji kantaan
def index(req):
    con = sqlite.connect('/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()

    mita_muokataan = req.form.getfirst("id")
    nimi = req.form.getfirst("nimi")
    kuvaus = req.form.getfirst("kuvaus")
	
    palautus = "-10"
	
    #muokkaus
    if mita_muokataan != '0':
        sql = """
        UPDATE ruokalaji
        SET nimi = :nimi, kuvaus = :kuvaus
        WHERE ruokalajiID = :muokattava
        """
        try:
            cur.execute(sql, {"nimi":nimi, "kuvaus":kuvaus, "muokattava":mita_muokataan})
            palautus = "1"
            con.commit()
            con.close()
            return palautus
        except:
            palautus = "-2"
            con.close()
            return palautus
    #uuden lisäys
    else:
        sql = """
        INSERT INTO ruokalaji (nimi, kuvaus)
        VALUES (:nimi, :kuvaus)
        """
        try:
            cur.execute(sql, {"nimi":nimi, "kuvaus":kuvaus})
            palautus = "0"
            con.commit()
            con.close()
            return palautus
        except:
            palautus = "-1"
            con.close()
            return palautus
