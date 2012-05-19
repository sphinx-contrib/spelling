def setup(app):
    app.add_config_value('coffee_src_dir', None, 'env')
    app.add_config_value('coffee_src_parser', None, 'env')
    from .domain import CoffeeDomain
    app.add_domain(CoffeeDomain)
    from . import documenters as doc
    app.add_autodocumenter(doc.ModuleDocumenter)
    app.add_autodocumenter(doc.ClassDocumenter)
    app.add_autodocumenter(doc.FunctionDocumenter)
    app.add_autodocumenter(doc.MethodDocumenter)
    app.add_autodocumenter(doc.StaticMethodDocumenter)
