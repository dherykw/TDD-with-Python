import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestNewVisitor(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_start_a_new_todo_list(self):
        # El usuatio ha odio de nuestra genial aplicación y entra
        self.browser.get('http://localhost:8000')

        # El usuario nota que el título es nuestra to do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Es invitado a insertar un to do en la lista
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Escribe "Comprar papel higienico en la lista"
        inputbox.send_keys('Comprar papel higienico')

        # Cuando pulsa enter la página se actualiza y pone:
        # 1. Comprar papel higienico en la lista
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1. Comprar papel higienico', [row.text for row in rows])

        # Sigue apareciendo un texbox que invita a añadir otra tarea
        # El usuario introduce otra tarea
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Comprar champú')
        inputbox.send_keys(Keys.ENTER)

        # La página se vuelve a actualizar y ahora muestra las dos tareas
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('2. Comprar champú', [row.text for row in rows])




        # El usuario se pregunta si el sitio recordará su lista, entonces ve
        # que el sitio genera una url unica para ella


        # Visita esa url y comprueba que su to-do list está aun ahí

        # Satisfecho abandona la página y se va a dormir

        self.fail('Fin de test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
