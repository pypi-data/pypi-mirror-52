
from setuptools import setup, find_packages
from distutils.core import setup, Extension

module1 = Extension('demo',
                    sources = ['./ppylex/demo_module.c']
                    )
module2 = Extension('yylex',
                    sources= ['lex.yy.c'] 
                    )

setup(
    name = "ppylex",
    version = "0.0.6",
    description = "An feature extraction algorithm",
    long_description = "An feature extraction algorithm, improve the FastICA",
    license = "MIT Licence",
    author = "jnddd",
    author_email = "122296743@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "linux_x86_64",
    install_requires = ["numpy"],
    ext_modules = [module1,module2]
)