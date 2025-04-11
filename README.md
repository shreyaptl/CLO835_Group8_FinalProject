# Install the required MySQL package
```
sudo apt-get update -y
sudo apt-get install mysql-client -y
```

# Running application locally
```
pip3 install -r requirements.txt
python3 app.py
```
``` docker network create clo835project ```

# Building and running 2 tier web application locally
### Building mysql docker image 
```
docker build -t my_db -f Dockerfile_mysql . 
```

### Building application docker image 
```
docker build -t my_app -f Dockerfile . 
```

### Running mysql
```
docker run -d --name mysql --network clo835project -e MYSQL_ROOT_PASSWORD=db_pass123 -p 3306:3306 my_db

```

## Quick Demo Command

To quickly run the application:

1. Set up environment variables:
```bash
# Set required variables
export TEAM_NAME="CloudSprint"
export TEAM_SLOGAN="Where Ideas Take Flight"
export IMAGE_URL="s3://clo835group8final/background.jpg"
export S3_BUCKET_NAME="clo835group8final"
export S3_REGION="us-east-1" 
export LOCAL_IMAGE_PATH="/app/static/images/background.jpg"
export DBHOST=mysql
export DBPORT=3306
export DBUSER=root
export DBPWD=db_pass123
export DATABASE=employees

# Add your AWS credentials
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
export AWS_SESSION_TOKEN="your_session_token_here"
```

## Run docker command

```
docker run -d \
  -e TEAM_NAME -e TEAM_SLOGAN -e IMAGE_URL -e S3_BUCKET_NAME -e S3_REGION -e LOCAL_IMAGE_PATH \
  -e DBHOST -e DBPORT -e DBUSER -e DBPWD -e DATABASE \
  -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN \
  --network clo835project \
  -p 81:81 \
  my_app
```