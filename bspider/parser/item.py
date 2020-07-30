class Item(object):
    """
    item对象,
    """

    def __init__(self, data_source: str, schema=None, **kwargs):
        """
        :param data_source: 数据源名称
        :param schema: 建表语句，要求有建表权限
        :param kwargs: 要存储的数据
        """
        self.data_source = data_source
        self.capacity = kwargs
        self.schema = schema

    # 增加元素
    def __setitem__(self, key, value):
        self.capacity[key] = value

    # 取出元素
    def __getitem__(self, item):
        return self.capacity[item]

    # 删除元素
    def __delitem__(self, key):
        del self.capacity[key]

    # 对象可迭代
    def __iter__(self):
        return self.capacity.items()

    def pop(self, key):
        return self.capacity.pop(key)

    def get(self, key, default=None):
        return self.capacity.get(key, default)

    def keys(self):
        return self.capacity.keys()

    def values(self):
        return self.capacity.values()

    def clear(self):
        return self.capacity.clear()

    def __repr__(self):
        return f'<Item: {len(self.capacity)} field>'

    __str__ = __repr__


class MySQLSaverItem(Item):

    def __init__(self, data_source: str, table: str, auto_update=True, schema=None, **kwargs):
        super().__init__(data_source, schema, **kwargs)
        self.table = table
        self.auto_update = auto_update
