审核运行步骤

## 初始化权限，角色，状态，动作脚本：

    sh sh_helper.sh 

## 查看审核表中相关数据：

    python scrip_shenhe.py

## 测试时使用前台页面发布数据：

http://127.0.0.1:5555/publish/9100

## 发布之后数据查看

http://127.0.0.1:5555/user/info 右侧待审核列表DATA中

## 后台页面：可操作用户，角色，权限，状态，动作

http://127.0.0.1:6796/（如需admin作为管理员，直接页面中修改用户角色）

## 前端页面：显示审核功能部分为模块

/templates/modules/post/state.html（/torcms/modules/widget_modules.py 283行）

 


