#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

class youtube(nodes.General, nodes.Element): pass

def visit_youtube_node(self, node):
    attrs = {
        "src": "http://www.youtube.com/embed/%s" % node["id"],
        "width": str(node["width"]),
        "height": str(node["height"]),
        "frameborder": "0",
    }
    self.body.append(self.starttag(node, "iframe", **attrs))
    self.body.append("</iframe>")

def depart_youtube_node(self, node):
    pass

class YouTube(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "width": directives.unchanged,
        "height": directives.unchanged,
    }

    def run(self):
        width = int(self.options.get("width", 560))
        height = int(self.options.get("height", 345))
        return [youtube(id=self.arguments[0], width=width, height=height)]

def setup(app):
    app.add_node(youtube, html=(visit_youtube_node, depart_youtube_node))
    app.add_directive("youtube", YouTube)
