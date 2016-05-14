# -*- coding: utf-8 -*-
import sys
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_start_a_new_todo_list_and_retrieve_it_later(self):
        # El usuario ha odio de nuestra genial aplicación y entra
        self.browser.get(self.server_url)

        # El usuario nota que el título es nuestra to do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Es invitado a insertar un to do en la lista
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Escribe "Comprar papel higienico en la lista"
        inputbox.send_keys('Comprar papel higienico')

        # Cuando pulsa enter, el usuario es llevado a una nueva url
        # y ahora la página se pone:
        # 1. Comprar papel higienico en la lista
        inputbox.send_keys(Keys.ENTER)
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1. Comprar papel higienico')

        # Sigue apareciendo un texbox que invita a añadir otra tarea
        # El usuario introduce otra tarea
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Comprar champú')
        inputbox.send_keys(Keys.ENTER)

        # La página se vuelve a actualizar y ahora muestra las dos tareas
        self.check_for_row_in_list_table('1. Comprar papel higienico')
        self.check_for_row_in_list_table('2. Comprar champú')

        # Ahora un nuevo usuario, Pepe, visita la página

        ## Usamos una nueva sesión de usuario para asegurarnos de que no hay
        ## información del usuario anterior.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Pepe visita el home, no hay rastro de la lista del usuario anterior.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comprar papel higienico', page_text)
        self.assertNotIn('Comprar champú', page_text)

        # Pepe empieza una nueva lista introduciendo un nuevo objeto
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Comprar Leche')
        inputbox.send_keys(Keys.ENTER)

        # Pepe obtine su url unica
        pepe_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')
        self.assertNotEqual(pepe_list_url, user_list_url)

        # De nuevo no hay rastro de la lista del primer Usuario
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comprar papel higienico', page_text)
        self.assertIn('Comprar Leche', page_text)