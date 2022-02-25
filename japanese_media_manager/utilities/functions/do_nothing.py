from typing import Callable
from inspect import getsource
from textwrap import dedent
from ast import AST
from ast import parse
from ast import Expr
from ast import Return
from ast import Constant
from ast import Pass
from ast import FunctionDef

def is_docstring(item: AST) -> bool:
    if not isinstance(item, Expr):
        return False
    if not isinstance(item.value, Constant):
        return False
    return isinstance(item.value.value, str)

def is_return_none(item: AST) -> bool:
    if not isinstance(item, Return):
        return False
    if item.value is None:
        return True
    if not isinstance(item.value, Constant):
        return False
    return item.value.value is None

def is_pass(item: AST) -> bool:
    return isinstance(item, Pass)

def is_ellipsis(item: AST) -> bool:
    if not isinstance(item, Expr):
        return False
    if not isinstance(item.value, Constant):
        return False
    return item.value.value is ...

def do_nothing(function: Callable) -> bool:
    """
    判断一个函数 :py:obj:`function` 是否什么也没做. 如果什么也没做, 就返回 ``True``, 否则返回 ``False``.

    :param function: 可执行函数, 但是不可以是 Lambda 函数, 也不可以是可执行的对象(实现了 :py:obj:`__call__` 方法).
    """

    tree = parse(dedent(getsource(function)))
    function_definition, *_ = tree.body

    if not isinstance(function_definition, FunctionDef):
        return False

    expressions = [item for item in function_definition.body if not is_docstring(item)]
    return all(is_return_none(expression) or is_pass(expression) or is_ellipsis(expression) for expression in expressions)
