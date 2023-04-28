审核运行步骤

## 初始化权限，角色，状态，动作脚本：

    python helper.py -i init

## 查看审核表中相关数据：

    python scrip_shenhe.py

## 测试时使用前台页面发布数据：

http://127.0.0.1:5555/publish/9100

## 后台页面：可操作用户，角色，权限，状态，动作

http://127.0.0.1:6796/（如需admin作为管理员，只接页面中修改用户角色）

## 前端页面：显示审核功能部分为模块

/templates/modules/post/state.html（/torcms/modules/widget_modules.py 283行）

发布后view页面可查看当前用户对应可操作动作：

例如角色为编辑者（用户名为 user_1editor,pass:Gg123456），目前只可看到'提交审核'按钮

提交审核后，角色为管理者(user_uadministrators: Gg123456)，可看到'通过'，'取消'，'拒绝'，'完成'按钮

点击'完成'后，Post更新`valid==1`列表页正常显示数据。其它按钮均对应其它状态下动作按钮

## 存在问题

提交审核或者通过，取消，拒绝，完成按钮后需刷新一下再进行操作

