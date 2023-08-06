# Copyright (c) 2019 William Emerison Six
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def var(fn, *args, **kwargs):
    """
    Creates a static local variable in the calling function's scope.

    >>> import staticlocal
    >>> def foo():
    ...     x = 1
    ...     staticlocal.var(fn=foo, y=3,z=6)
    ...     x = x + 1
    ...     foo.y = foo.y+1
    ...     foo.z = foo.z+1
    ...     return x, foo.y, foo.z
    ...
    >>> foo()
    (2, 4, 7)
    >>> foo()
    (2, 5, 8)
    >>> foo()
    (2, 6, 9)
    >>> foo()
    (2, 7, 10)
"""
    # set all the bindings on the function itself
    for k,v in kwargs.items():
        try:
            getattr(fn, k)
        except:
            setattr(fn, k, v)
