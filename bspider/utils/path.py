import os

ROOT_PATH = os.path.split(os.path.realpath(__file__))[0][:-5]

if __name__ == '__main__':
    print(ROOT_PATH)
