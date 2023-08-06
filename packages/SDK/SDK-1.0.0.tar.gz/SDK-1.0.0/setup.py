#-*- encoding:utf-8 -*-
__author__ = "zhouruifu"
__datetime__ = "2019/9/24 15:30"
__desc__ = """
@File: setup.py 是 setuptools 的构建脚本，用于告知 setuptools 我们要上传到PYPI的库的信息（库名、版本信息、描述、环境需求等）

参数解析：
    name：库名
    version：版本号
    author：作者
    author_email：作者邮箱（如：别人发现了bug或者提建议给我们添加功能联系我们用的）
    description：简述
    long_description：详细描述（一般会写在README.md中）
    long_description_content_type：README.md中描述的语法（一般为markdown）
    url：库/项目主页，一般我们把项目托管在GitHub，放该项目的GitHub地址即可
    packages：使用setuptools.find_packages()即可，这个是方便以后我们给库拓展新功能的（详情请看官方文档）
    classifiers：指定该库依赖的Python版本、license、操作系统之类的
    
    
MIT LICENSE 的大概意思是
    软件可以随便用，随便改
    可以免费，可以收费
    软件的源文件里必须有这个许可证文档
    我提供这个软件不是为了违法，你要用它来违法，那与我无关
    你用这个软件犯事了，责任全在你自己，与其他贡献者无关
"""

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SDK",
    version="1.0.0",
    author="zhouruifu",
    author_email="rocket_2014@126.com",
    description="Unified data transmission interface",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)