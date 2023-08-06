from distutils.core import setup
setup(
name='lulei_pypitest', # 对外我们模块的名字
version='1.0', # 版本号
description='这是第一个对外发布的测试模块', #描述
author='lulei', # 作者
author_email='Ray110@163.com',
py_modules=['pypi_test.my_pypitest','pypi_test.hello_pypi'] # 要发布的模块
)