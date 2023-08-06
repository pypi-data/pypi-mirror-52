"""
    sphinxcontrib.commonmark
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017-2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import Any, Dict, List

import pycmark
from docutils import nodes
from docutils.transforms import Transform
from pycmark import addnodes
from pycmark.transforms import LinebreakFilter, TightListsCompactor, TightListsDetector
from sphinx.application import Sphinx
from sphinx.transforms import SphinxTransform

from sphinxcontrib.commonmark.version import __version__


class CommonMarkParser(pycmark.CommonMarkParser):
    def get_transforms(self) -> List[Transform]:
        transforms = super().get_transforms()
        transforms.remove(LinebreakFilter)
        transforms.remove(TightListsCompactor)
        transforms.remove(TightListsDetector)
        return transforms


def html_visit_linebreak(self, node) -> None:
    self.body.append('<br />\n')
    raise nodes.SkipNode


def latex_visit_linebreak(self, node) -> None:
    self.body.append('\\linebreak\n')
    raise nodes.SkipNode


class SphinxLinebreakFilter(SphinxTransform):
    default_priority = 500

    def apply(self) -> None:
        if self.app.builder.format in ('html', 'latex'):
            return

        for node in self.document.traverse(addnodes.linebreak):
            node.replace_self(nodes.Text('\n'))


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_node(addnodes.linebreak,
                 html=(html_visit_linebreak, None),
                 latex=(latex_visit_linebreak, None))
    app.add_post_transform(SphinxLinebreakFilter)
    app.add_source_suffix('.md', 'markdown')
    app.add_source_parser(CommonMarkParser)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
