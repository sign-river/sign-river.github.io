# -*- coding: utf-8 -*-
import re
path = r'content/post/tutorial/network/stellaris-lan-setup/centos/index.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()
def repl(m):
    src = m.group(1)
    alt = m.group(2) or 'image'
    return '<a href="%s" target="_blank"> <img src="%s" alt="%s" style="max-width: 100%%; width: 1000px;"/> </a>' % (src, src, alt)
new_text = re.sub(r'<img\s+src="(images/[^"]+)"\s+alt="([^"]*)"\s+width="\d+"\s*/?>', repl, text)
with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_text)
print('Done.')
