# Copyright (c) 2021 Ivan Zadvornov

import json

from .tokenizer import Token
from typing import Union


def _convert_nodes_to_dict(item):
    """
    This function is used to convert every node
    in the tree to a dictionary that can be
    outputted using json.dumps
    """

    # If the item is a node
    if type(item) is Node:
        # Convert the node to dictionary
        item = {"type": item.type, **item.options}

        # Convert child nodes if there are any
        for key, value in item.items():
            item[key] = _convert_nodes_to_dict(value)
    # Else if the item is a list
    elif type(item) is list:
        # Call this function on every child node
        item = list(map(_convert_nodes_to_dict, item))

    return item


class Node:
    def __init__(self, type: str, **options):
        self.type = type
        self.options = options

    def __str__(self):
        return json.dumps(_convert_nodes_to_dict(self), indent=2)

    __repr__ = __str__


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def parse_module(self):
        node = Node("Module", body=[])

        while self.tokens:
            node.options["body"].append(self.parse_expression())

            if self.tokens:
                self.consume("Newline")

        return node

    def parse_expression(self):
        left = self.parse_expression_atom()
        return self.check_for_binary_operation(left)

    def parse_expression_atom(self):
        """
        This is a function to parse strings, numbers, lists, dictionaries etc.
        """

        # TODO: check for unary operations
        # TODO: add support for strings, lists and dictionaries
        return self.parse_number()

    def parse_number(self):
        token = self.consume("Number")
        return Node("Number", value=token.value)

    def check_for_binary_operation(self, left):
        precedence = {"+": 10, "-": 10, "*": 20, "/": 20, "%": 20}

        binary_operators = tuple(precedence.keys())

        if self.peek("Operator", binary_operators):
            operator = self.consume("Operator").value
            right = self.parse_expression_atom()

            if (
                left.type == "BinaryOperation"
                and precedence[left.options["operator"]] < precedence[operator]
            ):
                node = Node(
                    "BinaryOperation",
                    left=left.options["left"],
                    operator=left.options["operator"],
                    right=Node(
                        "BinaryOperation",
                        left=left.options["right"],
                        operator=operator,
                        right=right,
                    ),
                )
            else:
                node = Node(
                    "BinaryOperation", left=left, operator=operator, right=right
                )

            return self.check_for_binary_operation(node)

        return left

    def consume(self, type: Union[str, tuple[str]]):
        """
        Function to "eat" a token and throw an error
        if it has a non-corresponding type
        """

        if isinstance(type, str):
            type_str = type
        else:
            type_str = ", ".join(type)

        if len(self.tokens) == 0:
            raise SyntaxError(f"Expected {type_str}, but got end of file")

        token = self.tokens[0]

        if (isinstance(type, str) and token.type != type) or (
            not isinstance(type, str) and token.type in type
        ):
            raise SyntaxError(f"Expected {type_str}, but got {token.type}")

        self.tokens.pop(0)
        return token

    def peek(
        self, type: Union[str, tuple[str]], value: Union[None, str, tuple[str]] = None
    ):
        """
        Function to check if the next token has the corresponding type
        """

        if len(self.tokens) == 0:
            token = Token("eof", "\0")
        else:
            token = self.tokens[0]

        type_matches = (
            token.type == type if isinstance(type, str) else token.type in type
        )

        value_matches = (
            True
            if not value
            else (
                token.value == value if isinstance(value, str) else token.value in value
            )
        )

        return type_matches and value_matches
