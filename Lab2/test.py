import unittest
from test_equipment import Test, json_string, yaml_string, json_dict_string, yaml_dict_string, yaml_func_string, yaml_func, json_func, Exaple, toml_string, expamle_butoma
from serializer.form.MyJson import JsonFormat
from serializer.form.MyYaml import YamlFormat
from serializer.form.MyToml import TomlFormat
from factory.Factory import Factory


class TestSerializer(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.serializer = Factory()

    def test_factory(self):
        self.assertEqual(self.serializer.serialize(json_dict_string, YamlFormat, initial_type=JsonFormat), yaml_dict_string)
        self.assertEqual(self.serializer.serialize(yaml_func_string, YamlFormat, initial_type=YamlFormat), yaml_func_string)

    def test_json(self):
        #test function
        self.assertEqual(self.serializer.serialize(expamle_butoma, JsonFormat), json_func)
        self.assertEqual(self.serializer.deserialize(JsonFormat, obj_form=json_func)(), expamle_butoma())
        #test instance + class
        self.assertEqual(self.serializer.serialize(Test(), JsonFormat), json_string)
        self.assertEqual(self.serializer.deserialize(JsonFormat, obj_form=json_string).__dict__, Test().__dict__)
        self.assertEqual(self.serializer.serialize(Test(), JsonFormat, path_file="Json_test.json"), 1)
        self.assertEqual(self.serializer.deserialize(JsonFormat, path_file="Json_test.json").__dict__, Test().__dict__)

    def test_yaml(self):
        #test function
        self.assertEqual(self.serializer.serialize(expamle_butoma, YamlFormat), yaml_func)
        self.assertEqual(self.serializer.deserialize(YamlFormat, obj_form=yaml_func)(), expamle_butoma())
        #test instance + class
        self.assertEqual(self.serializer.serialize(Test(), YamlFormat), yaml_string)
        self.assertEqual(self.serializer.deserialize(YamlFormat, obj_form=yaml_string).__dict__, Test().__dict__)
        self.assertEqual(self.serializer.serialize(Test(), YamlFormat, path_file="Yaml_test.yaml"), 1)
        self.assertEqual(self.serializer.deserialize(YamlFormat, path_file="Yaml_test.yaml").__dict__, Test().__dict__)


    def test_toml(self):
        self.assertEqual(self.serializer.serialize(Exaple(), TomlFormat), toml_string)
        self.assertEqual(self.serializer.deserialize(TomlFormat, obj_form=toml_string).__dict__, Exaple().__dict__)
        self.assertEqual(self.serializer.serialize(Exaple(), TomlFormat, path_file="Toml_test.toml"), 1)
        self.assertEqual(self.serializer.deserialize(TomlFormat, path_file="Toml_test.toml").__dict__, Exaple().__dict__)
