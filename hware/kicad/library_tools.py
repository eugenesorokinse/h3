"""Replace one symbol while retaining other components in the local library."""
import re
from pathlib import Path

def save_symbol(name, definition):
    path = Path('h3.kicad_sym')
    text = path.read_text()
    start = re.search(r'\(symbol\s+"'+re.escape(name)+r'"(?=\s|\))', text)
    if start:
        depth = 0
        for token in re.finditer(r'"(?:\\.|[^"\\])*"|[()]', text[start.start():]):
            if token.group() == '(': depth += 1
            elif token.group() == ')':
                depth -= 1
                if depth == 0:
                    end = start.start()+token.end()
                    text = text[:start.start()]+definition+text[end:]
                    break
        else: raise ValueError('Unbalanced symbol')
    else:
        end = text.rfind(')')
        text = text[:end]+definition+'\n'+text[end:]
    path.write_text(text)
