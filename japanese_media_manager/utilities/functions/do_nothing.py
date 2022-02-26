from typing import Callable
from inspect import getsource
from textwrap import dedent
from ast import AST
from ast import parse
from ast import Expr
from ast import Return
from ast import Constant
from ast import Pass
from ast import List
from ast import FunctionDef

def is_docstring(item: AST) -> bool:
    """
    判断一个抽象语法树中的元素是否是 docstring.

    :param item: 抽象语法树中的元素.
    """

    if not isinstance(item, Expr):
        return False
    if not isinstance(item.value, Constant):
        return False
    return isinstance(item.value.value, str)

def is_return_empty_list(item: AST) -> bool:
    """
    判断一个抽象语法树中的元素是否是 ``return []``.

    :param item: 抽象语法树中的元素.
    """

    if not isinstance(item, Return):
        return False
    if not isinstance(item.value, List):
        return False
    return not bool(item.value.elts)

def is_return_none(item: AST) -> bool:
    """
    判断一个抽象语法树中的元素是否是 ``return`` 或者 ``return None``.

    :param item: 抽象语法树中的元素.
    """

    if not isinstance(item, Return):
        return False
    if item.value is None:
        return True
    if not isinstance(item.value, Constant):
        return False
    return item.value.value is None

def is_pass(item: AST) -> bool:
    """
    判断一个抽象语法树中的元素是否是 ``pass`` 语句.

    :param item: 抽象语法树中的元素.
    """

    return isinstance(item, Pass)

def is_ellipsis(item: AST) -> bool:
    """
    判断一个抽象语法树中的元素是否是 ``...`` 语句.

    :param item: 抽象语法树中的元素.
    """

    if not isinstance(item, Expr):
        return False
    if not isinstance(item.value, Constant):
        return False
    return item.value.value is ...

def do_nothing(function: Callable) -> bool:
    """
    判断一个函数 :py:obj:`function` 是否什么也没做. 如果什么也没做, 就返回 ``True``, 否则返回 ``False``.

    这个函数被用在 :py:obj:`utilities.crawlers.Base` 中, 用于判断子类实现了哪些成员方法.

    .. code-block:: python
        :caption: 几个什么也没做的函数示例

        def func_a(*args, **kwargs):
            return

        def func_b(*args, **kwargs):
            '''
            do nothing
            '''

        def func_c(*args, **kwargs):
            return None

        def func_d(*args, **kwargs):
            ...

    :param function: 可执行函数, 但是不可以是 Lambda 函数, 也不可以是可执行的对象(实现了 :py:obj:`__call__` 方法).
    """

    tree = parse(dedent(getsource(function)))
    function_definition, *_ = tree.body

    if not isinstance(function_definition, FunctionDef):
        return False

    method = lambda e: any(method(e) for method in (is_return_none, is_pass, is_ellipsis, is_docstring, is_return_empty_list))
    for expression in function_definition.body:
        if not method(expression):
            return False
    return True
