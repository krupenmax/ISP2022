from factory.Factory import Factory
from test_equipment import print_hi, Exaple, Test
from serializer.form.MyYaml import YamlFormat
from serializer.form.MyToml import TomlFormat
from serializer.form.MyJson import JsonFormat

import math
c = 42

def f(a, b):
    return math.sin(a * b * c)


fer = Factory()

res = fer.serialize(Test(), JsonFormat)

init = fer.deserialize(JsonFormat, res)

print(init.beta.name)