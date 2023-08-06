# trollius2asyncio

A tool based on lib2to3 for converting code using trollius to use
asyncio. After installation, run *trollius2asyncio*. It works in the
same way as 2to3.

For example, it will transform this:
```python
import trollius
from trollius import From, Return

@trollius.coroutine
def double_future(future):
    value = yield From(future)
    raise Return(2 * value)
```
into
```python
import asyncio


async def double_future(future):
    value = await future
    return 2 * value
```

## Usage

After installation, run `trollius2asyncio` as you would `2to3`. It takes the
same command-line arguments, including `-h` for help.

## Limitations

It recognises `From`, `trollius.From`, `Return` and `trollius.Return`, without
taking the imports into consideration. Thus, importing trollius as a different
name will confuse it, and `from tornado.gen import Return` will cause the
returns from Tornado to also be rewritten (which should still be a legal
transformation).

It recognises `@trollius.coroutine`, again without taking imports into
consideration. If the decorator is omitted, it won't turn the function into a
coroutine, which will lead to syntax errors if it ends up containing `await`
statements. It also won't apply the transformation if there are additional
decorators inside (i.e., between `@trollius.coroutine` and the definition)
since that would alter the semantics.

The resulting code is not necessarily well-styled e.g., the extra blank line
in the example above. These are limitations of lib2to3 and won't be easy to fix
without risking breaking code in corner cases.

## Release history

### 0.2

- Drop Python 3.4 support (output code uses async and await).

### 0.1.1

- Add licence.

### 0.1

- Initial release.
