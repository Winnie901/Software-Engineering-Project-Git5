from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'dbbikes.cvvkn6jkfbdf.eu-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'SEGroup25'
app.config['MYSQL_PASSWORD'] = 'SEGroup25?'
app.config['MYSQL_DB'] = 'dbbikes'
app.config['MYSQL_PORT'] = 3306

# create a connection to the database
conn = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    port=app.config['MYSQL_PORT'],
    cursorclass=pymysql.cursors.DictCursor

)


@app.route('/')
def index():
    cursor = conn.cursor()

    # execute a query
    cursor.execute('SELECT time FROM weather')

    # fetch the data
    data = cursor.fetchall()

    # close the cursor and connection
    cursor.close()
    conn.close()
    print(str(data))
    # return the data to the user
    return str(data)



@app.route('/mapping')
def map():
    cursor = conn.cursor()

    # execute a query
    cursor.execute('SELECT * FROM stations')

    # fetch the data
    data = cursor.fetchall()

    # close the cursor and connection
    cursor.close()
    conn.close()
    print(str(data))

    # return the data to the user
    return render_template('mapping.html', stations=data)




# @app.route('/')

if __name__ == "__main__":
    app.run()