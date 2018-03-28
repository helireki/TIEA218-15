from pysqlite2 import dbapi2 as sqlite
import simplejson as json

#haetaan ruokalaji kannasta id:n perusteella
def index(req):
    req.content_type = "text/html ;charset=utf-8"
    con = sqlite.connect( '/nashome2/helireki/html/hidden/kanta_demo/resepti')
    con.text_factory = str
    con.row_factory = sqlite.Row
    cur = con.cursor()

    sql = """
    SELECT nimi, kuvaus
    FROM ruokalaji
    WHERE ruokalajiID = :arvo
    """

    arvo = req.form.getfirst("valittu")
    cur.execute(sql, {"arvo":arvo})
    req.content_type = "application/json; charset=UTF-8"

    ruokalaji = {}
    for rivi in cur:
        ruokalaji["nimi"] = rivi["Nimi"]
        ruokalaji["kuvaus"] = rivi["Kuvaus"]
        ruokalaji["id"] = arvo

    con.close()
    req.write(json.dumps(ruokalaji))
    return