#!/usr/bin/env python3
import sys
import os
import re

import data

################################################################################

class MatrixCategory:
    def __init__(self, html, order=0):
        self.html = html
        self.order = order

class MatrixFootnote:
    def __init__(self, html, number=0):
        self.html = html
        self.number = number

class MatrixItem:
    def __init__(self, cols, rows, name, url, notes):
        if isinstance(cols, MatrixCategory): cols = [cols]
        if isinstance(rows, MatrixCategory): rows = [rows]
        self.cells = { (col.order, row.order) for col in cols for row in rows }
        self.name  = name
        self.url   = url
        self.notes = notes

class Matrix:
    def __init__(self):
        self.categories = []
        self.footnotes = []
        self.items = []
        self.title = None

    def add_category(self, html):
        cat = MatrixCategory(html, len(self.categories))
        self.categories.append(cat)
        return cat

    def add_footnote(self, html):
        note = MatrixFootnote(html, len(self.footnotes) + 1)
        self.footnotes.append(note)
        return note

    def add_item(self, cols, rows, name, *url_and_footnotes):
        url = [obj for obj in url_and_footnotes if not isinstance(obj, MatrixFootnote)]
        if len(url) > 1: raise ValueError("multiple URLs specified for a matrix item")
        url = url.pop()
        if not isinstance(url, str): raise TypeError("URL must be a string")
        notes = [obj for obj in url_and_footnotes if isinstance(obj, MatrixFootnote)]
        item = MatrixItem(cols, rows, name, url, notes)
        self.items.append(item)
        return item

    def to_html(self):
        # survey all used cells
        cells = set()
        for item in self.items:
            cells |= item.cells
        cols = { col for (col, row) in cells }
        rows = { row for (col, row) in cells }

        # produce header
        if self.title: yield f'<h2>{self.title}</h2>'
        yield '<table class="matrix"><tr><td></td>'
        for i, col in enumerate(self.categories):
            if i in cols:
                yield f'<th>{col.html}</th>'
        yield '</tr>'

        # produce cells
        for j, row in enumerate(self.categories):
            if not(j in rows): continue
            yield f'<tr><th>{row.html}</th>'
            for i, col in enumerate(self.categories):
                if not(i in cols): continue
                first = True
                prefix = '<td>'
                for item in self.items:
                    if not((i,j) in item.cells): continue
                    line = '<td>' if first else '<br>'
                    if item.url: line += f'<a href="{item.url}" target="_blank">'
                    line += item.name
                    if item.url: line += f'</a>'
                    yield line
                    first = False
                yield ('<td class="empty">&mdash;</td>' if first else '</td>')
            yield '</tr>'

        # produce footer
        yield '</table>'

################################################################################

if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))

    with open("template.html", 'r', encoding='utf-8') as f:
        html = f.read()

    def replace_object(m):
        obj = globals()[m.group(1).capitalize()]()
        getattr(data, m.group(2))(obj)
        return '\n'.join(obj.to_html())
    html = re.sub(r'<(matrix) id="([^"]+)">', replace_object, html)

    with open("index.html", 'w', encoding='utf-8') as f:
        f.write(html)
