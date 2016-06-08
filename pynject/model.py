class ListType:
    def __init__(self, sub_type: type):
        self.sub_type = sub_type

    def __repr__(self):
        return '<class \'list[{}]\'>'.format(self.sub_type.__name__)


class UnresolvedListType:
    def __init__(self, sub_type_provider):
        self.sub_type_provider = sub_type_provider

    @property
    def sub_type(self):
        return self.sub_type_provider()

    def __repr__(self):
        return '<class \'list[{}]\'>'.format(self.sub_type.__name__)


class PynjectAttribute:
    def __init__(self, name, attr_type):
        self.name = name
        self.attr_type = attr_type

    def __repr__(self):
        return 'PycksonAttribute({}, {})'.format(self.name,
                                                 self.attr_type)


class PynjectUnresolvedAttribute:
    def __init__(self, name, type_provider):
        self.name = name
        self.type_provider = type_provider

    @property
    def attr_type(self):
        return self.type_provider()

    def __repr__(self):
        return 'PycksonUnresolvedAttribute({}, {})'.format(self.name,
                                                           self.attr_type)


class PynjectModel:
    def __init__(self, attributes):
        self.attributes = attributes

    def __repr__(self):
        return repr(self.attributes)
