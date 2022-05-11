from serializer.form.MyJson import JsonFormat
from serializer.form.MyYaml import YamlFormat
from serializer.form.MyToml import TomlFormat
from factory.AbstractFactory import AbstractFactory


class Factory(AbstractFactory):

    def create_serializer(self, type_ser):

        if type_ser == JsonFormat:

            return JsonFormat()

        elif type_ser == YamlFormat:

            return YamlFormat()

        elif type_ser == TomlFormat:

            return TomlFormat()
