from pysqlite2 import dbapi2 as sqlite

#lisätään reseptiin tehdyt muokkaukset kantaan
def index(req):
    con = sqlite.connect('/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()
    
    mita_muokataan = req.form.getfirst("id")
    nimi = req.form.getfirst("nimi")
    kuvaus = req.form.getfirst("kuvaus")
    hlo = req.form.getfirst("hlo")
    ruokaid = req.form.getfirst("ruokaid")
    
    #haetaan ensin reseptiä vastaava vaiheiden määrä kannasta, jotta sitä voidaan verrata lomakkeelta tuleviin
    sql = """
    SELECT vaihenro
    FROM ohje
    WHERE reseptiID = :id
    """
    
    palautus = "-10"
    cur.execute(sql, {"id":mita_muokataan})
    maara = 0
    for rivi in cur:
        maara += 1
        
    sql = """
    UPDATE resepti
    SET nimi = :nimi, kuvaus = :kuvaus, henkilomaara = :hlo, ruokalajiID = :ruokaid
    WHERE reseptiID = :ide
    """

    vastineet = {"nimi":nimi, "kuvaus":kuvaus, "hlo":hlo, "ruokaid":ruokaid, "ide":mita_muokataan}
    try:
        cur.execute(sql, vastineet)
        palautus = "0"
    except:
        palautus = "-1"

    #päivitetään jo olemassa olevat vaiheet
    sql = """
    UPDATE ohje
    SET ohjeteksti = :teksti
    WHERE reseptiID = :ide AND vaihenro = :nro
    """
    
    eka_uusi = 0
    for i in range(maara):
        nro = i+1
        teksti = req.form.getfirst("vaihe%s" % str(nro))
        
        try:
            cur.execute(sql, {"teksti":teksti, "ide":mita_muokataan, "nro":nro})
            palautus = "1"
        except:
            con.rollback()
        eka_uusi = nro+1
        
    #lisätään uudet vaiheet
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
        vastineet = {"vaihe":eka_uusi, "res_id":mita_muokataan, "ohjeteksti":alkio}
        try:
            cur.execute(sql, vastineet)
            palautus = "2"
        except:
            con.rollback()
        eka_uusi += 1
        
    con.commit()
    con.close()
    req.write(palautus)
    return