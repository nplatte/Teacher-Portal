from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from teacher_view.models import Course, Assignment
from teacher_view.forms import CourseModelFileForm, EditCourseForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.timezone import datetime
from os import getcwd, remove, path
import zoneinfo


def _add_staff_user():
    test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
    staff_group = Group.objects.create(name='staff')
    staff_group.user_set.add(test_user)
    return test_user

def _make_class(user, title='test course'):
    term = f'2023 Fall Term'
    return Course.objects.create(title=title, course_instructor = user, term=term)


class TestViewCoursePage(TestCase):

    def setUp(self) -> None:
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)
        self.c = _make_class(self.test_user)
        self.response = self.client.get(reverse('staff_course_page', kwargs={'course_id': self.c.pk}))
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'teacher_view/course/view.html')

    def test_passes_navbar_information(self):
        cc = self.response.context['current_courses']
        self.assertEqual(len(cc), 1)
        self.assertIn(self.c, cc)

    def passes_correct_context(self):
        c = self.response.context['course']
        self.assertEqual(c, self.c)
        assignments = self.response.context['assignments']
        self.assertEqual(len(assignments), 0)

    def test_does_not_pass_other_course_assignments(self):
        c2 = _make_class(self.test_user, 'class 2')
        a1 = Assignment.objects.create(
            title='Make Google',
            description='make Google please',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            course=self.c
        )
        a2 = Assignment.objects.create(
            title='Make Google 2',
            description='make Google please 2',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='America/Panama')),
            course=c2
        )
        response = self.client.get(reverse('staff_course_page', kwargs={'course_id': self.c.pk}))
        a_list = response.context['assignments']
        self.assertIn(a1, a_list)
        self.assertNotIn(a2, a_list)


class TestAddCoursePage(TestCase):

    def setUp(self):
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)

    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

    def test_add_course_login_required(self):
        self.client.logout()
        request = self.client.get(reverse('staff_add_course_page'), follow=True)
        self.assertTemplateUsed(request, 'login/login.html')

    def test_page_uses_right_template(self):
        request = self.client.get(reverse('staff_add_course_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/course/create.html')

    def test_add_courses_passes_current_courses_to_navbar(self):
        new_course = _make_class(self.test_user)
        request = self.client.get(reverse('staff_add_course_page'))
        courses = request.context['current_courses']
        self.assertIn(new_course, courses)

    def test_file_upload_form_is_passed_to_page(self):
        request = self.client.get(reverse('staff_add_course_page'))
        form = request.context['file_form']
        self.assertIsInstance(form, CourseModelFileForm)

    def test_file_upload_form_redirects_to_new_course_page(self):
        pth = f'{getcwd()}\\teacher_view\\test_class_htmls\\CS_220_May.xls'
        ofile = open(pth)
        data = {
            'source_file': ofile
        }
        request = self.client.post(reverse('staff_add_course_page'), follow=True, data=data)
        self.assertRedirects(request, '/teacher/course/1/')

    def test_file_upload_creates_new_course(self):
        courses = len(Course.objects.all())
        self.assertEqual(0, courses)
        pth = f'{getcwd()}\\teacher_view\\test_class_htmls\\CS_220_May.xls'
        ofile = open(pth)
        data = {
            'source_file': ofile
        }
        request = self.client.post(reverse('staff_add_course_page'), follow=True, data=data)
        courses = len(Course.objects.all())
        self.assertEqual(1, courses)


class TestEditCoursePage(TestCase):

    def setUp(self):
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
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
        self.c = Course.objects.create(
            source_file=imf,
            code='CS 260 01',
            title='Introduction to Comp',
            term='2024 May Term',
            course_instructor=self.test_user
        )
    
    def tearDown(self) -> None:
        upload_dir = f'{getcwd()}\\class_htmls'
        if path.exists(f'{upload_dir}\\CS_260.xls'):
            remove(f'{upload_dir}\\CS_260.xls')
        return super().tearDown()  

    def test_returns_right_html_page(self):
        request = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        self.assertTemplateUsed(request, 'teacher_view/course/edit.html')

    def test_pass_current_courses_to_navbar(self):
        request = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        curr_courses = request.context['current_courses']
        edited_course = request.context['course']
        self.assertEqual(len(curr_courses), 1)
        self.assertEqual(self.c, edited_course)
        self.assertIsInstance(edited_course, Course)

    def test_course_uses_right_form_for_editing(self):
        request = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        edit_form = request.context['edit_form']
        self.assertIsInstance(edit_form, EditCourseForm)

    def test_form_has_existing_course_info(self):
        request = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        edit_form = request.context['edit_form'].as_p()
        self.assertIn('Introduction to Comp', edit_form)
        self.assertIn('CS 260 01', edit_form)

    def test_successful_POST_redirects_to_course_page(self):
        data = {
            'title': 'Weird',
            'code': '1234',
            'term': 'May 2024'
        }
        request = self.client.post(reverse('staff_edit_course_page', kwargs={'course_id': 1}), data=data)
        self.assertRedirects(request, reverse('staff_course_page', kwargs={'course_id': 1}))

    def test_unseccessful_POST_does_not_redirect(self):
        data = {
            'title': 'Weird',
            'term': 'May 2024'
        }
        request = self.client.post(reverse('staff_edit_course_page', kwargs={'course_id': 1}), data=data)
        self.assertRedirects(request, reverse('staff_course_page', kwargs={'course_id': 1}))

    def test_successful_form_updates_course_info(self):
        data = {
            'title': 'Introduction Class',
            'term': 'May 2024',
            'code': '1234'
        }
        request = self.client.post(reverse('staff_edit_course_page', kwargs={'course_id': self.c.pk}), data=data)
        c = Course.objects.get(pk=self.c.pk)
        self.assertNotEqual('Introduction to Comp', c.title)
        self.assertEqual(data['title'], c.title)


class TestCoursesViewPage(TestCase):

    def setUp(self) -> None:
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
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
        self.c = Course.objects.create(
            source_file=imf,
            code='CS 260 01',
            title='Introduction to Comp',
            term='2024 May Term',
            course_instructor=self.test_user
        )
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_uses_right_template(self):
        response = self.client.get(reverse('staff_courses_page'))
        self.assertTemplateUsed(response, 'teacher_view/course/courses.html')

    def test_passes_navbar_courses(self):
        request = self.client.get(reverse('staff_courses_page'))
        curr_courses = request.context['current_courses']
        self.assertEqual(len(curr_courses), 1)

    def test_passes_logged_in_users_courses(self):
        non_user_course = Course.objects.create(
            code='CS 260 02',
            title='Intro to Comp',
            term='2023 May Term'
        )
        response = self.client.get(reverse('staff_courses_page'))
        all_courses = response.context['all_courses']
        self.assertEqual(1, len(all_courses))
        self.assertNotIn(non_user_course, all_courses)
        self.assertIn(self.c, all_courses)
        