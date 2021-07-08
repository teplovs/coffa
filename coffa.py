#!/usr/bin/env python
# Copyright (c) 2021 Ivan Zadvornov

from coffa import tokenizer


print(list(tokenizer.tokenize(input("> "))))
