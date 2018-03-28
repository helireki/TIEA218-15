from pysqlite2 import dbapi2 as sqlite

#lisätään uusi resepti kantaan
def index(req):
    con = sqlite.connect('/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()

    sql = """
    INSERT INTO resepti (nimi, kuvaus, henkilomaara, ruokalajiID)
    VALUES (:nimi, :kuvaus, :hlo, :ruoka)
    """

    nimi = req.form.getfirst("nimi")
    kuvaus = req.form.getfirst("kuvaus")
    hlo = req.form.getfirst("hlo")
    ruoka = req.form.getfirst("ruoka")
    palautus = "-1"

    try:
        cur.execute(sql, {"nimi":nimi, "kuvaus":kuvaus, "hlo":hlo, "ruoka":ruoka})
        palautus = "0"
    except:
        palautus = "1"

    #tässä on ratkaisu, että otetaan vain peräkkäiset ohjekohdat mukaan
    vaiheet = []
    for i in range(10):
        teksti = req.form.getfirst("vaihe%s" % str(i+1), "")
        if teksti != "":
            vaiheet.append(teksti) 
        else:
            break

    sql = """
	INSERT INTO ohje (vaihenro, reseptiID, ohjeteksti)
    VALUES (:vaihe, :res_id, :ohjeteksti)
    """
	
    nro = 1
    resi = cur.lastrowid
    for alkio in vaiheet:
        vastineet = {"vaihe":nro, "res_id":resi, "ohjeteksti":alkio}
        try:
            cur.execute(sql, vastineet)
        except:
            palautus = "1"
            con.rollback()
        nro += 1
	
    con.commit()
    con.close()
    return palautus