#!/usr/bin/env python3
import sys
import os
import re

import data

################################################################################

class Matrix:
    def html(self):
        pass

################################################################################

if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))

    with open("template.html", 'r', encoding='utf-8') as f:
        html = f.read()

    def replace_object(m):
        obj = globals()[m.group(1).capitalize()]()
        getattr(data, m.group(2))(obj)
        return obj.html()
    html = re.sub(r'<(matrix) id="([^"]+)">', replace_object, html)

    with open("index.html", 'w', encoding='utf-8') as f:
        f.write(html)
