import argparse
from factory.Factory import Factory
from test_equipment import print_hi, Exaple, Test
from serializer.form.MyYaml import YamlFormat
from serializer.form.MyToml import TomlFormat
from serializer.form.MyJson import JsonFormat

objects = {"function": print_hi, "class": Exaple, "instance": Test()}
types = {"json": JsonFormat, "yaml": YamlFormat, "toml": TomlFormat}

serializer = Factory()
argparse = argparse.ArgumentParser()
argparse.add_argument('-act','--action', choices=["ser", "des"], required=True, default=None, help="Nothin")
argparse.add_argument('-ob','--object', choices=["function", "class", "instance"], required=False,default=None, help="Sorry")
argparse.add_argument('-st_fr', "--str_form", choices=["function", "class", "instance"], required=False,default=None, help="useless")
argparse.add_argument('-ty','--type_ser', choices=["json", "yaml", "toml"], required=True,default=None, help="More sorry")
argparse.add_argument('-init','--initial_type', choices=["json", "yaml", "toml"], default=None, help="My error")
argparse.add_argument('-path','--path_file', default=None, help="I wish about it")

print(argparse.parse_args())
res = argparse.parse_args()

if res.object in objects:
    obj = objects[res.object]

else:
    obj = None

if res.type_ser in types:
    type_ser = types[res.type_ser]

else:
    type_ser = None

initial_type = res.initial_type
path_file = res.path_file
str_form = res.str_form

ans = res.action

if ans == "ser":
    print(serializer.serialize(obj, type_ser, initial_type=initial_type, path_file=path_file))

elif ans == "des":
    result = serializer.deserialize(type_ser, obj_form=obj, path_file=path_file)
    print(result)