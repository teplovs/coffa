# Copyright (c) 2021 Ivan Zadvornov

import json

from .tokenizer import Token


def _convert_nodes_to_dict(item):
    if type(item) is Node:
        item = { "type": item.type, **item.options }
        
        for key, value in item.items():
            item[key] = _convert_nodes_to_dict(value)
    elif type(item) is list:
        item = list(map(_convert_nodes_to_dict, item))
    
    return item


class Node():
    def __init__(self, type: str, **options):
        self.type = type
        self.options = options

    def __str__(self):
        return json.dumps(_convert_nodes_to_dict(self), indent=2)

    __repr__ = __str__


class Parser():
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
        left = self.parse_number()

        # TODO: check if operator is valid in this context
        if self.peek("Operator"):
            operator = self.consume("Operator")
            right = self.parse_number()
            return Node("BinaryOperation", left=left, operator=operator.value, right=right)
        
        return left

    def parse_number(self):
        token = self.consume("Number")
        return Node("Number", value=token.value)

    def consume(self, type: str):
        if len(self.tokens) == 0:
            raise SyntaxError(f"Expected {type}, but got end of file")
        
        token = self.tokens[0]

        if token.type != type:
            raise SyntaxError(f"Expected {type}, but got {token.type}")

        self.tokens.pop(0)
        return token

    def peek(self, type: str):
        return self.tokens[0].type == type
