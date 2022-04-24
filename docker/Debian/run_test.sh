# docker stop $(docker ps -a -q)
# docker rm $(docker ps -a -q)

docker run -e POSTGRES_PASSWORD=111111 -e POSTGRES_DB=torcms \
  -e POSTGRES_USER=torcms -p 54323:5432 -d postgres:12
docker run -p 80:8888  -it  bk-torcms-debian11 \
  /vpy/bin/python3 helper.py -i init
docker run -p 80:8888  -it  bk-torcms-debian11 \
  /vpy/bin/python3 -m pytest tester

