GitHub中TorCMS代码提交操作规范
=================================


1. 对代码进行单元测试，如有问题，进行修改。

    nosetests3 -v -d --exe tester

1. 使用git命令，查看所有修改的，以及新增的文件。

    git status

1. 针对所有变动的Python源文件，使用pylint进行代码风格检查。按检查结果进行修改，尽量符合编码范围。可使用 PyCharm 的代码格式化工具。所有的文件，保证文字编码为UTF-8，所有文件换行符为 LF （Linux Format）。

    pylint path_to_file/pyfile.py

1. 使用pylint对 torcms 进行整体检查，查看是否有问题。 若有问题，继续修改代码。

    pylint torcms

1. 再次进行单元测试，如有问题，再次修改，并按上面流程重新检查。

    nosetests3 -v -d --exe tester

1. commit 代码，说明修改内容。如有新增文件，注意先添加。

    git commit -a

1. 提交修改内容。

    git push
