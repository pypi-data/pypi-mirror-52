import argparse
from ylcli.libs import entry, other
import os

parser = argparse.ArgumentParser()

"""
    使用不带- 或者 --的name参数，即可做到省略前缀，如使用 yundou-cli app
    下面获取到的name即是app
"""

parser.add_argument('name', default='YunDou', type=str)

args = parser.parse_args()


def main():
    name = args.name
    # 获取安装文件所在目录里
    d = os.path.dirname(__file__)
    # 获取脚本在命令行执行时所在目录
    work_path = os.getcwd()
    # 生成项目主文件 如YunDou.py
    entry(d, work_path, name)
    # 读取模板生成项目其他文件
    other(d, work_path)


if __name__ == '__main__':
    main()
