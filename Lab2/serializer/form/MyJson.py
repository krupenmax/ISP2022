from serializer.Serializer import Serializer
import re


class JsonFormat(Serializer):

    def __init__(self):
        pass

    def serialize_form(self, fields):
        json_str = "{"

        for key in fields:
            value = fields[key]
            data_str = f", \"{str(key)}\": "

            if isinstance(value, bool):

                if value:
                    data_str += "true"
                else:
                    data_str += "false"

            elif isinstance(value, (int, float)):
                data_str += str(value)

            elif isinstance(value, bytes):
                integer_value = "bytes_" + str(len(value)) + "_" + str(int.from_bytes(value, "big"))
                data_str += f"\"{integer_value}\""

            elif isinstance(value, str):  # Делаем отдельную проверку на тип у строки, т.к. строке в json необходимы ""
                data_str += f"\"{value}\""

            elif isinstance(value, (list, set, tuple, frozenset)):
                current_str = self.make_str_list(value)
                data_str += current_str

            elif isinstance(value, type(None)):
                data_str += "null"

            else:
                data_str += self.dumps(value)

            json_str += data_str

        json_str = json_str[:1] + json_str[3:] + "}"  # cut off first comma in json str

        return json_str

    def make_str_list(self, value):
        current_str = "["

        for element in value:
            current_str += ", "

            if isinstance(element, bool):

                if element:
                    current_str += "true"
                else:
                    current_str += "false"

            elif isinstance(element, bytes):
                integer_element = "bytes_" + str(len(element)) + "_" + str(int.from_bytes(element, "big"))
                current_str += f"\"{integer_element}\""

            elif isinstance(element, (int, float)):
                current_str += str(element)

            elif isinstance(element, str):
                current_str += f"\"{element}\""

            elif isinstance(element, (list, set, frozenset, tuple)):
                current_str += f"{self.make_str_list(element)}"

            elif isinstance(element, type(None)):
                current_str += "null"

            else:
                current_str += self.dumps(element)

        current_str = current_str[:1] + current_str[3:] + "]"

        return current_str

    def deserialize_from(self, my_str_json):
        my_str_json = my_str_json[1:len(my_str_json) - 1]
        str_items = self.find_items_jsonstr(my_str_json)
        result = self.make_dict_json(str_items)

        return result

    def find_items_jsonstr(self, my_str_json):
        str_items = []
        str_item = ""
        stack_brakets = []
        stack_squre_brakets = []
        stack_qoutes = []

        for i in range(len(my_str_json)):

            if my_str_json[i] == "\"":
                if len(stack_qoutes) == 0:
                    stack_qoutes.append("\"")
                else:
                    stack_qoutes.pop()

            if len(stack_qoutes) == 0:
                if my_str_json[i] == "{":
                    stack_brakets.append("{")

                if my_str_json[i] == "}":
                    stack_brakets.pop()

                if my_str_json[i] == "[":
                    stack_squre_brakets.append("[")

                if my_str_json[i] == "]":
                    stack_squre_brakets.pop()

            if my_str_json[i] == "," and not (len(stack_brakets)) and not (len(stack_squre_brakets)):
                str_items.append(str_item)
                str_item = ""
                continue

            str_item += my_str_json[i]

        str_items.append(str_item)

        return str_items

    def make_dict_json(self, my_str_items):
        my_dict = {}

        if len(my_str_items) != 0:
            my_str_items[0] = " " + my_str_items[0]  # добавляем пробел в начало превого будующего ключа, чтобы корректно обрезать его в дальнейшем вместе с остальными ключами

            for item in my_str_items:
                key_value = item.split(": ", 1)  # получаем ключ значения из нашего списка items(строк)

                if len(key_value) == 2:
                    key_value[0] = key_value[0][2:len(
                        key_value[0]) - 1]  # преобразуем наш ключ, чтобы записать его в словарь без кавычек json
                    key_value[1] = self.check_type_json(key_value[1])  # определяем тип значения json строки
                    my_dict[key_value[0]] = key_value[1]

        return my_dict

    def check_type_json(self, my_value):

        if my_value[:7] == '"bytes_':  # structer of bytes "bytes_(count of bytes)_(integer digitals)
            str_intger = re.findall(r'_\d+_', my_value)[0]  # take a count of bytes in string
            count_bytes = int(str_intger[1:len(str_intger) - 1])  # convert in integer
            str_intger = re.findall(r"_\d+", my_value)[1]  # take a integer difitals
            integer_value = int(str_intger[1:])
            my_value = integer_value.to_bytes(count_bytes, "big")  # convert all in bytesc

            return my_value

        elif my_value[0] == '"':
            my_value = my_value[1:len(my_value) - 1]

            return my_value

        elif my_value == "true":

            return True

        elif my_value == "false":

            return False

        elif my_value[0] == "[":
            my_list = []
            my_value = my_value[1:len(my_value) - 1]
            my_str = ""
            stack_bracket = []
            stack_square_bracket = []
            stack_qoutes = []

            for i in range(len(my_value)):

                if my_value[i] == "\"":
                    if len(stack_qoutes) == 0:
                        stack_qoutes.append("\"")
                    else:
                        stack_qoutes.pop()

                if len(stack_qoutes) == 0:

                    if my_value[i] == "{":
                        stack_bracket.append("{")

                    if my_value[i] == "}":
                        stack_bracket.pop()

                    if my_value[i] == "[":
                        stack_square_bracket.append("[")

                    if my_value[i] == "]":
                        stack_square_bracket.pop()

                if my_value[i] == ',' and len(stack_qoutes) == 0 and len(stack_bracket) == 0 and len(
                        stack_square_bracket) == 0:

                    if my_str[0] == " ":
                        my_str = my_str[1:len(my_str)]

                    result = self.check_type_json(my_str)
                    my_list.append(result)
                    my_str = ""
                    continue

                my_str += my_value[i]

            if len(my_str) != 0:

                if my_str[0] == " ":
                    my_str = my_str[1:len(my_str)]

                my_list.append(self.check_type_json(my_str))

            return my_list

        elif my_value[0] == "{":

            return self.deserialize_from(my_value)

        elif my_value == "null":

            return None

        for i in range(len(my_value)):

            if my_value[i] == ".":
                return float(my_value)

        return int(my_value)
