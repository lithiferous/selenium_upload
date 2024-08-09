import config
import os
import time
from files import GetAttribution
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from tools import *

class LoadShare():
    #todo create connection objects
    def __init__(self, user, password, segments, id_list, campaign, period):
        config.browser = webdriver.Chrome(executable_path=os.getcwd()
                                          +"/core/share/chromedriver.exe")
        self.user = user
        self.password = password
        self.segments = segments
        self.files = None
        self.current_date = segments.current_date
        self.folder_name = segments.outname
        self.folder_path = segments.filepath
        self.rtb = segments.rtb
        self.id_list = id_list if id_list is not None else []
        self.campaign = campaign if campaign is not None else None
        self.period = period if period is not None else None
        
    def create_zip(self):
        self.files = GetAttribution(self.segments).write_files().zippath + '.zip'
     
    def auth(self): #login
        visit("")
        add(css('userlogin'), self.user)
        add(css('userpassword'), self.password)
        goto(css('login_button'))

    def fill_data(self): #fill share information
        tmp_pwd = "0000"
        goto(css('shared_documents_tab'))
        goto(css('create_new_folder'))
        goto(css('public_link_checkbox'))
        edit_form(css('folder_name'), self.folder_name + '_' + self.rtb)
        edit_form(css('folder_password'), tmp_pwd)
        edit_form(css('folder_password_again'), tmp_pwd)
        goto(css('post_form'))
        write_share_info(self.folder_path, css('public_link'), self.rtb, self.id_list, self.campaign, self.period)
        
    def upload_files(self): #load zip archive
        goto(css('upload_files_button'))
        goto(css('upload_files_again'))
        send_files(self.files)
        upload_finish(css('upload_progress_bar'))
        config.browser.quit()

    def run_all(self):
        st = time.time()

        def get_time():
            t = time.time() - st
            return ' {:.2f} sec  {:.1f} min'.format(t, t / 60)
        self.create_zip()
        print(f'Zipping done in: {get_time()}')
        self.auth()
        print(f'Login done in: {get_time()}')
        self.fill_data()
        print(f'Share form done in: {get_time()}')
        self.upload_files()
        print(f'Upload done in: {get_time()}')
