# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
from cfg import SITE_CFG

# driver = webdriver.Firefox()
# driver = webdriver.Firefox()
driver = webdriver.Chrome()
site_url = SITE_CFG['site_url']


# 测试主页面查找按钮

def test_main_page():
    driver.get(site_url)

    result = driver.find_element_by_id('keyword').is_displayed()
    driver.find_element_by_id('keyword').send_keys('ikcest')

    print(result)

    driver.find_element_by_id('search_app_submit').click()
    sleep(5)


def test_mainsearch():
    driver.get(site_url)
    driver.find_element_by_id('w1').click()
    sleep(2)
    driver.find_element_by_link_text('Info').click()
    sleep(2)
    driver.find_element_by_id('keyword').send_keys('ikcest')
    driver.find_element_by_id('search_app_submit').click()


# 注册用户


def test_regist():
    driver.get('{0}/user/regist'.format(site_url))
    driver.find_element_by_id('user_name').send_keys('drr_test226')
    driver.find_element_by_id('user_pass').send_keys('1131322')
    driver.find_element_by_id('user_pass2').send_keys('1131322')
    driver.find_element_by_id('user_email').send_keys('4788455456456@qq.com')
    driver.find_element_by_id('sub1').click()
    sleep(5)


def test_regista():
    driver.get('{0}/user/regist'.format(site_url))
    driver.find_element_by_id('user_name').send_keys('drr_test7')
    driver.find_element_by_id('user_pass').send_keys('123456')
    driver.find_element_by_id('user_pass2').send_keys('12345678')
    driver.find_element_by_id('user_email').send_keys('2145348@qq.com')
    driver.find_element_by_id('sub1').click()
    sleep(4)


def test_registb():
    driver.get('{0}/user/regist'.format(site_url))
    driver.find_element_by_id('user_name').send_keys('drr_test8')
    driver.find_element_by_id('user_pass').send_keys('123456')
    driver.find_element_by_id('user_pass2').send_keys('123456')
    driver.find_element_by_id('user_email').send_keys('2145348')
    driver.find_element_by_id('sub1').click()
    sleep(4)


# 用户登陆

def test_login():
    driver.get('{0}/user/login'.format(site_url))
    driver.find_element_by_id('user_name').clear()
    driver.find_element_by_id('user_name').send_keys('jiping')
    driver.find_element_by_id('user_pass').clear()
    driver.find_element_by_id('user_pass').send_keys('123456')
    driver.find_element_by_id('btn_login').click()
    sleep(5)


def test_logina():
    driver.get('{0}/user/login'.format(site_url))
    driver.find_element_by_id('user_name').clear()
    driver.find_element_by_id('user_name').send_keys('jiping11')
    driver.find_element_by_id('user_pass').clear()
    driver.find_element_by_id('user_pass').send_keys('j131322')
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    sleep(5)


def test_loginb():
    driver.get('{0}/user/login'.format(site_url))
    driver.find_element_by_id('user_name').clear()
    driver.find_element_by_id('user_name').send_keys('jiping')
    driver.find_element_by_id('user_pass').clear()
    driver.find_element_by_id('user_pass').send_keys('131322123')
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    sleep(5)


# 退出登陆


def test_logout():
    driver.get('{0}/user/logout'.format(site_url))


# 修改密码
def test_userinfo():
    # test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Change Password').click()
    sleep(5)


def test_changepass():
    # test_login()
    driver.get('{0}/user/changepass'.format(site_url))
    driver.find_element_by_id('password').send_keys('123456')
    driver.find_element_by_id('password1').send_keys('123456')
    driver.find_element_by_class_name('btn btn-primary').find_element_by_link_text('Modify').click()
    # driver.find_element_by_link_text("Modify").click()
    sleep(5)


def test_changepassa():
    # test_login()
    driver.get('{0}/user/changepass'.format(site_url))
    driver.find_element_by_id('password').send_keys('123456')
    driver.find_element_by_id('password1').send_keys('12345')
    driver.find_element_by_link_text("Modify").click()
    sleep(5)


def test_changepassb():
    # test_login()
    driver.get('{0}/user/changepass'.format(site_url))

    driver.find_element_by_id('password').send_keys('131322')
    driver.find_element_by_id('password1').send_keys('123456')
    driver.find_element_by_link_text("Modify").click()
    sleep(5)


# 修改个人信息
def test_userinfoa():
    # test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Modify Personal Information').click()
    sleep(5)


def test_changeinfo():
    # test_login()
    driver.get('{0}/user/changeinfo'.format(site_url))
    driver.find_element_by_id('user_email').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_trueName').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_gender').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_birthDay').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_nickName').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_mobile').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_location').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_profile').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_postalCode').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_certificateType').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_certificateNum').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_company').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_interest').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_high').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_weight').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_bloodType').send_keys('giser@osgeo.cn')
    driver.find_element_by_link_text('Modify').click()


# 退出登陆-按钮
def test_userinfod():
    # test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Logout').click()
    sleep(5)


# 添加文档
def test_userinfob():
    # test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Add Document').click()
    sleep(5)


# 个人信息
def test_userinfoc():
    # test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Publish information').click()
    sleep(5)


# 发布按钮
def test_publish():
    # test_login()
    driver.get('{0}/publish/9'.format(site_url))
    driver.find_element_by_link_text('Resources').click()
    sleep(5)


def test_publisha():
    # test_login()
    driver.get('{0}/publish/k'.format(site_url))
    sleep(5)


# 添加文档
def test_post():
    test_login()
    sleep(5)
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_id('title').send_keys('test selenium')
    driver.find_element_by_id('tags').send_keys('test tags')
    driver.find_element_by_name('pcat0').send_keys('Misc')
    driver.find_element_by_name('pcat1').send_keys('Scientific Research')
    driver.find_element_by_name('pcat2').send_keys('Engineering')
    driver.find_element_by_name('pcat3').send_keys('Education')
    driver.find_element_by_name('pcat4').send_keys('Control Flood')
    driver.find_element_by_id('logo').send_keys('/static/upload/b9/b99c9056-90ef-11e6-8e5f-6c0b8492a212_m.jpg')
    # driver.find_element_by_id('cnt_md').send_keys('absasd13124asdfasfasdfsfdasdf')
    driver.find_element_by_id('memo').send_keys('memo')
    driver.find_element_by_id('sub1').click()
    sleep(5)


# view页面各按钮
def test_postview():
    # test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_link_text('Edit').click()
    sleep(5)


# 修改文档
def test_post_edit():
    # test_login()
    driver.get('{0}/post_man/view/t0000'.format(site_url))
    driver.find_element_by_link_text('Edit').click()
    sleep(5)
    driver.find_element_by_id('title').send_keys('bdks1ea3da4d')
    driver.find_element_by_id('keywords').send_keys('bdksd')
    driver.find_element_by_name('pcat0').send_keys('Misc')
    driver.find_element_by_name('pcat1').send_keys('Scientific Research')
    driver.find_element_by_name('pcat2').send_keys('Engineering')
    driver.find_element_by_name('pcat3').send_keys('Education')
    driver.find_element_by_name('pcat4').send_keys('Control Flood')
    driver.find_element_by_id('logo').send_keys('/static/upload/b9/b99c9056-90ef-11e6-8e5f-6c0b8492a212_m.jpg')
    # driver.find_element_by_id('cnt_md').send_keys('absasd13124')
    driver.find_element_by_id('logo').send_keys(Keys.ENTER)
    sleep(5)


# 修改文档分类
def test_post_reclass():
    test_login()
    sleep(5)
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_link_text('Reclassify').click()
    sleep(5)
    kind = Select(driver.find_element_by_id('kcat'))
    kind.select_by_value("k")
    driver.find_element_by_name('pcat0').send_keys('National')
    driver.find_element_by_id('sub1').click()


# 查看文档按钮。
def test_post_view():
    # test_login()
    driver.get('{0}/post_man/view/t0000'.format(site_url))
    driver.find_element_by_link_text('View').click()
    sleep(5)


# 收藏
def test_post_collect():
    test_login()
    sleep(5)
    driver.get('{0}/post/14c95'.format(site_url))
    driver.find_element_by_id('text_collect').click()
    sleep(5)


# 添加page
def test_page():
    # test_login()
    driver.get('{0}/page/t0000'.format(site_url))
    driver.find_element_by_id('title').send_keys('erfefsadfefasdfe')
    driver.find_element_by_id('cnt_md').send_keys('absasd13124')
    driver.find_element_by_id('sub1').click()
    sleep(5)


def test_page_edit():
    # test_login()
    driver.get('{0}/page/_edit/t0000'.format(site_url))
    driver.find_element_by_id('title').send_keys('e1111111rfefsadfefasdfe')
    driver.find_element_by_id('cnt_md').send_keys('1111111absasd13124')
    driver.find_element_by_id('sub1').click()
    sleep(5)


# 添加info

def test_info():
    test_login()
    sleep(5)
    driver.get('{0}/info/_cat_add/2201'.format(site_url))
    driver.find_element_by_id("title").send_keys('kldfkeji')
    driver.find_element_by_id('tags').send_keys('sfef')
    driver.find_element_by_id('logo').send_keys('/static/upload/b9/b99c9056-90ef-11e6-8e5f-6c0b8492a212_m.jpg')
    driver.find_element_by_xpath("//textarea[@id='cnt_md']").send_keys('coasasdsdnte1131321321513201531302313151nt')

    s1 = Select(driver.find_element_by_id('tag_lang'))
    s1.select_by_value("2")
    s2 = Select(driver.find_element_by_id('tag_data_format'))
    s2.select_by_value("1")
    s3 = Select(driver.find_element_by_id('tag_subject'))
    s3.select_by_value("3")
    s4 = Select(driver.find_element_by_id('tag_generation'))
    s4.select_by_value("1")
    s5 = Select(driver.find_element_by_id('tag_grade'))
    s5.select_by_value("4")
    s6 = Select(driver.find_element_by_id('tag_serial'))
    s6.select_by_value("1")
    s7 = Select(driver.find_element_by_id('tag_temperal'))
    s7.select_by_value("2")
    s8 = Select(driver.find_element_by_id('tag_spatial'))
    s8.select_by_value("1")
    s9 = Select(driver.find_element_by_id('tag_resolution'))
    s9.select_by_value("2")
    s10 = Select(driver.find_element_by_id('tag_share_type'))
    s10.select_by_value("1")
    s11 = Select(driver.find_element_by_id('tag_access'))
    s11.select_by_value("4")

    driver.find_element_by_id('memo').send_keys('14')
    driver.find_element_by_id('Button1').click()
    sleep(5)


# 修改信息
def test_info_edit():
    test_login()
    sleep(5)
    driver.get('{0}/info/_edit/9b2d3'.format(site_url))
    driver.find_element_by_id('title').send_keys('kldfkeji')
    driver.find_element_by_id('tags').send_keys('sfef')
    driver.find_element_by_id('logo').send_keys('/static/upload/b9/b99c9056-90ef-11e6-8e5f-6c0b8492a212_m.jpg')

    s1 = Select(driver.find_element_by_id('tag_lang'))
    s1.select_by_value("2")
    s2 = Select(driver.find_element_by_id('tag_data_format'))
    s2.select_by_value("1")
    s3 = Select(driver.find_element_by_id('tag_subject'))
    s3.select_by_value("3")
    s4 = Select(driver.find_element_by_id('tag_generation'))
    s4.select_by_value("1")
    s5 = Select(driver.find_element_by_id('tag_grade'))
    s5.select_by_value("4")
    s6 = Select(driver.find_element_by_id('tag_serial'))
    s6.select_by_value("1")
    s7 = Select(driver.find_element_by_id('tag_temperal'))
    s7.select_by_value("2")
    s8 = Select(driver.find_element_by_id('tag_spatial'))
    s8.select_by_value("1")
    s9 = Select(driver.find_element_by_id('tag_resolution'))
    s9.select_by_value("2")
    s10 = Select(driver.find_element_by_id('tag_share_type'))
    s10.select_by_value("1")
    s11 = Select(driver.find_element_by_id('tag_access'))
    s11.select_by_value("4")

    driver.find_element_by_id('cnt_md').send_keys('content')
    driver.find_element_by_id('memo').send_keys('14')
    driver.find_element_by_id('Button1').click()
    sleep(5)


def test_infoa():
    # test_login()
    driver.get('{0}/info/t0000'.format(site_url))
    driver.find_element_by_link_text('Edit').click()
    sleep(5)


def test_infob():
    # test_login()
    driver.get('{0}/info/t0000'.format(site_url))
    driver.find_element_by_link_text('Delete').click()
    sleep(5)


def test_infoc():
    # test_login()
    driver.get('{0}/info/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('水').click()
    sleep(5)


def test_infod():
    # test_login()
    driver.get('{0}/info/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Reclassify').click()
    sleep(5)


def test_infoe():
    # test_login()
    driver.get('{0}/info/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Review').click()
    sleep(5)


# post_man页

def test_post_man():
    # test_login()
    driver.get('{0}/post_man/view/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Edit').click()
    sleep(4)


def test_post_mana():
    # test_login()
    driver.get('{0}/post_man/view/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('View').click()
    sleep(4)


def test_postli():
    # test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Edit').click()
    sleep(4)


def test_postlia():
    # test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Reclassify').click()
    sleep(4)


# user_list

def test_user_recent():
    # test_login()
    driver.get('{0}/user_list/user_recent'.format(site_url))
    driver.find_element_by_id('tab2').click()
    sleep(4)


def test_comment():
    test_login()
    driver.get('{0}/post/1aef9'.format(site_url))
    driver.find_element_by_id('cnt_reply').send_keys('我来评论，哈哈哈！')

    # driver.find_element_by_link_text("Submit").click()
    driver.find_element_by_xpath("//a[contains(@onclick, 'reply_it')]").click()


if __name__ == '__main__':
    # test_main_page()
    # test_mainsearch()
    # test_regist()
    # test_regista()
    # test_registb()
    # test_login()
    # test_logina()
    # test_loginb()
    # test_userinfo()
    # test_userinfoa()
    # test_userinfob()
    # test_userinfoc()
    # test_userinfod()
    # test_logout()
    # test_login()
    # test_changepass()
    # test_changepassa()
    # test_changepassb()
    # test_publish()
    # test_publisha()
    # test_post()
    test_post_collect()
    # test_postview()
    # test_post_reclass()
    # test_post_edit()
    # test_post_view()

    # test_page()
    # test_page_edit()
    # test_info()
    # test_info_edit()
    # test_changeinfo()
    # test_infoa()
    # test_infob()
    # test_infoc()
    # test_infod()
    # test_infoe()
    # test_post_man()
    # test_post_mana()
    # test_postli()
    # test_postlia()
    # test_user_recent()
    # test_comment()
