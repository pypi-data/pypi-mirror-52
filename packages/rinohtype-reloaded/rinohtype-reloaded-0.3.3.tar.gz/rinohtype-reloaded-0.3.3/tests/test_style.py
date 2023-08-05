# This file is part of rinohtype, the Python document preparation system.
#
# Copyright (c) Brecht Machiels.
#
# Use of this source code is subject to the terms of the GNU Affero General
# Public License v3. See the LICENSE file or http://www.gnu.org/licenses/.


import pytest

from rinoh.dimension import PT
from rinoh.document import DocumentTree, Document, FakeContainer
from rinoh.language import EN
from rinoh.paragraph import Paragraph
from rinoh.text import StyledText, SingleStyledText
from rinoh.style import StyleSheet, StyledMatcher, Specificity


emphasis_selector = StyledText.like('emphasis')
paragraph_selector = Paragraph

matcher = StyledMatcher({
    'emphasized text': emphasis_selector,
    'paragraph': paragraph_selector,
})

ssheet1 = StyleSheet('base', matcher)
ssheet1('emphasized text', font_slant='italic')
ssheet1('paragraph', space_above=5*PT)

ssheet2 = StyleSheet('test', base=ssheet1)
ssheet2('paragraph', space_below=10*PT)

emphasized = SingleStyledText('emphasized', style='emphasis')
paragraph = Paragraph('A paragraph with ' + emphasized + ' text.')

doctree = DocumentTree([paragraph])

document = Document(doctree, ssheet2, EN)
container = FakeContainer(document)

def test_style():
    style1 = ssheet1['emphasized text']
    assert style1.font_width == 'normal'
    assert style1.font_slant == 'italic'

    style2 = ssheet1['paragraph']
    assert style2.space_above == 5*PT
    assert style2.space_below == 0

    style3 = ssheet2['paragraph']
    assert style3.space_above == 0
    assert style3.space_below == 10*PT


def test_get_selector():
    assert ssheet1.get_selector('emphasized text') == emphasis_selector
    assert ssheet1.get_selector('paragraph') == paragraph_selector


def test_get_styled():
    assert ssheet1.get_styled('emphasized text') == StyledText
    assert ssheet1.get_styled('paragraph') == Paragraph


def test_find_matches():
    match1, = ssheet1.find_matches(emphasized, None)
    assert match1.specificity == Specificity(0, 0, 1, 0, 1)
    assert match1.style_name == 'emphasized text'

    match2, = ssheet1.find_matches(paragraph, None)
    assert match2.specificity == Specificity(0, 0, 0, 0, 2)
    assert match2.style_name == 'paragraph'

    match3a, = ssheet2.find_matches(paragraph, None)
    assert match3a.specificity == Specificity(0, 0, 0, 0, 2)
    assert match3a.style_name == 'paragraph'


def test_find_style():
    assert ssheet1.find_style(emphasized, None) is ssheet1['emphasized text']
    assert ssheet1.find_style(paragraph, None) is ssheet1['paragraph']
    assert ssheet2.find_style(paragraph, None) is ssheet2['paragraph']


def test_get_style():
    assert emphasized.get_style('font_width', container) == 'normal'
    assert emphasized.get_style('font_slant', container) == 'italic'

    assert paragraph.get_style('margin_left', container) == 0
    assert paragraph.get_style('space_above', container) == 5*PT
    assert paragraph.get_style('space_below', container) == 10*PT
