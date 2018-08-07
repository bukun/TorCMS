# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
from cfg import SITE_CFG



driver = webdriver.Firefox()
site_url = SITE_CFG['site_url']


class Login():
    '''另外帐号登陆'''
    def login(self,driver):
        driver.get('{0}/user/login'.format(site_url))
        driver.find_element_by_id('user_name').clear()
        driver.find_element_by_id('user_name').send_keys('gislite')
        driver.find_element_by_id('user_pass').clear()
        driver.find_element_by_id('user_pass').send_keys('131322')
        driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
        sleep(5)




def test_main_page():
    '''
        测试搜索功能
        直接输入关键字搜索
        '''
    driver.get(site_url)

    result = driver.find_element_by_id('keyword').is_displayed()
    driver.find_element_by_id('keyword').send_keys('ikcest')

    print(result)

    driver.find_element_by_id('keyword').send_keys(Keys.ENTER)
    sleep(5)






def test_regist():
    '''
        测试注册用户功能
        正常输入
        '''
    driver.get('{0}/user/regist'.format(site_url))
    driver.find_element_by_id('user_name').send_keys('tor_test226')
    driver.find_element_by_id('user_pass').send_keys('1131322')
    driver.find_element_by_id('user_pass2').send_keys('1131322')
    driver.find_element_by_id('user_email').send_keys('478845545645@qq.com')
    driver.find_element_by_id('sub1').click()
    sleep(5)


def test_regista():
    '''
        测试注册用户功能
        两次密码不一致
        '''
    driver.get('{0}/user/regist'.format(site_url))
    driver.find_element_by_id('user_name').send_keys('tor_test7')
    driver.find_element_by_id('user_pass').send_keys('123456')
    driver.find_element_by_id('user_pass2').send_keys('12345678')
    driver.find_element_by_id('user_email').send_keys('2145348@qq.com')
    driver.find_element_by_id('sub1').click()
    sleep(4)


def test_registb():
    '''
        测试注册用户功能
        输入错误邮箱格式
        '''

    driver.get('{0}/user/regist'.format(site_url))
    driver.find_element_by_id('user_name').send_keys('tor_test8')
    driver.find_element_by_id('user_pass').send_keys('123456')
    driver.find_element_by_id('user_pass2').send_keys('123456')
    driver.find_element_by_id('user_email').send_keys('2145348')
    driver.find_element_by_id('sub1').click()
    sleep(4)




def test_login():
    '''
       测试用户登陆
       正常登陆
       '''
    driver.get('{0}/user/login'.format(site_url))
    driver.find_element_by_id('user_name').clear()
    driver.find_element_by_id('user_name').send_keys('giser')
    driver.find_element_by_id('user_pass').clear()
    driver.find_element_by_id('user_pass').send_keys('131322')
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    sleep(2)


def test_logina():
    '''
        测试用户登陆
        输入错误用户名
        '''
    driver.get('{0}/user/login'.format(site_url))
    driver.find_element_by_id('user_name').clear()
    driver.find_element_by_id('user_name').send_keys('jiping11')
    driver.find_element_by_id('user_pass').clear()
    driver.find_element_by_id('user_pass').send_keys('j131322')
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    sleep(5)


def test_loginb():
    '''
       测试用户登陆
       输入错误密码
       '''
    driver.get('{0}/user/login'.format(site_url))
    driver.find_element_by_id('user_name').clear()
    driver.find_element_by_id('user_name').send_keys('giser')
    driver.find_element_by_id('user_pass').clear()
    driver.find_element_by_id('user_pass').send_keys('131322123')
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    sleep(5)





def test_logout():
    '''
        用户退出登陆
        '''
    test_login()
    driver.get('{0}/user/logout'.format(site_url))



def test_userinfo():
    '''
        用户中心
        修改密码按钮
        '''
    test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Change Password').click()
    sleep(5)


def test_changepass():
    '''
        修改密码
        '''
    test_login()
    driver.get('{0}/user/changepass'.format(site_url))
    driver.find_element_by_id('rawpass').send_keys('131322')
    driver.find_element_by_id('user_pass').send_keys('123456')
    driver.find_element_by_id('user_pass2').send_keys('123456')
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    # driver.find_element_by_link_text("Modify").click()
    sleep(5)


def test_changepassa():
    '''
        修改密码
        两次密码输入不一致
        '''
    test_login()
    driver.get('{0}/user/changepass'.format(site_url))
    driver.find_element_by_id('rawpass').send_keys('131322')
    driver.find_element_by_id('user_pass').send_keys('123456')
    driver.find_element_by_id('user_pass2').send_keys('12345')
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    sleep(5)


def test_changepassb():
    '''
      修改密码
      两次密码输入不一致
      '''
    test_login()
    driver.get('{0}/user/changepass'.format(site_url))
    driver.find_element_by_id('rawpass').send_keys('131322')
    driver.find_element_by_id('user_pass').send_keys('131322')
    driver.find_element_by_id('user_pass2').send_keys('123456')
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
    sleep(5)



def test_userinfoa():
    '''
        用户中心
        修改个人信息按钮
        '''
    test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Modify Personal Information').click()
    sleep(5)


def test_changeinfo():
    '''
       修改个人信息
       '''
    test_login()
    driver.get('{0}/user/changeinfo'.format(site_url))
    driver.find_element_by_id('rawpass').send_keys('131322')
    driver.find_element_by_id('user_email').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_truename').send_keys('giser')
    s1 = Select(driver.find_element_by_id('def_gender'))
    s1.select_by_value("Female")
    driver.find_element_by_id('def_birthday').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_mobile').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_location').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_profile').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_postalcode').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_certificatetype').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_certificate').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_company').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_interest').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_high').send_keys('giser@osgeo.cn')
    driver.find_element_by_id('def_weight').send_keys('giser@osgeo.cn')
    s1 = Select(driver.find_element_by_id('def_bloodtype'))
    s1.select_by_value("B")
    driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()



def test_userinfod():
    '''
        用户中心
        退出功能
        '''
    test_login()
    driver.get('{0}/user/info'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Logout').click()
    sleep(5)



def test_userinfob():
    '''
        用户中心
        添加文档功能
        '''
    test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Add Document').click()
    sleep(5)



def test_userinfoc():
    '''
       用户中心
       发布信息功能
       '''

    test_login()
    driver.get('{0}/user/info'.format(site_url))
    driver.find_element_by_link_text('Publish Info').click()
    sleep(5)



def test_publish():
    '''
      用户中心
      发布信息 - 选择对应一级分类之后。
      '''

    test_login()
    driver.get('{0}/publish/9'.format(site_url))
    driver.find_element_by_link_text('Temperature').click()
    sleep(5)


def test_post():
    '''
      添加文档
      指定文档ID ： t0000 方式添加。
      '''
    test_login()
    sleep(5)
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_id('title').send_keys('test selenium')
    driver.find_element_by_id('tags').send_keys('test tags')
    driver.find_element_by_name('pcat0').send_keys('Principle')
    driver.find_element_by_name('pcat1').send_keys('Technology')
    driver.find_element_by_name('pcat2').send_keys('Education')
    driver.find_element_by_name('pcat3').send_keys('Major')
    driver.find_element_by_name('pcat4').send_keys('Resources')
    driver.find_element_by_id('logo').send_keys('/static/upload/b9/b99c9056-90ef-11e6-8e5f-6c0b8492a212_m.jpg')
    #driver.find_element_by_xpath("//textarea[@id='cnt_md']").send_keys('coasasdsdnte1131321321513201531302313151nt')
    # driver.find_element_by_id('memo').send_keys('memo')
    driver.find_element_by_id('sub1').click()
    sleep(5)



def test_postview():
    '''
       查看文档
       编辑按钮
       '''
    test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_link_text('Edit').click()
    sleep(5)


def test_post_edit():
    '''
       Review 后修改文档
       '''

    test_login()
    driver.get('{0}/post_man/view/t0000'.format(site_url))
    driver.find_element_by_link_text('Edit').click()
    sleep(5)
    driver.find_element_by_id('title').send_keys('bdks1ea3da4d')
    # driver.find_element_by_id('keywords').send_keys('bdksd')
    driver.find_element_by_name('pcat0').send_keys('Major')
    driver.find_element_by_name('pcat1').send_keys('Education')
    driver.find_element_by_name('pcat2').send_keys('Principle')
    driver.find_element_by_name('pcat3').send_keys('Resources')
    driver.find_element_by_name('pcat4').send_keys('Technology')
    driver.find_element_by_id('logo').send_keys('/static/upload/b9/b99c9056-90ef-11e6-8e5f-6c0b8492a212_m.jpg')
    sleep(2)
    # content= driver.find_element_by_xpath("//textarea[@id='cnt_md']")
    # if content:
    #     print('s')
    # content.send_keys('coasasdsdnte1131321321513201531302313151nt')
    driver.find_element_by_id('logo').send_keys(Keys.ENTER)
    sleep(5)



def test_post_reclass():
    '''
        修改文档大分类
        '''
    test_login()
    sleep(5)
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_link_text('Reclassify').click()
    sleep(5)
    kind = Select(driver.find_element_by_id('kcat'))
    kind.select_by_value("9")
    driver.find_element_by_name('pcat0').send_keys('Nature Geographic')
    driver.find_element_by_id('sub1').click()



def test_post_view():
    '''
        Review 后，查看文档按钮。
        '''
    # test_login()
    driver.get('{0}/post_man/view/t0000'.format(site_url))
    driver.find_element_by_link_text('View').click()
    sleep(5)



def test_post_collect():
    '''
       收藏文档
       '''
    test_login()
    sleep(5)
    driver.get('{0}/post/14c95'.format(site_url))
    driver.find_element_by_id('text_collect').click()
    sleep(5)



def test_page():
    '''
      添加page页面
      指定page  slug：t0000
      '''
    test_login()
    driver.get('{0}/page/t0000'.format(site_url))
    driver.find_element_by_id('title').send_keys('erfefsadfefasdfe')
    #driver.find_element_by_xpath("//textarea[@id='cnt_md']").send_keys('coasasdsdnte1131321321513201531302313151nt')
    driver.find_element_by_id('sub1').click()
    sleep(5)


def test_page_edit():
    '''
          修改page页面
          '''
    test_login()
    driver.get('{0}/page/_edit/t0000'.format(site_url))
    driver.find_element_by_id('title').send_keys('e1111111rfefsadfefasdfe')
    #driver.find_element_by_xpath("//textarea[@id='cnt_md']").send_keys('coasasdsdnte1131321321513201531302313151nt')
    driver.find_element_by_id('sub1').click()
    sleep(5)




def test_info():
    '''
       整体测试添加信息。
       '''

    test_login()
    sleep(5)
    driver.get('{0}/info/_cat_add/8101'.format(site_url))
    driver.find_element_by_id("title").send_keys('kldfkeji')
    driver.find_element_by_id('tags').send_keys('sfef')
    driver.find_element_by_id('logo').send_keys('/static/upload/b9/b99c9056-90ef-11e6-8e5f-6c0b8492a212_m.jpg')
    #driver.find_element_by_xpath("//textarea[@id='cnt_md']").send_keys('coasasdsdnte1131321321513201531302313151nt')

    s1 = Select(driver.find_element_by_id('tag__record'))
    s1.select_by_value("2")
    s2 = Select(driver.find_element_by_id('tag__derive'))
    s2.select_by_value("1")
    s3 = Select(driver.find_element_by_id('tag__temperal'))
    s3.select_by_value("3")
    s4 = Select(driver.find_element_by_id('tag__spatial'))
    s4.select_by_value("1")
    s5 = Select(driver.find_element_by_id('tag__from_projct'))
    s5.select_by_value("2")
    s6 = Select(driver.find_element_by_id('tag__share_type'))
    s6.select_by_value("1")
    s7 = Select(driver.find_element_by_id('tag__storage'))
    s7.select_by_value("2")
    s8 = Select(driver.find_element_by_id('tag__view_class'))
    s8.select_by_value("1")
    s9 = Select(driver.find_element_by_id('tag__paper_type'))
    s9.select_by_value("2")
    s10 = Select(driver.find_element_by_id('tag__media_type'))
    s10.select_by_value("1")

    driver.find_element_by_id('Button1').click()
    sleep(5)



def test_info_edit():
    '''
        整体测试修改信息。
        '''
    test_login()
    sleep(5)
    driver.get('{0}/info/_edit/928b3'.format(site_url))
    driver.find_element_by_id('title').send_keys('kldfkeji')
    driver.find_element_by_id('tags').send_keys('sfef')
    driver.find_element_by_id('logo').send_keys('/static/upload/b9/b99c9056-90ef-11e6-8e5f-6c0b8492a212_m.jpg')

    s1 = Select(driver.find_element_by_id('tag__record'))
    s1.select_by_value("2")
    s2 = Select(driver.find_element_by_id('tag__derive'))
    s2.select_by_value("1")
    s3 = Select(driver.find_element_by_id('tag__temperal'))
    s3.select_by_value("3")
    s4 = Select(driver.find_element_by_id('tag__spatial'))
    s4.select_by_value("1")
    s5 = Select(driver.find_element_by_id('tag__from_projct'))
    s5.select_by_value("2")
    s6 = Select(driver.find_element_by_id('tag__share_type'))
    s6.select_by_value("1")
    s7 = Select(driver.find_element_by_id('tag__storage'))
    s7.select_by_value("2")
    s8 = Select(driver.find_element_by_id('tag__view_class'))
    s8.select_by_value("1")
    s9 = Select(driver.find_element_by_id('tag__paper_type'))
    s9.select_by_value("2")
    s10 = Select(driver.find_element_by_id('tag__media_type'))
    s10.select_by_value("1")

    # driver.find_element_by_id('cnt_md').send_keys('content')
    # driver.find_element_by_id('memo').send_keys('14')
    driver.find_element_by_id('Button1').click()
    sleep(5)


def test_infoa():
    '''
        测试信息页面
        修改
        '''
    test_login()
    driver.get('{0}/info/9705c'.format(site_url))
    driver.find_element_by_link_text('Edit').click()
    sleep(5)


def test_infob():
    '''
        测试信息页面
        删除
        '''
    test_login()
    driver.get('{0}/info/9705c'.format(site_url))
    driver.find_element_by_link_text('Delete').click()
    sleep(5)


def test_infoc():
    '''
      测试信息页面
      不存在的链接文本
      '''
    test_login()
    driver.get('{0}/info/9705c'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('水').click()
    sleep(5)


def test_infod():
    '''
        测试信息页面
        修改分类
        '''
    test_login()
    driver.get('{0}/info/9705c'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Reclassify').click()
    sleep(5)


def test_infoe():
    '''
        测试信息页面
        Review
        '''
    test_login()
    driver.get('{0}/info/9705c'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Review').click()
    sleep(5)




def test_post_man():
    '''
      Review中 edit测试
      '''
    test_login()
    driver.get('{0}/post_man/view/9705c'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Edit').click()
    sleep(4)


def test_post_mana():
    '''
       Review中 View测试
       '''
    test_login()
    driver.get('{0}/post_man/view/9705c'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('View').click()
    sleep(4)


def test_postli():
    '''
    测试post页修改按钮
    :return:
    '''
    test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Edit').click()
    sleep(4)


def test_postlia():
    '''
    测试修改大分类
    :return:
    '''
    test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    sleep(2)
    driver.find_element_by_link_text('Reclassify').click()
    sleep(4)




def test_user_recent():
    test_login()
    driver.get('{0}/user_list/user_recent'.format(site_url))
    sleep(2)
    driver.find_element_by_xpath("//a[@href='#tab2']").click()
    sleep(4)




def test_comment():
    '''
       测试信息页面
       评论功能
       '''

    test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_id('cnt_reply').send_keys('我来评论，哈哈哈！评论的内容必须超过50字以上，否则评论失败。需要自己继续添加评论内容。')

    # driver.find_element_by_link_text("Submit").click()
    driver.find_element_by_xpath("//a[contains(@onclick, 'reply_it')]").click()


def test_vote():
    '''
    测试评论后其他用户点赞
    :return:
    '''
    Login().login(driver)
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_id('zan_text').click()
    sleep(5)
    driver.refresh()
    sleep(5)


def test_pldelete():
    '''
    测试评论本人删除评论
    :return:
    '''
    test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    # driver.find_element_by_link_text("Submit").click()
    driver.find_element_by_xpath("//a[contains(@onclick, 'reply_del')]").click()
    driver.refresh()
    sleep(2)


def test_pldeletea():
    '''
    测试权限高的用户删除其他用户的评论
    :return:
    '''
    Login().login(driver)
    driver.get('{0}/post/t0000'.format(site_url))
    # driver.find_element_by_link_text("Submit").click()
    driver.find_element_by_xpath("//a[contains(@onclick, 'reply_del')]").click()
    driver.refresh()
    sleep(2)



def test_nextpage():
    '''
    测试翻页功能
    :return:
    '''
    test_login()
    driver.get('{0}/post/t0000'.format(site_url))
    driver.find_element_by_link_text('Next Post').click()
    sleep(2)
    driver.find_element_by_link_text('Previous Post').click()
    sleep(2)
def test_nextpagea():
    '''
    测试列表翻页功能
    :return:
    '''
    test_login()
    driver.get('{0}/list/develop'.format(site_url))
    driver.find_element_by_link_text('Next page').click()
    sleep(2)
    driver.find_element_by_link_text('Previous page').click()
    sleep(2)
    driver.find_element_by_link_text('End').click()
    sleep(2)
    driver.find_element_by_xpath("//ul[@class='pagination']/li[1]/a").click()
    sleep(2)





if __name__ == '__main__':
      test_main_page()
    # test_mainsearch()
    # test_regist()
    #  test_regista()
    # test_registb()
    # test_login()
    # test_logina()
    #  test_loginb()
    # test_userinfo()
    # test_userinfoa()
    # test_userinfob()
    # test_userinfoc()
    # test_userinfod()
    # test_logout()
    # test_changepass()
    # test_changepassa()
    # test_changepassb()
    #  test_publish()
    # test_publisha()
    #  test_post()
    # test_post_collect()
    # test_postview()
    # test_post_reclass()
    #  test_post_edit()
    # test_post_view()

    # test_page()
    #  test_page_edit()
    # test_info()
    # test_info_edit()
    # test_changeinfo()
     # test_infoa()
    # test_infob()
    # test_infoc()
     #test_infod()
     # test_infoe()
    # test_post_man()
    #  test_post_mana()
    #  test_postli()
     # test_postlia()
    #  test_user_recent()
    # test_comment()
    # test_vote()
    # test_pldelete()
    # test_pldeletea()
    # test_nextpage()
    # test_nextpagea()

