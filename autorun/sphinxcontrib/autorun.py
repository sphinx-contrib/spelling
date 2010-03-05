# -*- coding: utf-8 -*-
"""
sphinxcontirb.autorun
~~~~~~~~~~~~~~~~~~~~~~

Run the code and insert stdout after the code block.


"""
from subprocess import Popen,PIPE

from docutils import nodes
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives
from sphinx.errors import SphinxError


class RunBlockError(SphinxError):
    category = 'runblock error'

class AutoRun(object):
    config = dict(
        pycon = 'python -',
        pycon_prefix_chars = 4,
        console = 'bash',
        console_prefix_chars = 1 ,
    )
    @classmethod
    def builder_init(cls,app):
        cls.config.update(app.builder.config.autorun_languages)


    
class RunBlock(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'linenos': directives.flag,
    }


    def run(self):
        config = AutoRun.config
        language = self.arguments[0]

        if language not in config:
            raise RunBlockError('Unknown language %s' % language)


        
        # Get configuration values for the language
        args = config[language].split()
        input_encoding = config.get(language+'_input_encoding','ascii')
        output_encoding = config.get(language+'_output_encoding','ascii')
        prefix_chars = config.get(language+'_prefix_chars',0)
        
        # Build the code text
        codelines = (line[prefix_chars:] for line in self.content)
        code = u'\n'.join(codelines).encode(input_encoding)
        
        # Run the code
        proc = Popen(args,stdin=PIPE,stdout=PIPE,stderr=PIPE)
        stdout,stderr = proc.communicate(code)

        # Process output 
        if stdout:
            out = ''.join(stdout).decode(output_encoding)
        else:
            out = ''.join(stderr).decode(output_encoding)
        
        # Get the original code with prefixes
        code = u'\n'.join(self.content)
        code_out = u'\n'.join((code,out))
        literal = nodes.literal_block(code_out,code_out)
        literal['language'] = language
        literal['linenos'] = 'linenos' in self.options
        return [literal]



def setup(app):
    app.add_directive('runblock', RunBlock)
    app.connect('builder-inited',AutoRun.builder_init)
    app.add_config_value('autorun_languages', AutoRun.config, 'env')

# vim: set expandtab shiftwidth=4 softtabstop=4 :
