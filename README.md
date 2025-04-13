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


#  Make sure you are using AWS CLI version 2. Use these instructions to update the AWS CLI version in your Cloud9 environment. 
```/usr/local/bin/aws –-version``` 


# Configure your permanent credentials and disable Cloud9 temporary credentials 
```/usr/local/bin/aws cloud9 update-environment --environment-id $C9_PID  --managed-credentials-action DISABLE```

```rm -vf ${HOME}/.aws/credentials``

# Use credentials from AWS Academy AWS Details and copy them into ~/.aws/credentials file

# install jq
```sudo yum -y install jq gettext bash-completion```

# Install eksctl
```curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp```
```sudo mv -v /tmp/eksctl /usr/local/bin```

# Enable eksctl bash completion
```eksctl completion bash >> ~/.bash_completion```
```. /etc/profile.d/bash_completion.sh```
```. ~/.bash_completion```
# Install kubectl
``curl -LO https://dl.k8s.io/release/v1.29.13/bin/linux/amd64/kubectl``
``chmod +x ./kubectl``
``sudo mv ./kubectl /usr/local/bin/``


# Create the cluster - these steps will take a few minutes
# Make sure to edit the eks_config and specify your Account Id in place of the [YOUR AWS ACCOUNT]

``` eksctl create cluster -f eks-config.yaml ```
``` eksctl delete cluster --name clo835-project --region us-east-1 ```

# Switch to CloudFormation service, examine the resources that are being created
# Update your kubeconfig
```aws eks update-kubeconfig --name clo835-project --region us-east-1 ```

```kubectl cluster-info```
