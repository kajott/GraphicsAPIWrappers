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
    def __init__(self, html):
        self.html = html
        self.number = 0

class MatrixItem:
    def __init__(self, cols, rows, name, url, notes):
        if isinstance(cols, MatrixCategory): cols = [cols]
        if isinstance(rows, MatrixCategory): rows = [rows]
        self.cells = { (col.order, row.order) for col in cols for row in rows }
        self.name  = name
        self.url   = url
        self.notes = notes

class Matrix:
    def __init__(self, obj_id=None):
        self.obj_id = obj_id
        self.categories = []
        self.notes = []
        self.items = []
        self.title = None
        self.coltitle = None
        self.rowtitle = None

    def add_category(self, html):
        cat = MatrixCategory(html, len(self.categories))
        self.categories.append(cat)
        return cat

    def add_footnote(self, html):
        note = MatrixFootnote(html)
        self.notes.append(note)
        return note

    def add_item(self, cols, rows, name, *url_and_footnotes):
        url = [obj for obj in url_and_footnotes if not isinstance(obj, MatrixFootnote)]
        if len(url) > 1: raise ValueError("multiple URLs specified for a matrix item")
        if url: url = url.pop()
        if url and not(isinstance(url, str)): raise TypeError("URL must be a string")
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
        spandecl = ""
        if self.coltitle: spandecl += ' rowspan="2"'
        if self.rowtitle: spandecl += ' colspan="2"'
        yield f'<table id="{self.obj_id}" class="matrix"><tr><td class="nocell"{spandecl}></td>'
        if self.coltitle:
            yield f'<th class="coltitle" colspan="{len(cols)}">{self.coltitle}</th>'
            yield f'</tr><tr>'
        for i, col in enumerate(self.categories):
            if i in cols:
                yield f'<th>{col.html}</th>'
        yield '</tr>'

        # produce cells (and assign footnote indexes as we go)
        note_count = 0
        first_row = True
        for j, row in enumerate(self.categories):
            if not(j in rows): continue
            yield f'<tr>'
            if first_row and self.rowtitle:
                yield f'<th class="rowtitle" rowspan="{len(rows)}"><div>{self.rowtitle}</div></th>'
            yield f'<th>{row.html}</th>'
            for i, col in enumerate(self.categories):
                if not(i in cols): continue
                first_line = True
                prefix = '<td>'
                for item in self.items:
                    if not((i,j) in item.cells): continue
                    line = ('<td>' if first_line else '') + '<div>'
                    if item.url: line += f'<a href="{item.url}" target="_blank">'
                    line += item.name
                    if item.url: line += f'</a>'
                    for note in item.notes:
                        if not note.number:
                            note_count += 1
                            note.number = note_count
                        line += f'<sup><a href="#{self.obj_id}-note-{note.number}">{note.number}</a></sup>'
                    yield line + '</div>'
                    first_line = False
                yield ('<td class="empty">&mdash;</td>' if first_line else '</td>')
            yield '</tr>'
            first_row = False

        # produce footer
        yield '</table>'
        if any(note.number for note in self.notes):
            yield '<ol id="{self.obj_id}-notes" class="footnotes">'
            for note in sorted(self.notes, key=lambda n: n.number):
                if not note.number: continue
                yield f'<li id="{self.obj_id}-note-{note.number}" value="{note.number}">{note.html}</li>'
            yield '</ol>'
        # TODO: handle footnotes (not yet done, because there aren't any)

################################################################################

if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))

    with open("template.html", 'r', encoding='utf-8') as f:
        html = f.read()

    def replace_object(m):
        obj_id = m.group(2)
        obj = globals()[m.group(1).capitalize()](obj_id)
        getattr(data, obj_id)(obj)
        return '\n'.join(obj.to_html())
    html = re.sub(r'<(matrix) id="([^"]+)">', replace_object, html)

    with open("index.html", 'w', encoding='utf-8') as f:
        f.write(html)
