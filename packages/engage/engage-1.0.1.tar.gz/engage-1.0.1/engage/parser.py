import ast
from typing import Any, Dict, List, Tuple, Optional, Iterator, Union
import warnings

import astor


def fetch_functions(content: str, return_body: bool = False) -> Iterator[Union[ast.FunctionDef, ast.AsyncFunctionDef]]:
    body = ast.parse(content)
    for part in ast.walk(body):
        if isinstance(part, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield part
    if return_body:
        yield body


def has_return(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
    return any(isinstance(node, ast.Return) for node in ast.walk(func))


def get_return_doc(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> str:
    return astor.to_source(func.returns).strip() if func.returns else None


def get_args(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> List[Tuple[str, Optional[str]]]:
    return [(arg.arg, (astor.to_source(arg.annotation)) if arg.annotation else None) for arg in func.args.args]


def get_kwargs(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> List[Tuple[str, Optional[str], str]]:
    return [(arg.arg, (astor.to_source(arg.annotation) if arg.annotation else None), astor.to_source(default))
            for arg, default in zip(func.args.kwonlyargs, func.args.kw_defaults)]


def get_kwarg(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Tuple[Optional[str], Optional[str]]:
    return func.args.kwarg.arg, (astor.to_source(func.args.kwarg.annotation) if func.args.kwarg.annotation else None)


def get_vararg(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Tuple[Optional[str], Optional[str]]:
    return func.args.vararg.arg, (astor.to_source(func.args.vararg.annotation) if func.args.vararg.annotation else None)


def get_indent(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> int:
    sorted_parts = sorted(filter(lambda x: x.col_offset != -1, func.body), key=lambda x: x.col_offset)
    try:
        return sorted_parts[0].col_offset
    except IndexError:
        warnings.warn("Unable to identify indentation for function {}, make sure the function is more than just a "
                      "docstring. This can be fixed by added 'pass'".format(func.name), UserWarning)
        return 4


def get_doc(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Optional[str]:
    if func.body:
        if isinstance(func.body[0], ast.Expr) and isinstance(func.body[0].value, ast.Str):
            return func.body[0].value.s


def func_summary(func: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Dict[str, Any]:
    return {
        "returns": has_return(func),
        "return_doc": get_return_doc(func),
        "vararg": get_vararg(func) if func.args.vararg else None,
        "kwarg": get_kwarg(func) if func.args.kwarg else None,
        "default_arg": get_kwargs(func),
        "arg": get_args(func),
        "docs": get_doc(func),
        "name": func.name,
        "indent": get_indent(func)
    }
