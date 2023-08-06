from distutils.core import setup

setup(name="hzpromise",
     author="Huzheng",
     author_email= "backbye@163.com",
     description= "An implementation of Promises/A+ for Python",
     version="1.0.1",
     py_modules=["hzpromise", "thenable"],
     python_requires='>=3.5'
     )

