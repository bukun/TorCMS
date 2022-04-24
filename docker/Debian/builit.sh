# docker stop $(docker ps -a -q)
# docker rm $(docker ps -a -q)
docker build -t bk-torcms-debian11 .
