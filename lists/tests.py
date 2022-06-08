from unittest import mock

from django.shortcuts import render
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page # deprecated for test client
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
        request.POST['item_text'] = "A new list item"
        
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        
        new_item = Item.objects.first()

        self.assertEqual(new_item.text, "A new list item")
       
    def test_redirect_after_POST(self):

        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_save_condition(self):

        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


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


class LiveViewTest(TestCase):

    def test_list_template(self):

        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_list(self):

        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1') # method can handle response binary; content decoding deprecated
        self.assertContains(response, 'itemey 2')
