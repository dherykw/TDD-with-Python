import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
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

        # Es invitado a insertar un to do en la lista


        # Escribe "Comprar papel higienico en la lista"


        # Cuando pulsa enter la página se actualiza y pone:
        # 1. Comprar papel higienico en la lista

        # Sigue apareciendo un texbox que invita a añadir otra tarea
        # El usuario introduce otra tarea

        # La página se vuelve a actualizar y ahora muestra las dos tareas

        # El usuario se pregunta si el sitio recordará su lista, entonces ve
        # que el sitio genera una url unica para ella


        # Visita esa url y comprueba que su to-do list está aun ahí

        # Satidfecho abandona la página y se va a dormir

if __name__ == '__name__':
    unittest.main(warnings='ignore')
