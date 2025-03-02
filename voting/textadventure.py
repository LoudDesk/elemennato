#!env/bin/python3
from flask import Flask, render_template, g, session, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
import sqlite3

class CONFIG:
    SECRET_KEY = 'jsdgfuhsadnkjawru7tw875683w9reajdknakjd'
    DEBUG = 1
    DEBUG_TB_ENABLED = 1
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DB_NAME = "textadventure.db"


app = Flask(__name__)
app.config.from_object(CONFIG)
DebugToolbarExtension(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = sqlite3.connect(CONFIG.DB_NAME)
        g._database.row_factory = sqlite3.Row
        db = g._database
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    session['score'] = 0
    return redirect( url_for('show_step') )

@app.route("/vote/<int:id>")
def voted(id):
    cursor = get_db().cursor()
    #cursor.execute("""SELECT * FROM answers WHERE id=?""", [id])
    cursor.execute("""UPDATE answers SET votes=votes+1 WHERE id=?""", [id])
    get_db().commit()
    #answer = cursor.fetchone()
    return render_template("vote.htm.j2", **locals())

@app.route("/reset_votes/")
def reset_votes():
    cursor = get_db().cursor()
    #cursor.execute("""SELECT * FROM answers WHERE id=?""", [id])
    cursor.execute("""UPDATE answers SET votes=0""")
    get_db().commit()
    #answer = cursor.fetchone()
    return render_template("vote.htm.j2")

#@app.route("/do/<int:id>/")
#def do_action(id):
#    cursor = get_db().cursor()
#    cursor.execute("""SELECT * FROM answers WHERE id=?""", [id])
#    answer = cursor.fetchone()
#
#    return redirect( url_for('show_step', id=answer['next_step_id']) )


@app.route("/idk/")
def show_step():
    cursor = get_db().cursor()
    
    cursor.execute("""SELECT * FROM steps""")
    steps = cursor.fetchall()

    cursor.execute("""SELECT * FROM answers""")
    answers = cursor.fetchall()


    return render_template("show_step.htm.j2", **locals())

if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True)
