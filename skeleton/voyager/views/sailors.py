from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def get_all_sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

def get_sailors_from_boat_name(conn, boat_name):
    return execute(conn, 
    "SELECT DISTINCT Sailors.sid, Sailors.name  FROM ((Voyages INNER JOIN Boats ON Voyages.bid = Boats.bid) INNER JOIN Sailors ON Voyages.sid = Sailors.sid) WHERE Boats.name = :b_name", {'b_name': boat_name})

def get_sailors_from_boat_color(conn, boat_color):
    return execute(conn, 
    "SELECT DISTINCT Sailors.sid, Sailors.name  FROM ((Voyages INNER JOIN Boats ON Voyages.bid = Boats.bid) INNER JOIN Sailors ON Voyages.sid = Sailors.sid) WHERE Boats.color = :b_color", {'b_color': boat_color})
    

def views(bp):
    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = get_all_sailors(conn)
        return render_template("table.html", name="sailors", rows=rows)
    
    @bp.route("/sailors/who-sailed")
    def _get_sailors_from_boat_name():
        with get_db() as conn:
            boat_name = request.args.get('boat-name')
            rows = get_sailors_from_boat_name(conn, boat_name)
        return render_template("table.html", name="Sailors who sailed boat: " + boat_name, rows=rows)

    @bp.route("/sailors/who-sailed-on-boat-of-color")
    def _get_sailors_from_boat_color():
        with get_db() as conn:
            boat_color = request.args.get('color')
            rows = get_sailors_from_boat_color(conn, boat_color)
        return render_template("table.html", name="Sailors who sailed boat color: " + boat_color, rows=rows)

    @bp.route("/sailors/add", methods=['POST', 'GET'])
    def _add_sailors():
        atrributes = {"Name" : "text", "age": "number", "experience": "number" }
        return render_template("form.html", name="Add Sailors: ", URI="/sailors/add/submit",  submit_message="Add Sailors", atrributes=atrributes)
