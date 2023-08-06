#!/usr/bin/python3
# __*__ coding: utf-8 __*__

'''
@Author: simonKing
@Os：Windows 10 x64
@Software: PY PyCharm
@File: __Html2Json.py
@Time: 2019/8/23 14:42
@Desc: Html2Json
'''

from bs4 import BeautifulSoup
from .__Tag import Tag

class PageParser:
    '''
    HTML to JSON
    '''
    def __init__(self, html_string):
        self.soup = BeautifulSoup(html_string, 'html.parser')
        self.html = self.soup.find('html')
        self.all_tags = self.parse()

    def parse(self):
        '''
        Conversion process
        :return:
        '''
        results = []
        for x, tag in enumerate(self.html.descendants):
            if str(type(tag)) == "<class 'bs4.element.Tag'>":
                if tag.name == 'script':
                    continue
                # Find tags with no children (base tags)
                if tag.contents:
                    if sum(1 for _ in tag.descendants) == 1:
                        t = Tag(tag.name.lower())
                        # Because it might be None (<i class="fa fa-icon"></i>)
                        if tag.string:
                            t.add_content(tag.string)

                        if tag.attrs:
                            for a in tag.attrs:
                                t.add_attribute(a, tag[a])

                        results.append(t.get_data())
                # Self enclosed tags (hr, meta, img, etc...)
                else:
                    t = Tag(tag.name.lower())

                    if tag.attrs:
                        for a in tag.attrs:
                            t.add_attribute(a, tag[a])
                    results.append(t.get_data())
        return results