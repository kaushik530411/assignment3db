
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
