from pysqlite2 import dbapi2 as sqlite
import simplejson as json

#haetaan reseptien tiedot kannasta
def index(req):
    con = sqlite.connect('/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()
	
    sql = """
    SELECT resepti.nimi, resepti.reseptiID, ohje.vaihenro, ohje.ohjeteksti
    FROM resepti LEFT OUTER JOIN ohje
    ON resepti.reseptiID = ohje.reseptiID
    ORDER BY resepti.nimi, resepti.reseptiID, ohje.vaihenro
    """

    cur.execute(sql)
    req.content_type = "application/json; charset=UTF-8"
	#kaksiulotteinen taulukko, jossa on tallessa id ja nimi ja ohjetekstit
    reseptit = []

    for rivi in cur:
        reseptit.append([rivi["ReseptiID"], rivi["Nimi"], rivi["Ohjeteksti"]])

    con.close()
    req.write(json.dumps(reseptit))
    return