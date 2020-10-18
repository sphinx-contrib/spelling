#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Spelling checker extension for Sphinx.
"""
from typing import Iterator, List, Optional, Tuple

try:
    import enchant
    from enchant.tokenize import Filter, get_tokenizer
except ImportError as imp_exc:
    enchant_import_error: Optional[ImportError] = imp_exc
else:
    enchant_import_error = None


class SpellingChecker:
    """Checks the spelling of blocks of text.

    Uses options defined in the sphinx configuration file to control
    the checking and filtering behavior.
    """

    def __init__(
        self,
        lang: str,
        suggest: bool,
        word_list_filename: Optional[str],
        tokenizer_lang: str = 'en_US',
        filters: Optional[List[str]] = None,
        context_line: bool = False
    ):
        if enchant_import_error is not None:
            raise RuntimeError(
                'Cannot instantiate SpellingChecker '
                'without PyEnchant installed',
            ) from enchant_import_error
        if filters is None:
            filters = []
        self.dictionary = enchant.DictWithPWL(lang, word_list_filename)
        self.tokenizer = get_tokenizer(tokenizer_lang, filters=filters)
        self.original_tokenizer = self.tokenizer
        self.suggest = suggest
        self.context_line = context_line

    def push_filters(self, new_filters: List[Filter]) -> None:
        """Add a filter to the tokenizer chain.
        """
        t = self.tokenizer
        for f in new_filters:
            t = f(t)
        self.tokenizer = t

    def pop_filters(self) -> None:
        """Remove the filters pushed during the last call to push_filters().
        """
        self.tokenizer = self.original_tokenizer

    def check(self, text: str) -> Iterator[Tuple[str, List[str], str]]:
        """Yields bad words and suggested alternate spellings.
        """
        for word, pos in self.tokenizer(text):
            correct = self.dictionary.check(word)
            if correct:
                continue

            suggestions = self.dictionary.suggest(word) if self.suggest else []
            line = line_of_index(text, pos) if self.context_line else ""

            yield word, suggestions, line


def line_of_index(text: str, index: int) -> str:
    try:
        line_start = text.rindex("\n", 0, index) + 1
    except ValueError:
        line_start = 0
    try:
        line_end = text.index("\n", index)
    except ValueError:
        line_end = len(text)

    return text[line_start:line_end]
