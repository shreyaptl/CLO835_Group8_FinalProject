import os
import boto3
import logging
from flask import Flask, render_template, request, send_file
from pymysql import connections, err

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Environment/config
IMAGE_URL = os.getenv('IMAGE_URL', 's3://clo835group8final/project-image.jpg')
TEAM_NAME = os.getenv('TEAM_NAME', 'SkyHigh Coders')
TEAM_SLOGAN = os.getenv('TEAM_SLOGAN', 'We Fly in the Cloud')
STUDENT_NAME = os.getenv('STUDENT_NAME', 'Shailendra Kushwaha')

MYSQL_HOST = os.getenv('DBHOST', 'localhost')
MYSQL_PORT = int(os.getenv('DBPORT', '3306'))
MYSQL_USER = os.getenv('DBUSER', 'root')
MYSQL_PASSWORD = os.getenv('DBPWD', 'yourpassword')
DATABASE = os.getenv('DATABASE', 'employees')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Parse bucket + key
BUCKET_NAME = IMAGE_URL.split('/')[2]
IMAGE_KEY = '/'.join(IMAGE_URL.split('/')[3:])
S3_IMAGE_FILENAME = IMAGE_KEY.split('/')[-1]

# MySQL connection
try:
    db_conn = connections.Connection(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=DATABASE
    )
    logging.info(" Connected to MySQL")
except err.OperationalError as e:
    logging.error(f" MySQL connection error: {e}")
    db_conn = None

# S3 download handler
def download_image_from_s3(bucket, key, local_filename):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        s3.download_file(bucket, key, local_filename)
        logging.info(f" Downloaded image from S3: {bucket}/{key}")
        return local_filename
    except Exception as e:
        logging.error(f" Failed to download image: {e}")
        return None

@app.route("/download/<filename>")
def download(filename):
    local_path = f"/tmp/{filename}"
    if download_image_from_s3(BUCKET_NAME, IMAGE_KEY, local_path):
        return send_file(local_path, mimetype='image/jpeg')
    return "Image not found", 500

@app.route("/", methods=["GET"])
def home():
    return render_template("addemp.html",
                           image_url=f"/download/{S3_IMAGE_FILENAME}",
                           team_name=TEAM_NAME,
                           team_slogan=TEAM_SLOGAN,
                           student_name=STUDENT_NAME)

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html",
                           image_url=f"/download/{S3_IMAGE_FILENAME}",
                           team_name=TEAM_NAME,
                           team_slogan=TEAM_SLOGAN,
                           student_name=STUDENT_NAME)

@app.route("/addemp", methods=["POST"])
def AddEmp():
    if not db_conn:
        return "Database not connected", 500

    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    try:
        cursor = db_conn.cursor()
        insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        logging.info(" Employee inserted")
    except Exception as e:
        logging.error(f" Insert failed: {e}")
        return "Error inserting data", 500
    finally:
        cursor.close()

    return render_template("addempout.html",
                           image_url=f"/download/{S3_IMAGE_FILENAME}",
                           team_name=TEAM_NAME,
                           team_slogan=TEAM_SLOGAN,
                           student_name=STUDENT_NAME)

@app.route("/getemp", methods=["GET", "POST"])
def GetEmp():
    return render_template("getemp.html",
                           image_url=f"/download/{S3_IMAGE_FILENAME}",
                           team_name=TEAM_NAME,
                           team_slogan=TEAM_SLOGAN,
                           student_name=STUDENT_NAME)

@app.route("/fetchdata", methods=["POST"])
def FetchData():
    if not db_conn:
        return "Database not connected", 500

    emp_id = request.form.get('emp_id')
    output = {}

    try:
        cursor = db_conn.cursor()
        select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        logging.info(f" Result for emp_id={emp_id}: {result}")

        if not result:
            return f"No employee found with ID {emp_id}", 404

        # Map result to named output fields
        output["emp_id"], output["first_name"], output["last_name"], output["primary_skills"], output["location"] = result

    except Exception as e:
        logging.error(f" Fetch error: {e}")
        return f"Error fetching employee data: {e}", 500
    finally:
        cursor.close()

    return render_template("getempout.html",
                           id=output["emp_id"],
                           fname=output["first_name"],
                           lname=output["last_name"],
                           interest=output["primary_skills"],
                           location=output["location"],
                           image_url=f"/download/{S3_IMAGE_FILENAME}",
                           team_name=TEAM_NAME,
                           team_slogan=TEAM_SLOGAN,
                           student_name=STUDENT_NAME)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
