sudo docker build -t pollution .
sudo docker run --rm -p 5000:5000 --name pollution pollution
