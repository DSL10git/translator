REMOTE_SERVER=ubuntu@ec2-54-188-57-227.us-west-2.compute.amazonaws.com
KEY_FILE=/Users/dandan/.ssh/test.pem

# Copy a file to remote server
LOCAL_FILE=main.py
REMOTE_LOCATION=/home/ubuntu/projects/chatbot
scp -i $KEY_FILE $LOCAL_FILE $REMOTE_SERVER:$REMOTE_LOCATION
