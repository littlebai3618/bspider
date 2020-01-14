from bspider.core.custom_module import BaseCustomModule


class BasePipeline(BaseCustomModule):

    def process_item(self, item):
        """
        对item进行处理,各个pipeline重写
        注意按照scrapy的风格
        可以yield返回也可以return
        返回类型为自订定义的类型，会传递给后面的pipeline，返回None将会丢弃这个item
        :param item:
        :return:
        """
        return item
