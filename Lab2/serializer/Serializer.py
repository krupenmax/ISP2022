from abc import ABC, abstractmethod
import inspect
import re
from types import FunctionType, CodeType
import types


class Serializer(ABC):

    def dumps(self, obj):

        if inspect.isclass(obj):  # создаем словарь из класса, чтобы сериализовать его как объект
            json_class_str = self.dumps(self.make_dict_class(obj))

            return json_class_str

        elif inspect.isfunction(obj):  # make dictionary from function, that serialize it like object
            json_func_str = self.dumps(self.make_dict_function(obj))

            return json_func_str

        elif isinstance(obj, dict):
            json_dict = self.serialize_form(obj)

            return json_dict

        else:
            dict_obj = self.make_dict_obj(obj)
            json_obj = self.serialize_form(dict_obj)
            return json_obj

    def make_dict_obj(self, obj):
        type_object = type(obj)
        dict_type = self.make_dict_class(type_object)
        dict_object = {'*type_class*': dict_type, 'dict': obj.__dict__}

        return dict_object

    @abstractmethod
    def serialize_form(self, fields):
        pass

    def dump(self, obj, my_file):
        str_json = self.dumps(obj)

        try:
            my_file.write(str_json)
        except IOError:

            return 0

        return 1

    def load(self, my_file):

        try:
            str_json = my_file.read()
            dict_result = self.loads(str_json)
        except IOError:

            return None

        return dict_result

    def loads(self, my_str):
        result = {}
        flag_have_object = False  # Flag of checking result on instance

        if my_str != "":
            result = self.deserialize_from(my_str)

            for key, value in result.items():

                if key == "*type_class*":  # Dictionary of instance have first item a name like "*type_class*" and second item "dict"
                    flag_have_object = True
                    result[key] = self.make_class_dict(
                        value)  # as after *type_class* must be dict, we transform only *type_class*

                elif key == "__init__":
                    result = self.make_class_dict(result)  # Checking dictionary on type of class

                elif key == "__code__":
                    result = self.make_func_dict(result)  # Checking dictionary on function

            if flag_have_object:
                InstanceType = result["*type_class*"]
                instance = InstanceType()  # Create a real instance from type, that we retrieve from dictionary
                instance.__dict__ = result["dict"]  # Transmit a serialized data

                return instance

        return result

    @abstractmethod
    def deserialize_from(self, my_str_json):
        pass

    def make_dict_function(self, fun):
        attributes = dict(inspect.getmembers(fun))
        attributes_code = dict(inspect.getmembers(attributes['__code__']))
        result_code = {}
        result_globals = {}

        for key, value in attributes_code.items():

            if key[0] != "_" and key != "replace" and key != "co_lines":
                if isinstance(value, str) and len(value) == 0:
                    result_code[key] = None

                else:
                    result_code[key] = value

        for element in attributes_code["co_names"]:

            if element in attributes["__globals__"]:
                value = attributes["__globals__"][element]

            else:
                continue

            if element == attributes["__name__"]:
                result_globals[element] = element

            elif isinstance(value, (int, float, bool, bytes, str)):
                result_globals[element] = value

            elif isinstance(value, (list, set, frozenset, tuple, dict)):
                result_globals[element] = value

            elif inspect.isclass(value):
                result_globals[element] = self.make_dict_class(value)

            elif inspect.ismodule(value):
                result_globals[value.__name__] = "__module__"

            elif inspect.isfunction(value):
                result_globals[element] = self.make_dict_function(value)

            else:
                result_globals[element] = self.make_dict_obj(value)

        array_closure = []

        if not (isinstance(attributes['__closure__'], type(None))):

            for item in attributes['__closure__']:  # перебираю все переменные участвующие в замыкании(используется для декоратора)

                if inspect.isfunction(item.cell_contents):
                    array_closure.append(self.make_dict_function(item.cell_contents))

                elif inspect.isclass(item.cell_contents):
                    array_closure.append(self.make_dict_class(item.cell_contents))

                elif isinstance(item.cell_contents, (str, int, float, bytes, list, tuple, set, frozenset, dict, type(None))):
                    array_closure.append(item.cell_contents)

                else:
                    array_closure.append(self.make_dict_obj(item.cell_contents))

        array_closure = tuple(array_closure)  # создаю картеж элементво замыкаиния  из обработанных в словари

        return {"__code__": result_code, "__globals__": result_globals, "__name__": attributes['__name__'],
                "__defaults__": attributes['__defaults__'], "__closure__": array_closure}

    def make_dict_class(self, obj):
        class_dict = {}
        attribute_class = inspect.getmembers(obj)

        for key, value in attribute_class:

            if key[0] != "_":

                if inspect.ismethod(value):
                    class_dict[key] = self.make_dict_function(value.__func__)

                elif isinstance(value, (int, float, bool, str, bytes, list, set, frozenset, tuple, dict)):
                    class_dict[key] = value

                elif inspect.isfunction(value):
                    class_dict[key] = self.make_dict_function(value)

                elif inspect.isclass(value):
                    class_dict[key] = self.make_dict_class(value)

                else:
                    class_dict[key] = self.make_dict_obj(value)

            elif key == "__init__":
                class_dict[key] = self.make_dict_function(value)

        return class_dict

    def make_func_dict(self, my_dict):
        dict_argument = {"co_argcount": None, "co_posonlyargcount": None, "co_kwonlyargcount": None, "co_nlocals": None,
                         "co_stacksize": None, "co_flags": None, "co_code": None, "co_consts": None, "co_names": None,
                         "co_varnames": None, "co_filename": None, "co_name": None, "co_firstlineno": None,
                         "co_lnotab": None, "co_freevars": (), "co_cellvars": ()}

        for key, value in my_dict['__code__'].items():

            if isinstance(value, list):
                value = self.conver_tuple(value)

            dict_argument[key] = value

        recursion_have = False

        for key, value in my_dict['__globals__'].items():
            flag_have_object = False

            if value == my_dict['__name__']:
                recursion_have = True
                continue

            elif value == "__module__":
                my_dict["__globals__"][key] = __import__(key)

            elif isinstance(value, dict):

                for master_key, master_value in value.items():

                    if master_key == "*type_class*":  # Dictionary of instance have first item a name like "*type_class*" anf second item "dict"
                        flag_have_object = True
                        my_dict["__globals__"][key][master_key] = self.make_class_dict(master_value)

                    if master_key == "__init__":
                        my_dict['__globals__'][key] = self.make_class_dict(value)

                    if master_key == "__code__":
                        my_dict["__globals__"][key] = self.make_func_dict(value)

                if flag_have_object:
                    InstanceType = my_dict["__globals__"][key]["*type_class*"]
                    instance = InstanceType()  # Creat a real instance from type, that we retrive from dictionary
                    instance.__dict__ = my_dict["__globals__"][key]["dict"]  # Transmit a serialized data
                    my_dict["__globals__"][key] = instance

        list_argument = [value for key, value in dict_argument.items()]
        code = CodeType(*list_argument)
        my_dict['__globals__']['__builtins__'] = __builtins__

        cells_closure = []

        if not (isinstance(my_dict['__closure__'], type(None))):

            for item in my_dict['__closure__']:  # перебираю все переменные участвующие в замыкании(используется для декоратора)
                flag_have_object = False

                if isinstance(item, dict):
                    cell_item = item

                    for master_key, value in item.items():  # find and deserialize all function and class, if thew have in clousure

                        if master_key == "*type_class*":  # Dictionary of instance have first item a name like "*type_class*" anf second item "dict"
                            flag_have_object = True
                            item[master_key] = self.make_class_dict(value)

                        elif master_key == "__init__":
                            cell_item = self.make_class_dict(item)

                        elif master_key == "__code__":
                            cell_item = self.make_func_dict(item)

                    if flag_have_object:
                        InstanceType = item["*type_class*"]
                        instance = InstanceType()  # Creat a real instance from type, that we retrive from dictionary
                        instance.__dict__ = item["dict"]  # Transmit a serialized data
                        cells_closure.append(instance)

                    else:
                        cells_closure.append(cell_item)

                else:
                    cells_closure.append(item)

        cells_closure = [types.CellType(element) for element in cells_closure]  # make a Cell object, that we transmit to FunctionType, because of clouser retrieve only Cell object
        cells_closure = tuple(cells_closure)
        func = FunctionType(code, my_dict['__globals__'], my_dict['__name__'], self.conver_tuple(my_dict['__defaults__']), cells_closure)

        if recursion_have:
            func.__getattribute__('__globals__')[my_dict['__name__']] = func

        return func

    def convert_tuple(self, obj):

        if not (isinstance(obj, type(None))):
            for i in range(len(obj)):
                if isinstance(obj[i], list):
                    obj[i] = self.conver_tuple(obj[i])

            return tuple(obj)

        else:

            return ()

    def make_class_dict(self, my_dict):

        for key, value in my_dict.items():
            flag_have_object = False

            if isinstance(value, dict):

                for master_key, master_value in value.items():

                    if master_key == "*type_class*":  # Dictionary of instance have first item a name like "*type_class*" anf second item "dict"
                        flag_have_object = True
                        my_dict[key][master_key] = self.make_class_dict(master_value)

                    if master_key == "__init__":
                        my_dict[key] = self.make_class_dict(value)

                    if master_key == "__code__":
                        my_dict[key] = self.make_func_dict(value)

                if flag_have_object:
                    InstanceType = my_dict[key]["*type_class*"]
                    instance = InstanceType()  # Creat a real instance from type, that we retrive from dictionary
                    instance.__dict__ = my_dict[key]["dict"]  # Transmit a serialized data
                    my_dict[key] = instance

        instance = type("Test", (), my_dict)

        return instance
