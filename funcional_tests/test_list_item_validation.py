# -*- coding: utf-8 -*-
from unittest import skip
from .base import FunctionalTest


class TestNewVisitor(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Pepe va a la home page y acidentalmente intenta introducir un item con texto
        # vacío.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # La home se refresca y aparece un error diciendo que la lista no puede contener item vacíos
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, "You can't have any empty list item ")

        # Pepe intenta otra ver introducit un item, esta vez con texto y funciona.
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1. Buy milk')

        # Como es perseverante intenta introducir otro objeto en blanco.
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # vuelve a recibir el mensaje de error de la página.
        self.check_for_row_in_list_table('1. Buy milk')
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, "You can't have any empty list item ")

        # lo corrige e introduce texto
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1. Buy milk')
        self.check_for_row_in_list_table('2. Make tea')
