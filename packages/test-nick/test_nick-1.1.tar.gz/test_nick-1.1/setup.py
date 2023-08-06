from distutils.core import setup
setup(
    name = "test_nick",
    version = "1.1",
    py_modules = ["test_nick"],
    author = "nick",
    author_email = "287041719@qq.com",
    description = "install the needed packages",
    install_requires = [
       'matplotlib>=2.1.1',
       'numpy>=1.14.0',
       'pandas>=0.21.0',
       'scipy>=1.0.0'
    ],
    python_requires='>=3',
    ) 