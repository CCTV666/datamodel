import setuptools


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setuptools.setup(
    name="datamodel",
    version="0.0.3",
    author="黄江桂",
    author_email="780810441@qq.com",
    description="一个可以从 JSON 映射到 Python 类的模块。",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/hjzCy/datamodel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# 编译：
# pip install --upgrade setuptools wheel
# python setup.py sdist bdist_wheel
# 上传：
# pip install --upgrade setuptools twine
# python -m twine upload --repository pypi dist/*
