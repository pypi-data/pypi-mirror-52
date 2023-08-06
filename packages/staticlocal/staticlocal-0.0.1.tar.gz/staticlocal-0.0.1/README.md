static

Python implementation of static local variables.

Static local variables are variables local to a function, which upon
first application, assign a value to the variable.  The value bound
by the variable persists after the function application completes,
so the state is preserved across muliple applications of the function.


```python
>>> import static
>>> def foo():
...     x = 1
...     static.local_var(fn=foo, y=3,z=6)
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
```
