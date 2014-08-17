from .dragon_test_case import DragonTestCase
from .models import TextModel, ParentModel, ChildModel
from .. import model_tools


class TestModelTools(DragonTestCase):
    def test_get_property(self):
        text_model = TextModel.objects.create(text='test')
        val = model_tools.get_property(text_model, 'text')
        self.assertEqual(val, text_model.text)

    def test_get_related_property(self):
        parent = ParentModel.objects.create(name='a parent')
        child = ChildModel.objects.create(number=12, parent=parent)
        val = model_tools.get_property(child, 'parent__name')
        self.assertEqual(val, parent.name)

    def test_get_invalid_related_property(self):
        parent = ParentModel.objects.create(name='a parent')
        child = ChildModel.objects.create(number=12, parent=parent)
        self.assertIsNone(model_tools.get_property(parent, 'parent__invalid_property__p'))

    def test_string_to_list(self):
        data_string = '[a,b,c]'
        expected = ['a', 'b', 'c']
        actual = model_tools.string_to_list(data_string)
        self.assertListEqual(expected, actual)

    def test_get_model(self):
        parent_model = 'tests.ParentModel'
        model = model_tools.get_model(parent_model)
        self.assertEqual(model, ParentModel)
