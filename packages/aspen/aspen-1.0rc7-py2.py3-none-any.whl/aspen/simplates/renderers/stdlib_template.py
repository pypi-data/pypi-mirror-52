from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from . import Renderer, Factory
from string import Template


class Renderer(Renderer):

    def compile(self, filepath, padded):
        return Template(padded)

    def render_content(self, context):
        return self.compiled.substitute(context)


class Factory(Factory):
    Renderer = Renderer
