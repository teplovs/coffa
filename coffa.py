#!/usr/bin/env python
# Copyright (c) 2021 Ivan Zadvornov

from coffa import tokenizer
from coffa.parser import Parser
from pprint import pprint


input_str = input("> ")
tokens = list(tokenizer.tokenize(input_str))
module = Parser(tokens).parse_module()
pprint(module)
