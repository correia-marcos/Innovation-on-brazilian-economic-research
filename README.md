# Novelty, transience and resonance in brazilian economic research (ANPEC meeting)

This is a paper project based on Topic Modelling and Information Theory concepts
used to analyse the innovation and transience of brazilian economic research. 
We used the submitted papers in Annals Meeting of ANPEC, to understand the extent to
which patterns of papers changed in time (given that they were submitted to the same
area in ANPEC meeting). This approach produces an quantitative analysis of the
innovation, transience and resonance of a paper in a corpus of other papers.
  
## Data

We use papers submitted in the ANPEC annal Meeting from 2013 to 2019. 2013 was 
the first year that ANPEC meeting used a 13 areas definition for research
submission, what was the basis of our anaylisis. Brifly, we tried to see what
were the areas (microeconomics, macro, political economics...) that produced
more innovation.
This make 1678 papers in total, with 576 in english and 1100 in portuguese.
In this period (2013-2019) there was two papers submitted in spanish, 
but this quantity is to little for Topic Modelling applications. 

**Important:** The anpec website in 2015 did not provide the name of the authors
of the articles and the institutions where they work. This was made 'by hands'
googling the papers. 

Two papers could not be downloaded, buy the program, do to problems in the [ANPEC website](https://en.anpec.org.br/previous-editions.php): 

doc235_2016 - TRABALHO FORMAL-INFORMAL FEMININO NO BRASIL: UMA DECOMPOSIÇÃO DOS DIFERENCIAIS DE RENDIMENTOS (2000-2010);
doc128_2013 - EFEITOS DO INVESTIMENTO EM CAPITAL INTANGÍVEL E PATENTES NO VALOR DAS EMPRESAS BRASILEIRAS

They were, also, downloaded by googling the title of the paper (on other sites).


## Summary

Briefly, we did the following:
* Part 1 - Scraping of htmls and important information (area of submission, coautors and universities)
* Part 2 - Download of files
* Part 3 - Convertion of files (pdf to txt; doc and docx to txt)
* Part 4 - Pré-processing
* Part 4 - Stopwords (en, pt)
* Part 5 - Stemming / Lemmatizing
* Part 5 - Topic Modelling
* Part 5 - Latent dirichlet allocation (LDA)
* Part 5 - Ressonance/novelty/transience calculations (formula based on Kullback-leiber divergence)
* Part 6 - Further analysis with citations and other variables

## Script requirements
* requests
* bs4
* pandas
* os
* time
* glob
* io
* docx
* re
* sys
* pdfminer
* pdftotext
* lda
* logging
* gensim
* nltk
* scipy
* pickle
* wordcloud
* sklearn
* collections
* matplotlib.pyplot
* seaborn
* NTRexample_FRevNCA from github (cloned)
* artifici_lda library from github (cloned)
* polyglot library from github (cloned)
* stanza

**Important:** some of this libraries need to be downloaded (pip install or
conda install).

**Important²:** those libraries cited as (cloned), would be a submodule of the project in a perfect world. Do to the lack of knowlegde by the time this project was written, we just cloned. In future projects, such a problem won't happen, but it will be a normal folder in this one.
