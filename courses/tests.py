
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Course
from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase

class CourseModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_course = Course.objects.create(
            author = test_user,
            title = 'Title of Course',
            body = 'Words about the course',
        )
        test_course.save()

    def test_blog_content(self):
        course = Course.objects.get(id=1)

        self.assertEqual(str(course.author), 'tester')
        self.assertEqual(course.title, 'Title of Course')
        self.assertEqual(course.body, 'Words about the course')

class APITest(APITestCase):

    def test_list_FORBIDDIEN(self):
        response = self.client.get(reverse('Course_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_course = Course.objects.create(
            author = test_user,
            title = 'Title of Course',
            body = 'Words about the course',
        )
        test_course.save()

        response = self.client.get(reverse('Course_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_course.title,
            'body': test_course.body,
            'author': test_course.id,
        })

    def  test_loggedin_user(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()
        c = Client()
        logged_in = c.login(username='tester', password='pass')
        self.assertTrue(logged_in)

    def test_create(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

     
        url = reverse('Course_list')
        data = {
            "title":"Testing is Fun!!!",
            "body":"when the right tools are available",
            "author":test_user.id,
        }
        self.client.login(username='tester',password='pass')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_course = Course.objects.create(
            author = test_user,
            title = 'Title of Course',
            body = 'Words about the course'
        )

        test_course.save()

        url = reverse('Course_detail',args=[test_course.id])
        data = {
            "title":"Testing is Still Fun!!!",
            "author":test_course.author.id,
            "body":test_course.body,
        }
        self.client.login(username='tester',password='pass')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, url)
        self.assertEqual(Course.objects.count(), test_course.id)
        self.assertEqual(Course.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a post."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_course = Course.objects.create(
            author = test_user,
            title = 'Title of Course',
            body = 'Words about the course'
        )

        test_course.save()

        course = Course.objects.get()

        url = reverse('Course_detail', kwargs={'pk': course.id})

        self.client.login(username='tester',password='pass')
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)