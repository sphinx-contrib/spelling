# -*- coding: utf-8 -*-
import os
import shutil

def on_html_collect_pages(app):
    for f in app.builder.config.rawfiles:
        src = os.path.join(app.srcdir, f)
        dst = os.path.join(app.builder.outdir, f)
        # cleanup
        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            elif os.path.isfile(dst):
                os.remove(dst)
        # copy file
        if os.path.exists(src):
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            elif os.path.isfile(src):
                shutil.copy(src, dst)
            else:
                msg = ('rawfiles target is not directory or file "%s".' % src)
                app.builder.warn(msg)
        else:
            msg = ('rawfiles can not find "%s".' % src)
            app.builder.warn(msg)

    return ()

def setup(app):
    app.add_config_value('rawfiles', [], 'html')
    app.connect("html-collect-pages", on_html_collect_pages)
