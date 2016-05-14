# -*- coding: utf-8 -*-
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # El usuario entra al home
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Obseva que el inputbox está agradablente centrado
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=5
        )
