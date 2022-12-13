git 使用


##  彻底删除git中历史文件夹

有些时候不小心上传了一些敏感文件(例如密码), 或者不想上传的文件(没及时或忘了加到.gitignore里的),
而且上传的文件又特别大的时候, 这将导致别人clone你的代码或下载zip包的时候也必须更新或下载这些无用的文件,
因此, 我们需要一个方法, 永久的删除这些文件(包括该文件的历史记录).

先设置要彻底删除的文件夹名称


    export to_remove_path=to_remove
    git filter-branch --force --index-filter 'git rm -rf --cached --ignore-unmatch $to_remove_path' --prune-empty --tag-name-filter cat -- --all

    ###############
    rm -rf .git/refs/original/
    git reflog expire --expire=now --all
    git gc --prune=now

    #######################
    git push origin master --force