# -*- coding: utf-8 -*-
from unittest import skip
from .base import FunctionalTest


class TestNewVisitor(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Pepe va a la home page y acidentalmente intenta introducir un item con texto
        # vacío.

        # La home se regresca y aparece un error diciendo que la lista no puede contener item vacíos

        # Pepe intenta otra ver introducit un item, esta vez con texto y funciona.

        # Como es perseverante intenta introducir otro objeto en blanco.

        # vuelve a recibir el mensaje de error de la página.

        # lo corrige e introduce tenxo

        self.fail("Escribeme!!")
