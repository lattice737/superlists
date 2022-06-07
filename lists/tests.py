from unittest import mock

from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page

@mock.patch('django.template.context_processors.get_token', mock.Mock(return_value='test_token'))
class HomePageTest(TestCase):
    '''Lists app unit testing class'''

    def test_root(self):
        
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_html(self):

        request = HttpRequest()
        response = home_page(request)
        expected_html = render(request, 'home.html')

        self.assertEqual(response.content.decode(), expected_html.content.decode())

    def test_POST_request(self):
        
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = "1: Buy peacock feathers"
        
        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())
        
        context = {'new_item_text': '1: Buy peacock feathers'}
        expected_html = render(request, 'home.html', context)

        self.assertEqual(response.content.decode(), expected_html.content.decode()) # FIXME content != expected_html

# Create your tests here.
