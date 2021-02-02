"""Script for coverting pdf and doc/docx files into txt.

Convertions were done from pdf to txt and docx to txt, using downloaded
 modules (pdfminer and docx).

Important: pdf convertion to txt is not as simple as it's seem. We created
a new version since the former one had many errors in symbol convertion. The
results were droped in txt_filesv2

"""
# coding=utf-8

import os
import glob
import io
import docx
import re
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


# VERY IMPORTANT: we found (after a while) that doc235_2016 and doc128_2013
# files could not be openned! ANPEC doesn't have this papers, cause they are
# corrupted.


root = os.path.abspath(os.curdir)
base = rf'{root}/dados/files/'

aff = base + r'docs_2016\doc235_2016.pdf'
aff2 = base + r'docs_2013\doc128_2013.pdf'
aff3 = base + r'docs_2018\doc097_2018.pdf'  # cryptograph problem
aff4 = base + r'docs_2014\doc088_2014.pdf'  # cryptograph problem

# aff3 and aff4 files were copied from the file_txts folder.

sys.stdout.encoding = 'utf-8'
os.chdir(f'{root}/dados/txt_filesv3')
# os.chdir(f'{root}/dados/txt_filesv2')

# os.mkdir(f'{root}/dados/txt_filesv2')
# os.mkdir(f'{root}/dados/txt_filesv3')
# =============================================================================
#  pdf files part
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
    os.chdir(f'{root}\\dados\\txt_filesv3')
    txts = []
    for i in range(len(pdf_files)):
        file_pdf = glob.glob(pdf_files[i])

        for j in file_pdf:

            if j == aff or j == aff2 or j == aff3 or j == aff4:
                pass
            else:
                rsrcmgr = PDFResourceManager()
                retstr = StringIO()
                codec = 'utf-8'
                laparams = LAParams()
                device = TextConverter(rsrcmgr, retstr,
                                       codec=codec, laparams=laparams)
                fp = open(j, 'rb')
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                password = ""
                maxpages = 0
                caching = True
                pagenos = set()

                for page in PDFPage.get_pages(fp, pagenos,
                                              maxpages=maxpages,
                                              password=password,
                                              caching=caching,
                                              check_extractable=True):
                    interpreter.process_page(page)

                text = retstr.getvalue()
                txts.append(text)

                fp.close()
                device.close()
                retstr.close()

            nome = re.search(r'(doc[0-9]{3}_[0-9]{4})', j).group() + '.txt'

            with open(nome, 'w', encoding='utf-8') as f:
                f.write(text)
                f.close()

    os.chdir(root)
    return txts


# =============================================================================
# PDF that were corrupted in ANPEC html
# =============================================================================


def corrupted_pdf(papers):
    """
    Do a simple convertion of pdf into txt.

    Parameters
    ----------
    papers : List with corrupted papers (directory tree)
        DESCRIPTION.

    Returns
    -------
    None.

    """
    os.chdir(f'{root}/dados/txt_filesv3')
    for paper in papers:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr,
                               codec=codec, laparams=laparams)
        fp = open(paper, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()

        nome = re.search(r'(doc[0-9]{3}_[0-9]{4})', paper).group() + '.txt'

        with open(nome, 'w', encoding='utf-8') as f:
            f.write(text)
            f.close()

    os.chdir(root)


# =============================================================================
# Docx part
# =============================================================================

# Another very important thing: files previously downloaded as "doc" were
# converted in docv (in better_names.py), but this didn't change some content
# property. Briefly, the data structure  of old word documents (.doc) is
# different, and the "docx" library can't read those. We changed the .doc
# documents 'by hand', in the security advanced setting.


scope = reversed(range(2013, 2020))
doc_fils = [f'{root}/dados/files/docs_{x}/*.docx' for x in scope]


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
    os.chdir(root)

# =============================================================================
# Applying functions
# =============================================================================

# IMPORTANT: We noticed that our algorithmum still produces the files of
# aff1, aff2, aff3 e aff4. Since aff3 and aff4 were problems related to
# cryptography that the better library can't handle, we just copied those two
# files from "txt_files" folder. The other ones (aff1, aff2) have to be
# removed from the folder (the ANPEC html doesn't have them).


if __name__ == '__main__':
    convertDocxtoText(doc_fils)
    convertPDFtoText(pdf_files)
    papers = [aff, aff2]
    corrupted_pdf(papers)
