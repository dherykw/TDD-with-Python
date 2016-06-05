from unittest import skip

from django.test import TestCase
from django.utils.html import escape

from list.forms import ItemForm, EMPTY_ITEM_ERROR
from list.models import Item, List


# Create your tests here.
class HomePageTest(TestCase):
    maxDiff = None

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'list/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list/list.html')

    def test_displays_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)

        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other itemey 1')
        self.assertNotContains(response, 'other itemey 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text': 'A new item for an exiting list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an exiting list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text': 'A new item fot an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/%d/' % (list_.id,),
                                data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(),0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list/list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item = Item.objects.create(list=list1, text='textkey')
        response = self.client.post(
            '/lists/%d/' % list1.id,
            data={'text': item.text}
        )
        expected_error = escape("You've already got this in your list")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list/list.html')
        self.assertEqual(Item.objects.count(), 1)

class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)