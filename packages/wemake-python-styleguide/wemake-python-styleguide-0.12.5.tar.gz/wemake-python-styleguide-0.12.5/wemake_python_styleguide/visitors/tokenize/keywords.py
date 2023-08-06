# -*- coding: utf-8 -*-

import keyword
import tokenize

from typing_extensions import final

from wemake_python_styleguide.violations.consistency import (
    MissingSpaceBetweenKeywordAndParenViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class WrongKeywordTokenVisitor(BaseTokenVisitor):
    """Visits keywords and finds violations related to their usage."""

    def visit_name(self, token: tokenize.TokenInfo) -> None:
        """
        Check keywords related rules.

        Raises:
            MissingSpaceBetweenKeywordAndParenViolation

        """
        if keyword.iskeyword(token.string):
            self._check_space_before_open_paren(token)

    def _check_space_before_open_paren(self, token: tokenize.TokenInfo) -> None:
        if token.line[token.end[1]:].startswith('('):
            self.add_violation(
                MissingSpaceBetweenKeywordAndParenViolation(token),
            )
