from flask import Flask, render_template, request, redirect
import sqlite3

flask_app = Flask(__name__)

def connect_db():
    return sqlite3.connect("tasks.db")

@flask_app.route("/", methods=["GET","POST"])
def home():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT
    )
    """)

    if request.method == "POST":
        task = request.form["task"]
        cursor.execute("INSERT INTO tasks(task) VALUES(?)",(task,))
        conn.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    return render_template("index.html", tasks=tasks)

@flask_app.route("/delete/<int:id>")
def delete(id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()

    return redirect("/")

if __name__ == "__main__":
    flask_app.run(debug=True)