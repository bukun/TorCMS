测试说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
因之前数据表有改动，增 删字段等，所以需要先运行以下命令，再进行测试。


python helper.py -i drop_tables
python helper.py -i init


python3 -m pytest tester