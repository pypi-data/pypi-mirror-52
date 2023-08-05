import numba as nb
import llvmlite.binding as llvm

import pytest
from rbc.irtools import compile_to_LLVM
from rbc.typesystem import Type


def test_simple():

    @nb.njit
    def bar(x):
        return 7

    @nb.extending.overload(len)
    def mylen(x):
        def impl(x):
            return 772234
        return impl

    def foo(x):
        return bar(x) + 1
    
    sig = Type.fromstring('int64(int64)')

    r = compile_to_LLVM([(foo, [sig])], 'host', debug=True)
    print(r)
