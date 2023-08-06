# Python PDF Generator

![https://pypi.org/project/pdfpug/](https://img.shields.io/pypi/v/pdfpug.svg)
![https://pdfpug.readthedocs.io/en/latest/?badge=latest](https://readthedocs.org/projects/pdfpug/badge/?version=latest)

**PdfPug** is a tool that makes it easy to create beautiful PDF files from scratch.
It provides simple and easy to use APIs that allow for quick creation of PDF files.
PdfPug consists of small building blocks/components like Table, List, Header etc.
and the ability to customise these components to suit different use cases.

**Note: PdfPug is a very new package whose APIs are not stable. It can be considered
to be in pre-alpha development stage! Keep an eye out for updates.**

Here is an example,

``` {.sourceCode .python}
>>> from pdfpug import Header, Paragraph, PdfReport
>>> intro_header = Header('Introduction to PdfPug')
>>> para = Paragraph(
...     "Lorem Ipsum is <b>simply</b> <u>dummy</u> text of the printing and typesetting "
...     "industry. Lorem Ipsum has been the industry's standard dummy text "
...     "ever since the 1500s, when an unknown printer took a galley of type"
...     " and scrambled it to make a type specimen book. It has survived not "
...     "only five centuries, but also the leap into electronic typesetting, "
...     "remaining essentially unchanged. It was popularised in the 1960s with "
...     "the release of Letraset sheets containing Lorem Ipsum passages, and "
...     "more recently with desktop publishing software like Aldus PageMaker "
...     "including versions of Lorem Ipsum."
... )
>>> report = PdfReport()
>>> report.add_element(intro_header)
>>> report.add_element(para)
>>> report.generate_pdf('pdfpug-report.pdf')
```

## Installation

PdfPug is published on [PyPi](https://pypi.org/project/pdfpug/) and can be installed
from there:

``` {.sourceCode .bash}
$ pip install pdfpug
```

## Documentation

Documentation is available from <https://pdfpug.readthedocs.io/en/latest/>
