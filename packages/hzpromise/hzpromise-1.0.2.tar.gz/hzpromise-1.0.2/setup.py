from distutils.core import setup

with open("version") as f:
    version = f.readline().strip("\n")

def next_version(version):
    print(f"current verison:{version}")
    major_version, minor_version, build_version = [int(i) for i in version.split(".")]
    build_version = build_version + 1
    return '.'.join(str(i) for i in [major_version, minor_version, build_version])

setup(name="hzpromise",
     author="Huzheng",
     author_email= "backbye@163.com",
     description= "An implementation of Promises/A+ for Python",
     version=str(version),
     url = "https://gitee.com/hu321/promise",
     py_modules=["hzpromise", "thenable"],
     python_requires='>=3.5'
     )

with open("version", 'w') as f:
    f.write(next_version(version)+"\n")
