from flask import Flask, render_template, request
import sqlite3
from uuid import uuid4
from werkzeug.utils import secure_filename


db = sqlite3.connect("izdevumiii.db", check_same_thread = False)
cur = db.cursor()

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/parskats")
def parskats():
    return render_template("parskats.html")


@app.route("/kontakti")
def kontakti():
    return render_template("kontakti.html")

@app.route("/visi_dati")
def visi_dati():
    res = cur.execute("SELECT * FROM izdevumi")
    izdevumi = res.fetchall()
    return render_template("visi_dati.html", data=izdevumi)




@app.route("/ievade", methods=["GET","POST"])
def ievade():
    #izdevumu datu pievienošana datubāze
    if request.method == "POST":
        id = str(uuid4())
        datums = request.form["datums"]
        izdevumi = request.form["izdevumi"]
        sql = '''INSERT INTO izdevumi
            VALUES (?,?,?)'''
        cur.execute(sql, (id, datums, izdevumi))
        db.commit()
      #čeka augšupielāde datubāze    
        cheks = request.files["cheks"]
        
        filename = secure_filename(cheks.filename)
        mimetype = cheks.mimetype
        cheks_id = str(uuid4())
        cheks_name = filename
        mimetype = mimetype


        sql = ''' INSERT INTO cheks VALUES (?,?,?,?)''' 
        #sqlb.bind_blob(1, cheks)
        #cur.execute(sql (cheks_id, cheks, cheks_name, mimetype)) 
        db.commit() 
        return render_template("ievade.html")
    else:
        return render_template("ievade.html") 


if __name__ == "__main__":
    app.run(debug=True)

