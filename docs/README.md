# Building documentation

Wisualia uses [Sphinx](http://www.sphinx-doc.org/) for documentation generation.
Following Sphinx extensions are also used:
* [autodoc] and [apidoc] for API documentation generation.
* [napoleon] for readable Google style docstrings.
* [doctest] to misuse documentation tests to generate documentation images.
* [sphinx-autodoc-typehints] to find type information from function signatures.

To build documentation run: `build_docs.py` or `build_docs.py --clean`.
The resulting documentation will be in `docs/_build/` folder. For more
information run `build_docs.py -h`.

[autodoc]: http://www.sphinx-doc.org/en/stable/ext/autodoc.html#module-sphinx.ext.autodoc
[apidoc]: http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html
[napoleon]: http://www.sphinx-doc.org/en/stable/ext/napoleon.html
[doctest]: http://www.sphinx-doc.org/en/stable/ext/doctest.html
[sphinx-autodoc-typehints]: https://github.com/agronholm/sphinx-autodoc-typehints
