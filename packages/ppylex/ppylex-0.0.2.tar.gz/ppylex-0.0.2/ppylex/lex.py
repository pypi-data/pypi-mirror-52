import ctypes
adder = ctypes.cdll.LoadLibrary('./yy.so')
adder.yylex()