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

def views(bp):
    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = get_all_sailors(conn)
        return render_template("table.html", name="sailors", rows=rows)