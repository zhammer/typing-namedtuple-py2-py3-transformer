from typing import List, Optional, Tuple, Type, Union, Set

import libcst as cst
import libcst.matchers as m

from typing_namedtuple_transformer.helpers import (
    with_added_imports,
    name_or_attribute_matches,
    name_or_attribute_matches_one_of,
)


class TransformError(Exception):
    """
    Error raised upon encountering a known error while attempting to transform
    the tree.
    """


class TypingNamedTupleTransformer(cst.CSTTransformer):
    """
    """

    def __init__(self) -> None:
        self.simple_statement_line_stack: List[bool] = []
        self.name: Optional[str] = None
        self.namedtuple_func: Optional[cst.BaseExpression] = None
        self.attributes: List[Tuple[str, cst.BaseExpression]] = []

    def visit_Module(self, node):
        return True

    @property
    def in_namedtuple(self) -> bool:
        return self.simple_statement_line_stack and self.simple_statement_line_stack[-1]

    def visit_SimpleStatementLine(
        self, node: cst.SimpleStatementLine
    ) -> Optional[bool]:
        is_py2_typing_namedtuple = self.is_py2_typing_namedtuple(node)
        if is_py2_typing_namedtuple and self.in_namedtuple:
            raise TransformError("Entering a py2 typing namedtuple while already in one.")

        self.simple_statement_line_stack.append(is_py2_typing_namedtuple)

        if is_py2_typing_namedtuple:
            self.namedtuple_func = node.body[0].value.func
            self.name = node.body[0].value.args[0].value.value[1:-1]

        return True

    def visit_Tuple(self, node: cst.Tuple) -> None:
        if not self.in_namedtuple:
            return

        self.attributes.append(
            (node.elements[0].value.value[1:-1], node.elements[1].value)
        )

    def leave_SimpleStatementLine(
        self, node: cst.SimpleStatementLine, updated_node: cst.SimpleStatementLine
    ) -> cst.SimpleStatementLine:
        leaving_py2_typing_namedtuple = self.simple_statement_line_stack.pop()
        if not leaving_py2_typing_namedtuple:
            return updated_node

        class_annotations = [
            cst.SimpleStatementLine(
                body=[
                    cst.AnnAssign(
                        target=cst.Name(attribute_name),
                        annotation=cst.Annotation(annotation=attribute_value),
                    )
                ]
            )
            for attribute_name, attribute_value in self.attributes
        ]

        classdef_node = cst.ClassDef(
            name=cst.Name(self.name),
            bases=[cst.Arg(self.namedtuple_func)],
            body=cst.IndentedBlock(body=class_annotations),
            leading_lines=updated_node.leading_lines
        )

        # reset state
        self.name = None
        self.namedtuple_func = None
        self.attributes = []

        return classdef_node

    @staticmethod
    def is_py2_typing_namedtuple(node: cst.SimpleStatementLine) -> bool:
        return m.matches(
            node,
            m.SimpleStatementLine(
                body=[
                    m.Assign(
                        value=m.Call(
                            func=(
                                m.Name("NamedTuple")
                                | m.Attribute("typing", "NamedTuple")
                            )
                        )
                    ),
                ]
            ),
        )
