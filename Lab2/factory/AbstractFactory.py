from abc import ABC, abstractmethod


class AbstractFactory(ABC):

    @abstractmethod
    def create_serializer(self, type_ser):
        pass

    def serialize(self, obj, type_ser, initial_type=None, path_file=None):
        serializer = self.create_serializer(type_ser)

        if isinstance(obj, str):

            if initial_type is None:
                raise TypeError("Positional argument string implies a not empty initial type")

            if initial_type == type_ser:
                return obj

            current_ser = self.create_serializer(initial_type)
            obj = current_ser.loads(obj)

        if path_file is None:
            obj_form = serializer.dumps(obj)

        else:
            with open(f"{path_file}", "w") as file:
                obj_form = serializer.dump(obj, file)

        return obj_form

    def deserialize(self, type_ser, obj_form=None, path_file=None):
        serializer = self.create_serializer(type_ser)

        if path_file is None:
            obj = serializer.loads(obj_form)

        else:
            with open(f"{path_file}", "r") as file:
                obj = serializer.load(file)

        return obj
