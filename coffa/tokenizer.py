# Copyright (c) 2021 Ivan Zadvornov

import re

from dataclasses import dataclass
from typing import Generator


rules = {
    "Number": r"(0|[1-9][0-9]*)(\.[0-9]+)?",
    "Operator": r"\+|\-|\*|\/|\%",
    "Whitespace": r"[ \t]+",
    "Newline": r"(\r?\n[ \t]*)+"
}


@dataclass
class Token():
    type: str
    value: str


def tokenize(
    string: str,
    skip_whitespace: bool = True
) -> Generator[Token, None, None]:
    # while there is input left
    while len(string) > 0:
        found_match = False

        # iterate over rules
        for rule, regex in rules.items():
            # check for matches
            match = re.match(regex, string, re.M)

            # if there is a match
            if match:
                # get all the matching text
                value = match.group()

                found_match = True

                if not (rule == "Whitespace" and skip_whitespace):
                    # yield our token
                    yield Token(rule, value)

                # remove tokenized part of our string
                string = string[len(value):]

        if not found_match:
            raise SyntaxError(f'Unexpected character "{string[0]}"')
