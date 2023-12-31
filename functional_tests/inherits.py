from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import InMemoryUploadedFile

from teacher_view.models import Course
from os import getcwd, path, remove
from time import sleep


class BasicSeleniumTest(StaticLiveServerTestCase):

    ''' This is the parent class of each of the functional tests, it provides the 
    setUp and tearDown that is needed for each class. In addition it provides attributes
    such as self.browser and the base path needed for some of the functional tests.

    '''

    def setUp(self) -> None:
        # each Functional Test ran needs a teacher account that can be logged into
        self.test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        staff_group = Group.objects.create(name='staff')
        staff_group.user_set.add(self.test_user)
        # it also needs a browser window
        self.browser = webdriver.Firefox()
        # and a base path of where to pull the sample course files from
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
        return super().setUp()
    
    def tearDown(self) -> None:
        # looks in the file upload location and deletes the file if it exists
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()
    
    def _teacher_login(self, username='new', password='password'):
        # this is to be used on the login screen to log in the test user
        username_input = self.browser.find_element(By.ID, 'username')
        username_input.send_keys(username)
        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        sleep(3)
    
    def _create_course(self, instructor=None):
        # this creates a course using the InMemoryUploadedFile as the course file
        if not instructor:
            instructor = self.test_user
        file = open(f'{self.base_path}\\CS_260.xls')
        imf = InMemoryUploadedFile(
            file=file,
            field_name='source_file',
            name='CS_260.xls',
            content_type='application/vnd.ms-excel',
            size=14054,
            charset=None,
            content_type_extra={}
        )
        c = Course.objects.create(
            source_file=imf,
            code='CS 260 01',
            title='Introduction to Comp',
            term='2024 May Term',
            instructor=instructor
        )
        return c