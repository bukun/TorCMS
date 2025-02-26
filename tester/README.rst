测试说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
因之前数据表有改动，增删字段等，所以需要先运行以下命令，再进行测试。

注意： 不要在生产环境运行。


python helper.py -i reset
python helper.py -i init


python3 -m pytest tester
python3 -m pytest tester/test_model/test_collect.py
