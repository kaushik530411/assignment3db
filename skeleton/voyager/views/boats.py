
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