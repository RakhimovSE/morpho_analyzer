# -*- coding: utf-8 -*-
"""
:mod:`morpho_analyzer.opencorpora_dict.parse` is a
module for OpenCorpora XML dictionaries parsing.
"""
from __future__ import absolute_import, unicode_literals, division

import logging
import collections

logger = logging.getLogger(__name__)

ParsedDictionary = collections.namedtuple('ParsedDictionary', 'lexemes links grammemes version revision')

def parse_opencorpora_xml(filename):
    """
    Parse OpenCorpora dict XML and return a ``ParsedDictionary`` namedtuple.
    """
    from lxml import etree

    links = []
    lexemes = {}
    grammemes = []
    version, revision = None, None

    def _clear(elem):
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    for ev, elem in etree.iterparse(filename):

        if elem.tag == 'grammeme':
            name = elem.find('name').text
            parent = elem.get('parent')
            alias = elem.find('alias').text
            description = elem.find('description').text

            grameme = (name, parent, alias, description)
            grammemes.append(grameme)
            _clear(elem)

        if elem.tag == 'dictionary':
            version = elem.get('version')
            revision = elem.get('revision')
            _clear(elem)

        if elem.tag == 'lemma':
            if not lexemes:
                logger.info('parsing xml:lemmas...')

            lex_id, word_forms = _word_forms_from_xml_elem(elem)
            lexemes[lex_id] = word_forms
            _clear(elem)

        elif elem.tag == 'link':
            if not links:
                logger.info('parsing xml:links...')

            link_tuple = (
                elem.get('from'),
                elem.get('to'),
                elem.get('type'),
            )
            links.append(link_tuple)
            _clear(elem)

    return ParsedDictionary(lexemes, links, grammemes, version, revision)


def _word_forms_from_xml_elem(elem):
    """
    Return a list of (word, tags) pairs given "lemma" XML element.
    """
    def _tags(elem):
        return ",".join(g.get('v') for g in elem.findall('g'))

    lexeme = []
    lex_id = elem.get('id')

    if len(elem) == 0:  # deleted lexeme?
        return lex_id, lexeme

    base_info = elem.findall('l')

    assert len(base_info) == 1
    base_tags = _tags(base_info[0])

    for form_elem in elem.findall('f'):
        tags = _tags(form_elem)
        form = form_elem.get('t').lower()
        lexeme.append(
            (form, " ".join([base_tags, tags]).strip())
        )

    return lex_id, lexeme
