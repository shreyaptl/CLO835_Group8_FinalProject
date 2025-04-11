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
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=db_pass123 -e MYSQL_DATABASE=mydb -p 3306:3306 my_db
```

### Running app
```
docker run -d --name myapp -e DBHOST=mysql -e DBPORT=3306 -e DBUSER=root -e DBPWD=db_pass123 -e DATABASE=employees -e APP_COLOR=blue -p 81:81 my_app
```
