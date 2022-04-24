自建 Docker .

1. 运行 build.sh 建立 。
2. 运行 PostgreSQL

    docker run -e POSTGRES_PASSWORD=111111 -e POSTGRES_DB=torcms \
        -e POSTGRES_USER=torcms -p 54323:5432 -d postgres:12

3. 初始化：

    docker run -p 80:8888  -it  bk-torcms-debian-test \
        /vpy/bin/python3 helper.py -i init