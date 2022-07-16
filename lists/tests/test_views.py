from unittest import mock, skip

from django.utils.html import escape # parses str argument to HTML-escaped string
from django.test import TestCase
from django.urls import resolve

from lists.forms import DUPLICATE_ITEM_ERROR, ExistingListItemForm, ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List
from lists.views import home_page # deprecated for test client

@mock.patch('django.template.context_processors.get_token', mock.Mock(return_value='test_token'))
class HomePageTest(TestCase):

    def test_root(self):
        
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_root_uses_item_form(self):

        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class NewListTest(TestCase):

    def test_POST_request(self):

        self.client.post(
            "/lists/new", # no trailing slash -- action URLs that modify the database
            data={'text': 'A new list item'},
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):

        response = self.client.post("/lists/new", data={'text': 'A new list item'})
        new_list = List.objects.first()

        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_no_save_invalid_items(self):

        self.client.post('/lists/new', data={'text': ''})
        
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_home(self):

        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_displayed(self):

        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_invalid_input_passes_form_to_template(self):

        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

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

    def test_display_item_form(self):

        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")

        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

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

    def test_POST_saves_to_existing_list(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={'text': 'A new item for an existing list'},
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={'text': 'A new item for an existing list'},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def post_invalid_input(self):

        list_ = List.objects.create()
        return self.client.post(f"/lists/{list_.id}/", data={'text': ''})

    def test_nothing_saved_to_db_with_invalid_input(self):

        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_list_template_rendered_with_invalid_input(self):

        response = self.post_invalid_input()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_form_passed_to_template_with_invalid_input(self):

        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_errors_displayed_with_invalid_input(self):

        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_duplicate_items_errors_displayed_on_lists_page(self):

        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')

        response = self.client.post(f"/lists/{list1.id}/", data={'text': 'textey'})
        expected_error = DUPLICATE_ITEM_ERROR

        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)