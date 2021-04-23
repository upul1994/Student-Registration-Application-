from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "flash messages"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_PORT"] =  3307
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "flaskcrud"

mysql = MySQL(app)


@app.route("/")
def Index():
    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM students')
    fetchdata = cur.fetchall()
    cur.close()
    return render_template("index.html", data=fetchdata)


@app.route("/insert", methods=["POST"])
def Insert():
    flash("Data inserted Successful")

    name = request.form["names"]
    email = request.form["emails"]
    phone = request.form["phones"]

    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO students(name,email,phone) VALUES(%s,%s,%s)", (name, email, phone))

    mysql.connection.commit()

    return redirect(url_for("Index"))



@app.route("/update", methods=["POST", "GET"])
def Update():
    if request.method == "POST":
        flash("Data Updated Successfully")
        id_data = request.form["id"]
        name = request.form["names"]
        email = request.form["emails"]
        phone = request.form["phones"]

        curs = mysql.connection.cursor()
        curs.execute("UPDATE students SET name=%s,email=%s,phone=%s WHERE id=%s", (name, email, phone, id_data))

        mysql.connection.commit()
        return redirect(url_for("Index"))


@app.route("/delete/<string:id_data>", methods=["POST", "GET"])
def delete(id_data):
    flash("Data deleted successful")
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM students WHERE id=%s", id_data)
    mysql.connection.commit()
    return redirect(url_for("Index"))




if __name__ == "__main__":
    app.run(debug=True)
