from flask import Flask, render_template, request, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        userDetails = request.json
        name = userDetails['name']
        email = userDetails['email']
        alreadyExists = get_one(name)
        if alreadyExists is None:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users VALUES(%s, %s)", (name, email))
            mysql.connection.commit()
            cur.close()

            return make_response({
                "status": True,
                "massage": 'successfully added'
            })

        return make_response({
            "status": False,
            "massage": 'user already exists'
        })


@app.route('/delete_user/<string:name>', methods=['DELETE'])
def delete(name):
    result = get_one(name)
    if result is not None:
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE FROM users WHERE name = '{name}'")
        mysql.connection.commit()
        cur.close()

        return make_response({
            "status": True,
            "massage": 'successfully deleted'
        })
    return make_response({
        "status": False,
        "massage": 'deleted fail so user not found'
    })


@app.route('/update_user', methods=['PUT'])
def update_user():
    if request.method == 'PUT':
        userDetails = request.json
        result = get_one(userDetails['name'])
        if result is not None:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET email = %s WHERE name = %s", (userDetails['email'], userDetails['name']))
            mysql.connection.commit()
            cur.close()

            return make_response({
                "status": True,
                "massage": 'successfully updated'
            })
        return make_response({
            "status": False,
            "massage": 'Update fail so user not found'
        })


@app.route('/getAll_users', methods=['GET'])
def get_all_users():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        if result.__len__() == 0:
            return make_response({
                "status": False,
                "massage": "users are not here"
            })

        mysql.connection.commit()
        cur.close()
        return make_response({
            "status": True,
            "data": result
        })


@app.route('/get_user/<string:name>', methods=['GET'])
def get_user(name):
    if request.method == 'GET':
        result = get_one(name)
        if result is not None:
            return make_response({
                "status": True,
                "data": result
            })
        return make_response({
            "status": False,
            "massage": 'the name can not find'
        })


def get_one(name):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE name = '{name}'")
    result = cur.fetchone()
    mysql.connection.commit()
    cur.close()

    return result


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, port=3030) //modified port
