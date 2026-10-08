"""The GUI modules (debyetools.tpropsgui) must parse on every supported Python (3.10-3.12): a plain ast.parse on the
running interpreter, plus a token check for f-strings that reuse their own quotes inside a replacement field, which
only Python >= 3.12 accepts (GUI review G3). No Qt needed.
"""
import ast
import sys
import tokenize
from pathlib import Path

GUI = Path(__file__).resolve().parent.parent / 'debyetools' / 'tpropsgui'


def _pep701_only(path):
    """f-strings that reuse their own quote inside a replacement field (valid only from Python 3.12, G3)."""
    bad = []
    if sys.version_info < (3, 12):
        return bad  # ast.parse below already rejects them
    stack = []
    with open(path, 'rb') as f:
        for tok in tokenize.tokenize(f.readline):
            if tok.type == tokenize.FSTRING_START:
                q = tok.string.lstrip('rRbBfFuU')[:3]
                q = q if q in ('"""', "'''") else q[0]
                if stack and stack[-1] == q:
                    bad.append(tok.start[0])
                stack.append(q)
            elif tok.type == tokenize.FSTRING_END:
                stack.pop()
            elif tok.type == tokenize.STRING and stack:
                s = tok.string.lstrip('rRbBuU')
                if s.startswith(stack[-1]):
                    bad.append(tok.start[0])
    return bad


def test_gui_modules_parse_on_python310():
    problems = {}
    for path in sorted(GUI.rglob('*.py')):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        lines = _pep701_only(path)
        if lines:
            problems[path.name] = lines
    assert not problems, 'f-strings that need Python >= 3.12: %s' % problems
