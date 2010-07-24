# -*- coding: utf-8 -*-
"""
    sphinxcontrib.cheeseshop
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2010 by Richard Jones, Georg Brandl.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes, utils
from docutils.parsers.rst import directives

from sphinx.util.compat import Directive


RELEASE_INFO = '''\
<div class="release_info">%(prefix)s:
  <a href="http://pypi.python.org/pypi/%(dist)s">latest</a></div>
'''
RELEASE_SCRIPT = '''\
<script type="text/javascript">
  $(function() {
    $('.release_info').each(
    function() {
      var href, self = this;
      href = $('a', this).attr('href');
      $.getJSON(href + '/json?callback=?',
        function(data) {
          $('a', self).remove();
          var ul = $('<ul>').appendTo(self);
          $u.each(data.urls, function(url) {
            $('<li>').append(
              $('<a>').attr('href', url.url).text(url.filename)
            ).appendTo(ul);
          });
      });
    });
  });
</script>
'''

class CheeseShop(Directive):
    """Directive for embedding "latest release" info."""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'prefix': directives.unchanged
    }

    def run(self):
        env = self.state.document.settings.env
        ret = []
        if not env.temp_data.get('cheeseshop_script_written'):
            env.temp_data['cheeseshop_script_written'] = True
            ret.append(nodes.raw(RELEASE_SCRIPT, RELEASE_SCRIPT, format='html'))
        dist = self.arguments[0]
        html = RELEASE_INFO % {'dist': dist,
                               'prefix': self.options.get('prefix') or 'Download'}
        ret.append(nodes.raw(html, html, format='html'))
        return ret


def pypi_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for linking to PyPI packages."""
    dist = utils.unescape(text)
    env = inliner.document.settings.env
    url = env.config.cheeseshop_url + '/' + dist
    ref = nodes.reference(rawtext, text, refuri=url)
    return [ref], []


def setup(app):
    app.add_directive('pypi-release', CheeseShop)
    app.add_role('pypi', pypi_role)
    app.add_config_value('cheeseshop_url',
                         'http://pypi.python.org/pypi', 'html')
