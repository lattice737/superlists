from unittest import mock

from django.shortcuts import render
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item

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
        self.assertIn('1: Buy peacock feathers', response.content.decode())
        
        context = {'new_item_text': '1: Buy peacock feathers'}
        expected_html = render(request, 'home.html', context)

        self.assertEqual(response.content.decode(), expected_html.content.decode()) # FIXME content != expected_html

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'The second list item')

# Create your tests here.
