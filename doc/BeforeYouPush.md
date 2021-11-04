# 代码提交规范实践

以 TorCMS 开发为例进行说明。

## 开发环境建立

首先建立虚拟环境，然后安装开发依赖项：

    python3 -m venv vpy
    source vpy/bin/active
    pip install -r doc/requirements-dev.txt


## 代码检测与测试

下面各项为主要命令，不必依顺序执行。

### 代码风格检测

1. 使用 pycodestyle 进行代码风格检查，指定每行长度限制为120字符。解决掉所有问题：

    python3 -m pycodestyle -r --max-line-length=120 torcms

1. 针对所有变动的Python源文件，使用pylint进行代码风格检查。按检查结果进行修改，尽量符合编码范围。可使用 PyCharm 的代码格式化工具。所有的文件，保证文字编码为UTF-8，所有文件换行符为 LF （Linux Format）。

    python3 -m pylint path_to_file/pyfile.py

1. 使用pylint对 torcms 进行整体检查，查看是否有问题。 若有问题，继续修改代码。

    python3 -m pylint torcms
    
### 单元测试

1. 进行单元测试，如有问题，再次修改，并按上面流程重新检查。

    python3 -m pytest tester
    
### 代码提交
    
1. 使用git命令，查看所有修改的，以及新增的文件。

    git status

1. commit 代码，说明修改内容。如有新增文件，注意先添加。

    git commit -a

1. 提交修改内容。

    git push
