import ctypes
adder = ctypes.cdll.LoadLibrary('../yylex.cpython-37m-x86_64-linux-gnu.so')
adder.yylex()