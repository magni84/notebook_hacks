# Publish notebook

**Usage:** python publish_notebook.py ORIGINAL NEW

It does three things:

1. Set all markup cells to non-editable and non-deletable
2. In all code-cells it change `solution_code # REPLACE published_code` to `published_code`. (The magic word is "# REPLACE ")
3. It creates a table of content. The first cell will be skipped (assuming it is the title of the notebook). 
It will then look at each markup cell. If it starts with a line "# Heading" or "## Heading"" it will be included in the TOC. Finally it inserts a new cell with the TOC right after the first cell. In the current version it is assumed that each heading-cell contain only the heading, otherwise strange line breaks may be added...(easy to fix, but I'm too lazy right now).

