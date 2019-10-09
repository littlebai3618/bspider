# @Time    : 2018/3/14 下午2:48
# @Author  : 白尚林
# @File    : root_path
# @Use     : 获取根目录
import os

ROOT_PATH = os.path.split(os.path.realpath(__file__))[0][:-5]

if __name__ == '__main__':
    print(ROOT_PATH)
