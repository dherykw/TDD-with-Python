# -*- coding: utf-8 -*-
from unittest import skip
from .base import FunctionalTest


class TestNewVisitor(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector(".has-error")

    def test_cannot_add_empty_list_items(self):
        # Pepe va a la home page y acidentalmente intenta introducir un item con texto
        # vacío.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # La home se refresca y aparece un error diciendo que la lista no puede contener item vacíos
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have any empty list item")

        # Pepe intenta otra ver introducit un item, esta vez con texto y funciona.
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1. Buy milk')

        # Como es perseverante intenta introducir otro objeto en blanco.
        self.get_item_input_box().send_keys('\n')

        # vuelve a recibir el mensaje de error de la página.
        self.check_for_row_in_list_table('1. Buy milk')
        error = self.browser.find_element_by_css_selector(".has-error")
        self.assertEqual(error.text, "You can't have any empty list item")

        # lo corrige e introduce texto
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1. Buy milk')
        self.check_for_row_in_list_table('2. Make tea')

    def test_cannot_add_duplicate_items(self):
        # Pepe va a la página de home y empieza una nueva lista
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1. Buy milk')

        # El accidentalmente intenta introducir un elemento duplicado
        self.get_item_input_box().send_keys('Buy milk\n')

        # El ve un util mensaje de error
        self.check_for_row_in_list_table('1. Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        # Pepe comienza una nueva list the una manera que causa un error de validación
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # Empieza a escribir y el error desaparece
        self.get_item_input_box().send_keys('a')
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())

