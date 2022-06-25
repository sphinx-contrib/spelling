from docutils.parsers.rst import roles

from . import directive


class WordRole(roles.GenericRole):
    """Let the user indicate that inline text is spelled correctly.
    """

    def __call__(self, role, rawtext, text, lineno, inliner,
                 options={}, content=[]):
        env = inliner.document.settings.env
        docname = env.docname
        good_words = text.split()
        directive.add_good_words_to_document(env, docname, good_words)
        return super().__call__(role, rawtext, text, lineno, inliner,
                                options=options, content=content)
