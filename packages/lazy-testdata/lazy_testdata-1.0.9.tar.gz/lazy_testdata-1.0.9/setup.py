import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lazy_testdata",
    version="1.0.9",
    author="YuWeiPeng",
    author_email="404051211@qq.com",
    description="""
    testdata include chinese personal four element and offen use datetime 测试数据包含随机生成的中国公民四要素，及常用的日期时间
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.cnblogs.com/yicaifeitian/",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent", ]

    ,
)
