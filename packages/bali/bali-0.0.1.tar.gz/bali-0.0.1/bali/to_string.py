
def to_string(original_class):

    def is_primitive(obj):
        return not hasattr(obj, '__dict__')

    def __str__(self):
        builder = []

        for att in dir(self):
            if not att.startswith("_"):
                if isinstance(self.__getattribute__(att), list) or isinstance(self.__getattribute__(att), tuple):
                    list_builder = []
                    for list_item in self.__getattribute__(att):
                        if not is_primitive(list_item):
                            list_builder.append(__str__(list_item))
                        else:
                            list_builder.append(str(list_item))
                    builder.append('{' + str(att) + ' = [' + ', '.join(list_builder) + ']}')
                elif isinstance(self.__getattribute__(att), dict):

                    dict_builder = []
                    for key, value in self.__getattribute__(att).items():
                        if not is_primitive(value):
                            dict_builder.append(__str__(key) + ' : ' + __str__(value))
                        else:
                            dict_builder.append(str(key) + ' : ' + str(value))
                    builder.append('{' + str(att) + ' = ' + ', '.join(dict_builder) + '}')
                elif not is_primitive(self.__getattribute__(att)):
                    builder.append('{' + str(att) + ' = ' + __str__(self.__getattribute__(att)) + '}')
                else:
                    builder.append('{' + str(att) + ' = ' + str(self.__getattribute__(att)) + '}')
        return ', '.join(builder)

    original_class.__str__ = __str__
    return original_class
