from unittest import mock

from django.shortcuts import render
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page # deprecated for test client
from lists.models import Item, List

@mock.patch('django.template.context_processors.get_token', mock.Mock(return_value='test_token'))
class HomePageTest(TestCase):

    def test_root(self):
        
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    #def test_html(self):

    #    response = self.client.get("/")

    #    html = response.content.decode('utf8')
        
    #    self.assertTrue(html.startswith('<!DOCTYPE html>'))
    #    self.assertIn('<title>To-Do lists</title>', html)
    #    self.assertTrue(html.strip().endswith('</html>'))
    #    self.assertTemplateUsed(response, 'home.html')

class NewListTest(TestCase):

    def test_POST_request(self):

        self.client.post(
            "/lists/new", # no trailing slash -- action URLs that modify the database
            data={'item_text': 'A new list item'},
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):

        response = self.client.post("/lists/new", data={'item_text': 'A new list item'})
        new_list = List.objects.first()

        self.assertRedirects(response, f"/lists/{new_list.id}/")

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
       
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'The second list item')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_list_template(self):

        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")

        self.assertTemplateUsed(response, 'list.html')

    def test_correct_list_to_template(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertEqual(response.context['list'], correct_list)

    def test_display_unique_list_items(self):

        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')


class NewItemTest(TestCase):

    def test_existing_list_POST_request(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_list_view_redirect(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
