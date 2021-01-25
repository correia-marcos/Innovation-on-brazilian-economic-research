"""" 
Script create for introduce a better id term in each paper of the base.

We realize that paper ids were not that good. It doesn't expose from which
year a given paper was, permiting different paper having the same id.

In the next steps, having a Id that differenciate the year of the papers will
be necessary, since the final database would agg all papers together.
Also, and very important, ".doc" extesion don't have good modules to extract
their content, so we also changed de extension as well.
"""

import os


def mysplit(s) -> str:
    """Split specific strings."""
    head = s.rstrip('0123456789')
    tail = s[len(head):]
    return head, tail


for i in reversed(range(2013, 2020)):
    # Change the below os.chdir to catch the correct directory tree
    os.chdir(f'C:/Users/Usuário/Projects/monografia/dados/files/docs_{i}')
    for f in os.listdir():
        file_name, file_ext = os.path.splitext(f)
        print(file_name, file_ext)
        if file_ext == '.doc':
            file_ext = '.docx'
        doc, number = mysplit(file_name)
        doc = doc[:3]
        number = number.zfill(3)
        new_name = '{}{}_{}{}'.format(doc, number, 2019, file_ext)
        os.chdir(f'C:/Users/Usuário/Projects/monografia/dados/files/docs_{i}')
        os.rename(f, new_name)
        os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\dados\\files')
