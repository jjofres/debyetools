"""The examples in README.md and docs/index.rst run against the current code and print what the docs show."""
import doctest
import io
import re
import contextlib
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize('page', ['docs/index.rst', 'docs/source/api/nDeb.rst', 'docs/source/api/fsdb.rst',
                                  'docs/source/api/pairanalysis.rst'])
def test_rst_examples(page):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        result = doctest.testfile(str(ROOT / page), module_relative=False,
                                  optionflags=doctest.NORMALIZE_WHITESPACE, verbose=False)
    assert result.attempted > 3
    assert result.failed == 0


def test_readme_example():
    text = (ROOT / 'README.md').read_text(encoding='utf-8').replace('\r\n', '\n')
    code = re.search(r'```Python\n(.*?)```', text, re.S).group(1)
    out = io.StringIO()
    with warnings.catch_warnings(), contextlib.redirect_stdout(out):
        warnings.simplefilter('ignore')
        exec(compile(code, 'README.md', 'exec'), {})
    assert 'Cp(298.15 K) = 24.22 J/mol-at/K' in out.getvalue()
