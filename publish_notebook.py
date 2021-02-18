
#!/usr/bin/env python

from pathlib import Path
import re
import fire
import json

MAGIC_WORD = '# REPLACE '


def publish_notebook(old_path, new_path):
    """ Set all markdown cells to not editable or deletable.
    Removes solutions from code cells.
    Adds a table of content.
    """

    old_path = Path(old_path)
    new_path = Path(new_path)

    assert old_path.is_file(), f'{old_path} is not a file.'
    assert not new_path.is_file(), f'{new_path} already exists.'

    toc = TOC()

    with old_path.open() as old:
        data = json.load(old)

        # The first cell should not be in TOC
        cell0 = data['cells'][0]
        if cell0['cell_type'] == 'markdown':
            cell0['metadata']['editable'] = False
            cell0['metadata']['deletable'] = False

        for cell in data['cells'][1:]:
            # Markdown cells
            if cell['cell_type'] == 'markdown':
                cell['metadata']['editable'] = False
                cell['metadata']['deletable'] = False
                toc.next_cell(cell)
            
            # Code cells
            if cell['cell_type'] == 'code':
                replace(cell)

    # Insert TOC after first cell.
    data['cells'].insert(1, toc.get_cell())

    # Update notebook metadata (kernel)
    kernel = data['metadata']['kernelspec']
    kernel['display_name'] = "Python 3"
    kernel['language'] = "python"
    kernel['name'] = "python3"

    with new_path.open('w') as new:
        json.dump(data, new)


class TOC():
    """
    Create a table of content. Uses 2 levels of headings.
    """

    def __init__(self):

        self.current = 1
        self.count1 = 0
        self.count2 = 0
        self.source = ['# Table of content\n']

    def next_cell(self, cell):
        line = cell['source'][0]
        nr = len(re.search('(#*)', line).group(0))

        if nr == 1:
            self.count1 += 1
            self.count2 = 0
            new_heading = '* ### [%d. %s](#sec%d)\n' % \
                (self.count1, line[2:], self.count1)
            self.source.append(new_heading)

            cell['source'][0] = '# %d. %s <a id="sec%d">' % \
                (self.count1, line[2:], self.count1)

        if nr == 2:
            self.count2 +=1
            new_heading = ' * #### [%d.%d %s](#sec%d_%d)\n' % \
                (self.count1, self.count2, line[3:], self.count1, self.count2)
            self.source.append(new_heading)

            cell['source'][0] = '## %d.%d %s <a id="sec%d_%d">' %  \
                (self.count1, self.count2, line[3:], self.count1, self.count2)

    def get_cell(self):
        cell = {}
        cell['cell_type'] = 'markdown'
        cell['metadata'] = {}
        cell['metadata']['editable'] = False
        cell['metadata']['deletable'] = False
        cell['source'] = self.source

        return cell


def replace(cell):
    # Goes through each line of cell
    # and replaces everything before MAGIC_WORD
    # with whatever comes after MAGIC_WORD
    for i in range(len(cell['source'])):
        line = cell['source'][i]
        if MAGIC_WORD in line:
            solution, template = line.split(MAGIC_WORD)
            whitespace = re.search('( *)', line).group(0)
            cell['source'][i] = whitespace + template


if __name__ == '__main__':
    fire.Fire(publish_notebook)
