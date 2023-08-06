from django.template import Context, Template
from django.test import TestCase
from django.test.utils import override_settings


class TemplatesTagsTestCase(TestCase):
    front_url = 'http://myfront/'

    @override_settings(FRONT_URL=front_url)
    def test_front_url(self):
        context = Context()
        template_to_render = Template(
            '{% load settings_tags %}'
            '{% front_url %}'
        )

        rendered = template_to_render.render(context)

        self.assertEqual(rendered, self.front_url)
