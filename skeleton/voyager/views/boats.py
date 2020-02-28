
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from voyager.db import get_db, execute

def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")

def get_boats_from_sailor_name(conn, sailor_name):
    return execute(conn, 
    "SELECT DISTINCT Boats.bid, Boats.name  FROM ((Sailors INNER JOIN Voyages ON Voyages.sid = Sailors.sid) INNER JOIN Boats ON Voyages.bid = Boats.bid) WHERE Sailors.name = :s_name", {'s_name': sailor_name})

def get_boats_by_popularity(conn):
    return execute(conn, 
    "SELECT DISTINCT Boats.bid, Boats.name, COUNT(Boats.bid) as num_of_voyages  FROM (Boats INNER JOIN Voyages ON Voyages.bid = Boats.bid) GROUP BY Boats.bid ORDER BY COUNT(Boats.bid) DESC")

def insert_boat_in_DB(conn, boat_name, boat_color):
    if boat_name == None or boat_color == None or boat_name == "" or boat_color == "":
        raise Exception
    return execute(conn,
    "INSERT INTO Boats (name, color) VALUES (:boat_name, :boat_color);", {'boat_name': boat_name, "boat_color": boat_color}
    )

def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="boats", rows=rows)

    @bp.route("/boats/sailed-by")
    def _get_boats_from_sailors_name():
        with get_db() as conn:
            sailor_name = request.args.get('sailor-name')
            rows = get_boats_from_sailor_name(conn, sailor_name)
        return render_template("table.html", name="Boats sailed by sailor: " + sailor_name, rows=rows)
    
    @bp.route("/boats/by-popularity")
    def _get_boats_by_popularity():
        with get_db() as conn:
            rows = get_boats_by_popularity(conn)
        return render_template("table.html", name="Boats ordered by popularity (Num of Voyages): ", rows=rows)

    @bp.route("/boats/add", methods=['POST', 'GET'])
    def _add_boat():
        atrributes = {"Name" : "text", "Color": "text" }
        return render_template("form.html", name="Add Boats: ", URI="/boats/add/submit",  submit_message="Add boat", atrributes=atrributes)

    @bp.route("/boats/add/submit", methods=['POST'])
    def _insert_boat_in_DB():
        with get_db() as conn:
            boat_name = request.form.get("Name")
            boat_color = request.form.get("Color")
            try:
                insert_boat_in_DB(conn, boat_name, boat_color)
            except Exception:
                return render_template("form_error.html", errors=["Your insertions did not went through check your inputs again."])
        return _boats()