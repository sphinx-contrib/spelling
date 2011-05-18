# -*- coding: utf-8 -*-
"""
    sphinxcontrib.cheeseshop
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2010 by Richard Jones, Georg Brandl.
    :license: BSD, see LICENSE for details.
"""

import re

from docutils import nodes, utils
from docutils.parsers.rst import directives

from sphinx.util.nodes import split_explicit_title
from sphinx.util.compat import Directive


RELEASE_INFO = '''\
<div class="release_info %(class)s">%(prefix)s:
  <a href="http://pypi.python.org/pypi/%(dist)s">latest</a></div>
'''

RELEASE_SCRIPT = '''\
<script type="text/javascript">
  $(function() {
    $('.release_info').each(function() {
      var self = this, anchor = $('a', this);
      $.getJSON(anchor.attr('href') + '/json?callback=?', function(data) {
          anchor.remove();
        var ul = $('<ul>').appendTo(self);
        $.each(data.urls, function(url_id) {
          var url=data.urls[url_id];
          var li=$('<li>');
          li.appendTo(ul);
          var a=$('<a>').attr('href', url.url).text(url.filename);
          a.appendTo(li);
        });
      });
    });
  });
</script>
'''

class CheeseShop(Directive):
    """Directive for embedding "latest release" info in the form of a list of
    release file links.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'prefix': directives.unchanged,
        'class': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        ret = []
        if not env.temp_data.get('cheeseshop_script_written'):
            env.temp_data['cheeseshop_script_written'] = True
            ret.append(nodes.raw(RELEASE_SCRIPT, RELEASE_SCRIPT, format='html'))
        dist = self.arguments[0]
        prefix = self.options.get('prefix') or 'Download'
        class_ = self.options.get('class') or ''
        html = RELEASE_INFO % {'dist': dist, 'prefix': prefix, 'class': class_}
        ret.append(nodes.raw(html, html, format='html'))
        return ret


def pypi_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to PyPI packages."""
    env = inliner.document.settings.env
    text = utils.unescape(text)
    has_explicit, title, target = split_explicit_title(text)
    m = re.match(r'(.*)\s+\((.*?)\)', target)
    if m:
        dist, version = m.groups()
        url = env.config.cheeseshop_url + '/' + dist + '/' + version
        if not has_explicit:
            title = '%s %s' % (dist, version)
    else:
        url = env.config.cheeseshop_url + '/' + target
    ref = nodes.reference(rawtext, title, refuri=url)
    return [ref], []


def setup(app):
    app.require_sphinx('1.0')
    app.add_directive('pypi-release', CheeseShop)
    app.add_role('pypi', pypi_role)
    app.add_config_value('cheeseshop_url',
                         'http://pypi.python.org/pypi', 'html')
