from collections import namedtuple

from flask import render_template
from flask import request

from voyager.db import get_db, execute

def get_all_voyages(conn):
    return execute(conn, "SELECT v.sid, v.bid, v.date_of_voyage FROM Voyages AS v")

def get_sailors_from_date(conn, voyage_date):
    return execute(conn, 
    "SELECT DISTINCT Sailors.sid, Sailors.name  FROM (Sailors INNER JOIN Voyages ON Voyages.sid = Sailors.sid) WHERE Voyages.date_of_voyage = :v_date", {'v_date': voyage_date})

def views(bp):
    @bp.route("/voyages")
    def _get_all_voyages():
        with get_db() as conn:
            rows = get_all_voyages(conn)
        return render_template("table.html", name="voyages", rows=rows)
    
    @bp.route("/sailors/who-sailed-on-date")
    def _get_sailors_from_date():
        with get_db() as conn:
            voyage_date = request.args.get("date")
            rows = get_sailors_from_date(conn, voyage_date)
        return render_template("table.html", name="Sailors travelling on date: " + voyage_date, rows=rows)