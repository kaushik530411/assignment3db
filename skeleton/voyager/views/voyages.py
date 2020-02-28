from collections import namedtuple

from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for


from voyager.db import get_db, execute

def get_all_voyages(conn):
    return execute(conn, "SELECT v.sid, v.bid, v.date_of_voyage FROM Voyages AS v")

def get_sailors_from_date(conn, voyage_date):
    return execute(conn, 
    "SELECT DISTINCT Sailors.sid, Sailors.name  FROM (Sailors INNER JOIN Voyages ON Voyages.sid = Sailors.sid) WHERE Voyages.date_of_voyage = :v_date", {'v_date': voyage_date})

def insert_voyages_in_DB(conn, sid, bid, date):
    return execute(conn,
    "INSERT INTO Voyages (sid, bid, date_of_voyage) VALUES (:sid, :bid, :date);", {'sid': sid, "bid": bid, "date": date}
    )

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

    @bp.route("/voyages/add", methods=['POST', 'GET'])
    def _add_voyages():
        atrributes = {"Sid" : "number", "Bid": "number", "Date": "text" }
        return render_template("form.html", name="Add Voyages: ", URI="/voyages/add/submit",  submit_message="Add", atrributes=atrributes)
    
    @bp.route("/voyages/add/submit", methods=['POST'])
    def _insert_voyages_in_DB():
        with get_db() as conn:
            sid = request.form.get("Sid")
            bid = request.form.get("Bid")
            date = request.form.get("Date")
            try:
                insert_voyages_in_DB(conn, sid, bid, date)
            except Exception:
                return render_template("form_error.html", errors=["Your insertions did not went through check your inputs again."])
        return _get_all_voyages()
    
