from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

class TestTeacherCreateNewClass(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def teacher_login(self, username='new', password='password'):
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def test_teacher_can_create_new_class(self):
        # A teacher wants to log in to create a new class
        # they go to the Wartburg MCSP Website and see a log in page
        User.objects.create_user('new', 'new@gmail.com', 'password')
        # They enter the log in information and are taken to the staff view of the website
        self.assertIn('Wartburg MCSP Teachers', self.browser.title)
        # they see a nav bar on the top of the page, this displays a Home button, Courses button, an Assignments button, and a Grades Button
        home_btn = self.browser.find_element(By.ID, 'nav-home')
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        assignments_btn = self.browser.find_element(By.ID, 'nav-assignments')
        grades_btn = self.browser.find_element(By.ID, 'nav-grades')
        # they click the courses Button
        courses_btn.click()
        # This takes them to a new page where they see all the courses with a break down of students and recent activity
        courses = self.browser.find_elements(By.CLASS_NAME, 'course-title')
        self.assertEqual(len(courses), 0)
        self.assertEqual('Courses', self.browser.title)
        # At the top is a button for new courses
        new_course_btn = self.browser.find_element(By.ID, 'new-course-btn')
        # They click this button and a window pops up on screen asking for a file upload
        new_course_btn.click()
        # They select the course file from their computer and press enter
        file_upload = self.browser.find_element_by_name('Class_File')
        file_upload.send_keys('C:\\Users\\nplat\\OneDrive\\Desktop\\Senior Project\\Class\\test_class_htmls\\cs_220.xls')
        save_course = self.browser.find_element_by_name('_save')
        save_course.click()
        # the back end processes the file and generates a new course page from the file
        # they see the students in the course and navigate to courses and see the course listed after refreshing.
        courses = self.browser.find_elements(By.CLASS_NAME, 'course-title')
        self.assertEqual(len(courses), 1)