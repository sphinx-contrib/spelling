from sphinx.domains import Domain

from . import directive


class SpellingDomain(Domain):

    name = 'spelling'
    label = 'Spelling Checker'
    directives = {
        'word-list': directive.SpellingDirective,
    }

    def get_objects(self):
        return []

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        return None

    def resolve_any_xref(self, env, fromdocname, builder, target, node,
                         contnode):
        return []

    def merge_domaindata(self, docnames, otherdata):
        pass
