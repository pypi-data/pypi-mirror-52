.. -*- coding: utf-8 -*-

Changes
-------

0.21 (2019-09-20)
~~~~~~~~~~~~~~~~~

- Explain assertion errors, to avoid meaningless logging messages

- Suppress warning on ignored ``<pre>`` tags


0.20 (2019-09-02)
~~~~~~~~~~~~~~~~~

- Ignore ``code-block`` attributes


0.19 (2019-07-16)
~~~~~~~~~~~~~~~~~

- Workaround a degenerated case involving empty hrefs


0.18 (2019-07-12)
~~~~~~~~~~~~~~~~~

- Completely ignore ``<iframe>`` and ``<script>`` tags

- Extract <table> content as plain paragraph, to make them at least readable


0.17 (2019-07-03)
~~~~~~~~~~~~~~~~~

- Ignore text attributes that we are not going to handle


0.16 (2019-06-25)
~~~~~~~~~~~~~~~~~

- Handle HTML created with non-Unix end-of-line convention


0.15 (2018-08-23)
~~~~~~~~~~~~~~~~~

- Ignore ``<style>`` tags and degenerated ``<a>`` tags


0.14 (2018-08-23)
~~~~~~~~~~~~~~~~~

- Ignore ``<img>`` tags, out of scope at least for now


0.13 (2018-08-23)
~~~~~~~~~~~~~~~~~

- Rewritten HTML parser, slightly more robust and versatile


0.12 (2018-08-17)
~~~~~~~~~~~~~~~~~

- Try harder to handle degenerated paragraphs represented with DIVs

- Replace asserts with a custom exception to signal parsing errors


0.11 (2018-08-15)
~~~~~~~~~~~~~~~~~

- Handle degenerated paragraphs represented with DIVs

- Add an option to swallow HTML parsing exceptions and falling back to plain text


0.10 (2018-08-01)
~~~~~~~~~~~~~~~~~

- Handle SPANs inside headings


0.9 (2018-07-12)
~~~~~~~~~~~~~~~~

- Ignore standalone BRs in the HTML parser


0.8 (2018-07-12)
~~~~~~~~~~~~~~~~

- Ignore BRs inside headings in the HTML parser


0.7 (2018-06-26)
~~~~~~~~~~~~~~~~

- Better handling of nested DIVs in the HTML parser


0.6 (2018-06-13)
~~~~~~~~~~~~~~~~

- Handle implicit list item indexes in SEMPrinter


0.5 (2018-04-26)
~~~~~~~~~~~~~~~~

- Properly escape also the link's address


0.4 (2018-04-26)
~~~~~~~~~~~~~~~~

- New ``escape`` option to ``HTMLPrinter`` that by default uses `html.escape(text,
  quote=True)`__ to emit safe text spans

  __ https://docs.python.org/3/library/html.html#html.escape


0.3 (2018-04-20)
~~~~~~~~~~~~~~~~

- Support for hyperlinks

- Support for headings

- New function to emit a Quill Delta representation of an AST


0.2 (2018-03-10)
~~~~~~~~~~~~~~~~

- Fix HTML representation of numbered list items without a value

- Raise a specific InvalidNestingError exception instead of generic AssertionError


0.1 (2018-02-25)
~~~~~~~~~~~~~~~~

- Renamed to metapensiero.markup.semtext


0.0 (unreleased)
~~~~~~~~~~~~~~~~

- Initial effort.
