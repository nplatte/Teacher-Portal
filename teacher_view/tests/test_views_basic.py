from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from teacher_view.models import Course


def _add_staff_user():
    test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
    staff_group = Group.objects.create(name='staff')
    staff_group.user_set.add(test_user)
    return test_user

def _make_class(user, title='test course'):
    term = f'2023 Fall Term'
    return Course.objects.create(title=title, course_instructor = user, term=term)


class TestHomePage(TestCase):

    def setUp(self):
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)

    def test_home_page_uses_right_template(self):
        request = self.client.get(reverse('staff_home_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/home.html')

    def test_home_page_passes_current_classes_for_navbar(self):
        new_course = _make_class(self.test_user)
        request = self.client.get(reverse('staff_home_page'))
        course_list = request.context['current_courses']
        self.assertIn(new_course, course_list)


class TestProfilePage(TestCase):

    def setUp(self):
        self.test_user = _add_staff_user()
        self.client.force_login(self.test_user)

    def test_profile_page_uses_right_template(self):
        request = self.client.get(reverse('staff_profile_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/profile.html')

    def test_profile_page_passes_current_courses_to_navbar(self):
        new_course = _make_class(self.test_user)
        request = self.client.get(reverse('staff_profile_page'))
        course_list = request.context['current_courses']
        self.assertIn(new_course, course_list)