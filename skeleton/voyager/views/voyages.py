from collections import namedtuple

from flask import render_template
from flask import request

from voyager.db import get_db, execute

def get_all_voyages(conn):
    return execute(conn, "SELECT v.sid, v.bid, v.date_of_voyage FROM Voyages AS v")

def views(bp):
    @bp.route("/voyages")
    def _get_all_voyages():
        with get_db() as conn:
            rows = get_all_voyages(conn)
        return render_template("table.html", name="voyages", rows=rows)