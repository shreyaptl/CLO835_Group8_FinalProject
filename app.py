from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import boto3

app = Flask(__name__)

# Database configuration
DBHOST = os.environ.get("DBHOST") or "mysql"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "db_pass123"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT") or "3306")

# Developer name and S3 info from ConfigMap or env
TEAM_NAME = os.environ.get("TEAM_NAME", "CloudSprint")
TEAM_SLOGAN = os.environ.get("TEAM_SLOGAN", "Where Ideas Take Flight")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "clo835group8final")
OBJECT_KEY = os.environ.get("S3_OBJECT_KEY", "background.jpg")
LOCAL_IMAGE_NAME = "background.jpg"
LOCAL_IMAGE_PATH = f"static/{LOCAL_IMAGE_NAME}"

# Connect to MySQL
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)

# Download background image from S3 to static folder
def download_background_image():
    try:
        print(f"Downloading {OBJECT_KEY} from S3 bucket {BUCKET_NAME}...")
        s3 = boto3.client('s3')
        os.makedirs('static', exist_ok=True)
        s3.download_file(BUCKET_NAME, OBJECT_KEY, LOCAL_IMAGE_PATH)
        print("Background image downloaded and stored in /static/")
    except Exception as e:
        print(f"Failed to download image from S3: {e}")

# Call the image download before app starts
download_background_image()


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', bg_image=LOCAL_IMAGE_PATH)


@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', bg_image=LOCAL_IMAGE_PATH)


@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()

    return render_template('addempoutput.html', name=emp_name, owner_name=OWNER_NAME, bg_image=LOCAL_IMAGE_PATH)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", bg_image=LOCAL_IMAGE_PATH)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']
    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
    except Exception as e:
        print(e)
    finally:
        cursor.close()

    return render_template("getempoutput.html",
                           id=output["emp_id"],
                           fname=output["first_name"],
                           lname=output["last_name"],
                           interest=output["primary_skills"],
                           location=output["location"],
                           bg_image=LOCAL_IMAGE_PATH)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
