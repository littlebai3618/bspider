# @Time    : 2019/11/6 4:01 下午
# @Author  : baii
# @File    : base_item
# @Use     : 解析对象


class Item(object):
    """
    item对象,
    """
    all_field = []

    def __init__(self, **kwargs):
        """
        构造函数
        """
        self.field_value = kwargs

    # 增加元素
    def __setitem__(self, key, value):
        self.field_value[key] = value

    # 取出元素
    def __getitem__(self, item):
        return self.field_value[item]

    # 删除元素
    def __delitem__(self, key):
        del self.field_value[key]

    def pop(self, key):
        return self.field_value.pop(key)

    def get(self, key):
        return self.field_value.get(key)

    def keys(self):
        return self.field_value.keys()

    def values(self):
        return self.field_value.values()

    def clear(self):
        return self.field_value.clear()

    def __repr__(self):
        return f'<Item: {len(self.field_value)} field>'

    __str__ = __repr__

class MySQLSaverItem(Item):

    def __init__(self, table_name: str, db: str, **kwargs):
        """
        构造函数
        """
        self.table_name = table_name
        self.db = db
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<MySQLSaverItem: {len(self.field_value)} field>'