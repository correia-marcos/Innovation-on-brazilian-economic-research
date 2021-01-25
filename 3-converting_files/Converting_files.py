"""Script for coverting pdf and doc/docx files into txt.

Convertions were done from pdf to txt and docx to txt, using downloaded
 modules (pdftotext and docx).
Important: We do not recomend the use of PyPDF2 for PDFs bigger than one page.
The extraction method is still weak and no enconding could gave good results.
That is, txt generated is very messy.

UPDATE: Wih the recent updates in python, the pdftotext module turn into an
OS command. We realized this after extraction were realized, after a test of
the program. We will leave a comentary as an example of how to apply the new
pdftotext for WINDOWS.
"""
# coding=utf-8

import os
import glob
import io
import docx
import re
import sys
import pdftotext


# VERY IMPORTANT: we found (after a while) that doc235_2016 and doc128_2013
# files could not be openned! ANPEC doesn't have this papers, cause they are
# corrupted.

# Change the below "base" variable to the correct directory tree
base = r'C:/Users/Usuário/Projects/monografia/dados/files/'

aff = base + r'docs_2016\doc235_2016.pdf'
aff2 = base + r'docs_2013\doc128_2013.pdf'

sys.stdout.encoding = 'utf-8'
os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\dados\\txt_files')

# =============================================================================
#  New use of pdftotext
# =============================================================================

# file_path = r'C:\Users\Usuário\Projects\monografia\dados\files\docs_2015'
# file_path = file_path + r'\doc007_2015.pdf'

# text = os.popen(f"pdftotext -enc UTF-8 {file_path}").readlines()
# os.system("pdftotext {} {} ".format(file_path, "teste.txt"))


# =============================================================================
# pdf files part
# =============================================================================

scope = reversed(range(2013, 2020))
pdf_files = [base + rf'docs_{x}/*.pdf' for x in scope]


def convertPDFtoText(path):
    """
    Do a simple convertion of pdf into txt.

    Parameters
    ----------
    path : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    os.chdir('C:\\Users\\Usuário\\Projects\\monografia\\dados\\txt_files')
    for i in range(len(pdf_files)):
        file_pdf = glob.glob(pdf_files[i])

        for j in file_pdf:

            with open(j, 'rb') as fout:
                if j == aff or j == aff2:
                    pass
                else:
                    pdf = pdftotext.PDF(fout)
            nome = re.search(r'(doc[0-9]{3}_[0-9]{4})', j).group() + '.txt'

            with open(nome, 'w', encoding='utf-8') as f:
                for pages in pdf:
                    f.write(pages)
                f.close()

# =============================================================================
# Docx part
# =============================================================================

# Another very important thing: files previously downloaded as "doc" were
# converted in docv (in better_names.py), but this didn't change some content
# property. Briefly, the data structure  of old word documents (.doc) are
# different, and the "docx" library can't read those. We changed the .doc
# documents 'by hand', in the security advanced setting.


scope = reversed(range(2013, 2020))
doc_fils = [f'C:/Users/Usuário/Projects/monografia/dados/files/docs_{x}/*.docx'
            for x in scope]


def convertDocxtoText(path):
    """
    Do a simple convertion from docx to txt.

    Returns
    -------
    None.

    """
    for i in range(len(doc_fils)):
        file_docx = glob.glob(doc_fils[i])

        for j in file_docx:

            document = docx.Document(j)
            nome = re.search(r'(doc[0-9]{3}_[0-9]{4})', j).group() + '.txt'
            with io.open(nome, 'w', encoding='utf-8') as textfile:
                for para in document.paragraphs:
                    textfile.write(para.text)


if __name__ == '__main__':
    convertDocxtoText(doc_fils)
    convertPDFtoText(pdf_files)
