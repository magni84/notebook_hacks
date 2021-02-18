# Publish notebook

**Usage:** python publish_notebook.py ORIGINAL NEW

It does three things:

1. Set all markup cells to non-editable and non-deletable
2. In all code-cells it change 
```
	solution_code # REPLACE new_code
```
to `new_code`.
3. It creates a table of content. The first cell will be skipped (assuming it is the title of the notebook). 
It will then look at each markup cell. If it starts with a line "# Heading" or "## Heading"" it will be included in the TOC. (It is assumed that the cell only contains the heading..). Finally it inserts a new cell with the TOC right after the first cell.

