from distutils.core import setup
setup(
    name='policeMath', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，只测试数学方法', #描述
    author='lieyingsilence', # 作者
    author_email='838469602@qq.com',
    py_modules=['policeMath.demo1','policeMath.demo2'] # 要发布的模块
)