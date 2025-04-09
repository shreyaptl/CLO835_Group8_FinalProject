import os
from flask import Flask, render_template
import boto3
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from K8s ConfigMap and Secrets
IMAGE_URL = os.getenv('IMAGE_URL', 's3://clo835group8final/background.jpg')
TEAM_NAME = os.getenv('TEAM_NAME', 'SkyHigh Coders')
TEAM_SLOGAN = os.getenv('TEAM_SLOGAN', 'We Fly in the Cloud')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Parse S3 image path
try:
    BUCKET_NAME = IMAGE_URL.split('/')[2]  # e.g., clo835group8final
    IMAGE_KEY = '/'.join(IMAGE_URL.split('/')[3:])  # e.g., background.jpg
    LOCAL_IMAGE_PATH = 'static/background.jpg'
except IndexError:
    BUCKET_NAME = ''
    IMAGE_KEY = ''
    LOCAL_IMAGE_PATH = 'static/background.jpg'

def fetch_background_image():
    """Download background image from private S3 bucket."""
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME, IMAGE_KEY]):
        logging.warning("Missing AWS credentials or image configuration.")
        return

    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3.download_file(BUCKET_NAME, IMAGE_KEY, LOCAL_IMAGE_PATH)
        logging.info(f"✅ Background image successfully downloaded from: {IMAGE_URL}")
    except Exception as e:
        logging.error(f"Failed to fetch image from S3: {e}")

@app.route('/')
def index():
    fetch_background_image()
    return render_template('index.html', team_name=TEAM_NAME, team_slogan=TEAM_SLOGAN)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
