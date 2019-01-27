import inspect

from sphinx.util import logging

from .builder import SpellingBuilder
from .directive import SpellingDirective

logger = logging.getLogger(__name__)


def setup(app):
    # If we are running inside the test suite, "app" will be a module.
    if inspect.ismodule(app):
        return
    logger.info('Initializing Spelling Checker')
    app.add_builder(SpellingBuilder)
    # Register the 'spelling' directive for setting parameters within
    # a document
    app.add_directive('spelling', SpellingDirective)
    # Report guesses about correct spelling
    app.add_config_value('spelling_show_suggestions', False, 'env')
    # Set the language for the text
    app.add_config_value('spelling_lang', 'en_US', 'env')
    # Set the language for the tokenizer
    app.add_config_value('tokenizer_lang', 'en_US', 'env')
    # Set a user-provided list of words known to be spelled properly
    app.add_config_value('spelling_word_list_filename',
                         None,
                         'env')
    # Assume anything that looks like a PyPI package name is spelled properly
    app.add_config_value('spelling_ignore_pypi_package_names', False, 'env')
    # Assume words that look like wiki page names are spelled properly
    app.add_config_value('spelling_ignore_wiki_words', True, 'env')
    # Assume words that are all caps, or all caps with trailing s, are
    # spelled properly
    app.add_config_value('spelling_ignore_acronyms', True, 'env')
    # Assume words that are part of __builtins__ are spelled properly
    app.add_config_value('spelling_ignore_python_builtins', True, 'env')
    # Assume words that look like the names of importable modules are
    # spelled properly
    app.add_config_value('spelling_ignore_importable_modules', True, 'env')
    # Add any user-defined filter classes
    app.add_config_value('spelling_filters', [], 'env')
    return {"parallel_read_safe": True}
