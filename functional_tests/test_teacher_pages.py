from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User, Group
from selenium.webdriver.common.action_chains import ActionChains
from os import getcwd

from teacher_view.models import Course

from time import sleep

class TestTeacherCreateNewClass(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def teacher_login(self, username='new', password='password'):
        username_input = self.browser.find_element(By.ID, 'username')
        username_input.send_keys(username)
        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def test_teacher_can_create_new_class(self):
        # A teacher wants to log in to create a new class
        # they go to the Wartburg MCSP Website and see a log in page
        test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        staff_group = Group.objects.create(name='staff')
        staff_group.user_set.add(test_user)
        # They enter the log in information and are taken to the staff view of the website
        self.assertIn('Log In', self.browser.title)
        self.teacher_login()
        sleep(1)
        self.assertIn('Wartburg MCSP Teachers', self.browser.title)
        # they see a nav bar on the top of the page, this displays a Home button, Courses button, an Assignments button, and a Grades Button
        chain = ActionChains(self.browser)
        home_btn = self.browser.find_element(By.ID, 'nav-home')
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        #assignments_btn = self.browser.find_element(By.ID, 'nav-assignments')
        grades_btn = self.browser.find_element(By.ID, 'nav-grades')
        # they move to the courses dropdown and reveal other options
        chain.move_to_element(courses_btn).perform()
        add_course_btn = self.browser.find_element(By.ID, 'add-course')
        curr_courses_btn = self.browser.find_element(By.ID, 'curr-courses')
        # They move to see the current courses
        curr_courses_btn.click()
        # uh oh! They don't see any
        curr_courses = self.browser.find_elements(By.ID, 'course_title')
        self.assertEqual(len(curr_courses), 0)
        # they decide to fix this by adding a course
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        chain.move_to_element(courses_btn).perform()
        add_course_btn = self.browser.find_element(By.ID, 'add-course')
        add_course_btn.click()
        # This takes them to a new page where they see a form to make courses
        # At the top is an upload for files
        # They select the course file from their computer and press enter
        file_upload = self.browser.find_element(By.ID, 'source_file_input')
        file_upload.send_keys(f'{getcwd()}\\class_htmls\\CS_220.xls')
        save_course = self.browser.find_element(By.ID, 'file-submit')
        save_course.click()
        # the teacher is automatically taken to a new course page where theysee the new course title and stuff
        course = Course.objects.all()[0]
        self.assertEqual(self.browser.title, course.title)
        self.browser.find_element(By.ID, 'course-title')
