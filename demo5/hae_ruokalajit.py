from pysqlite2 import dbapi2 as sqlite
import simplejson as json

#haetaan ruokalajit kannasta
def index(req):
    con = sqlite.connect('/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()
	
    sql = """
    SELECT ruokalajiID, nimi
    FROM ruokalaji
    ORDER BY nimi
    """

    cur.execute(sql)
    req.content_type = "application/json; charset=UTF-8"
    ruokalajit = {}

    for rivi in cur:
        ruokalajit[rivi["RuokalajiID"]] = rivi["Nimi"]

    con.close()
    req.write(json.dumps(ruokalajit))
    return