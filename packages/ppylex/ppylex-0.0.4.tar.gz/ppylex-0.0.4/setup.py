
from setuptools import setup, find_packages
from distutils.core import setup, Extension

module1 = Extension('demo',
                    sources = ['demo_module.c']
                    )

setup(
    name = "ppylex",
    version = "0.0.4",
    # keywords = ("pip", "SICA","featureextraction"),
    description = "An feature extraction algorithm",
    long_description = "An feature extraction algorithm, improve the FastICA",
    license = "MIT Licence",

    # url = "https://github.com/LiangjunFeng/SICA",
    author = "jnddd",
    author_email = "122296743@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "linux_x86_64",
    install_requires = ["numpy"],
    ext_modules = [module1]
)