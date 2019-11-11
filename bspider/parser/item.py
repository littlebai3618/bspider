# @Time    : 2019/11/6 4:01 下午
# @Author  : baii
# @File    : base_item
# @Use     : 解析对象


class Item(object):
    """
    item对象,
    """

    def __init__(self, **kwargs):
        """
        构造函数
        """
        self.capacity = kwargs

    # 增加元素
    def __setitem__(self, key, value):
        self.capacity[key] = value

    # 取出元素
    def __getitem__(self, item):
        return self.capacity[item]

    # 删除元素
    def __delitem__(self, key):
        del self.capacity[key]

    def pop(self, key):
        return self.capacity.pop(key)

    def get(self, key):
        return self.capacity.get(key)

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

    def __init__(self, table: str, db: str, auto_update: bool=True, **kwargs):
        """
        构造函数
        """
        self.table = table
        self.db = db
        self.auto_update = auto_update
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<MySQLSaverItem: {self.db}{self.table} {len(self.capacity)} field>'