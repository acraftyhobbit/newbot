docker build -t craftybot:latest .

docker run -p 4000:8000 -e ENVIRONMENT='local' craftybot:latest /apps/deployment/startup/app.sh