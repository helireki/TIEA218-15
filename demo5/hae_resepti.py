from pysqlite2 import dbapi2 as sqlite
import simplejson as json

#haetaan reseptin tiedot kannasta
def index(req):
    con = sqlite.connect( '/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()

    sql = """
    SELECT resepti.nimi, resepti.kuvaus, resepti.henkilomaara, resepti.ruokalajiID, ohje.vaihenro, ohje.ohjeteksti
    FROM resepti LEFT OUTER JOIN ohje
    ON resepti.reseptiID = :ide AND resepti.reseptiID = ohje.reseptiID
    ORDER BY ohje.vaihenro
    """

    res_id = req.form.getfirst("id")
    req.content_type = "application/json; charset=UTF-8"

    cur.execute(sql, {"ide":res_id})
    resepti = []
    for rivi in cur:
        nimi = rivi["Nimi"]
        kuvaus = rivi["Kuvaus"]
        hlo = rivi["Henkilomaara"]
        ruokaid = rivi["RuokalajiID"]
        ohjeteksti = ""
        try:
            ohjeteksti = rivi["Ohjeteksti"]
        except:
            ohjeteksti = ""
        resepti.append([res_id, nimi, kuvaus, hlo, ruokaid, ohjeteksti])

    con.close()
    req.write(json.dumps(resepti))
    return