from time import sleep
from cfg import SITE_CFG

site_url = SITE_CFG['site_url']


class Login():
    #另外帐号登陆
    def login(self,driver):
        driver.get('{0}/user/login'.format(site_url))
        driver.find_element_by_id('user_name').clear()
        driver.find_element_by_id('user_name').send_keys('gislite')
        driver.find_element_by_id('user_pass').clear()
        driver.find_element_by_id('user_pass').send_keys('131322')
        driver.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
        sleep(5)




