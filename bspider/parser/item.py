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

    # 对象可迭代
    def __iter__(self):
        return self.capacity.items()

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

    def __init__(self, table: str, database: str, auto_update: bool = True, **kwargs):
        """
        准备存入MySQL 的Item
        :param table: 存入mysql 的表名
        :param auto_update: 如果为true, 当插入数据已经存在会自动更新已经存在的数据
        :param kwargs: 要插入table的数据
        """
        self.table = table
        self.database = database
        self.auto_update = auto_update
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<MySQLSaverItem: {self.database}->{self.table} {len(self.capacity)} field>'


class RedisSaverItem(Item):

    def __init__(self, db: int = 0, **kwargs):
        """
        Beta Item
        """
        self.db = db
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<RedisSaverItem: {self.db} {len(self.capacity)} field>'


class RabbitMQSaverItem(Item):

    def __init__(self, exchange: str, **kwargs):
        """
        Beta Item
        """
        self.exchange = exchange
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<RabbitMQSaverItem: {self.exchange} {len(self.capacity)} field>'
