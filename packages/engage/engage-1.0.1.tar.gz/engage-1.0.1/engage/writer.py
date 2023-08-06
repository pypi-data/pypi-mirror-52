import ast
import inspect
from typing import Tuple, Type, Optional

from engage.parser import fetch_functions, func_summary

from astor import to_source


class Writer:

    def __init__(self):
        self.docs = []

    def update_arg(self, arg: Tuple[str, Optional[str]]):
        raise NotImplemented

    def update_kwargs(self, kwarg: Tuple[str, Optional[str]]):
        raise NotImplemented

    def update_vararg(self, vararg: [str, Optional[str]]):
        raise NotImplemented

    def update_default_arg(self, arg: Tuple[str, Optional[str], str]):
        raise NotImplemented

    def update_return(self, return_doc: Optional[str]):
        raise NotImplemented

    def digest(self, indent: int) -> str:
        split = "\n" + " " * indent
        return split + split.join(self.docs) + split


class Sphinx(Writer):

    def update_arg(self, arg: Tuple[str, Optional[str]]):
        if arg[0] == 'self':
            return
        self.docs.append(":param {}: ".format(arg[0]))
        if arg[1] is not None:
            self.docs.append(":type {}: {}".format(arg[0], arg[1].strip("\n() ")))
        else:
            self.docs.append(":type {}: ".format(arg[0]))

    def update_default_arg(self, arg: Tuple[str, Optional[str], str]):
        self.docs.append(":param {}:  (Default: {})".format(arg[0], arg[2].strip("\n() ")))
        if arg[1] is not None:
            self.docs.append(":type {}: {}".format(arg[0], arg[1].strip("\n() ")))
        else:
            self.docs.append(":type {}: ".format(arg[0]))

    def update_kwarg(self, kwarg: Tuple[str, Optional[str]]):
        self.docs.append(":param **{}: ".format(kwarg[0]))
        if kwarg[1] is not None:
            self.docs.append(":type **{}: {}".format(kwarg[0], kwarg[1].strip("\n() ")))
        else:
            self.docs.append(":type **{}: ".format(kwarg[0]))

    def update_return(self, return_doc: Optional[str]):
        self.docs.append(":return: ")
        if return_doc is not None:
            self.docs.append(":rtype: {}".format(return_doc))
        else:
            self.docs.append(":rtype: ")

    def update_vararg(self, vararg: [str, Optional[str]]):
        self.docs.append(":param *{}: ".format(vararg[0]))
        if vararg[1] is not None:
            self.docs.append(":type *{}: {}".format(vararg[0], vararg[1].strip("\n() ")))
        else:
            self.docs.append(":type *{}: ".format(vararg[0]))

    def update_docs(self, docs: str):
        cleaned = inspect.cleandoc(docs)
        self.docs = cleaned.split("\n") + [""] + self.docs


def update_module(contents: str, writer: Type[Writer] = Sphinx) -> str:
    func_data = map(func_summary, fetch_functions(contents))
    summary = []
    for function in func_data:
        author = writer()
        for name, value in function.items():
            if value and hasattr(author, "update_" + name):
                if not isinstance(value, list):
                    getattr(author, "update_" + name)(value)
                else:
                    for item in value:
                        getattr(author, "update_" + name)(item)
        summary.append(author.digest(function['indent']))

    func_generator = fetch_functions(contents, True)
    for doc, part in zip(summary, func_generator):
        if isinstance(part.body[0], ast.Expr) and isinstance(part.body[0].value, ast.Str):
            part.body[0].value.s = doc
        else:
            e = ast.Expr([ast.Str(doc)])
            part.body.insert(0, e)
    return to_source(next(func_generator))
