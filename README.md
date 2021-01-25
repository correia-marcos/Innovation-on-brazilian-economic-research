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

Três papers could not be downloaded do to problems in the [ANPEC website](https://en.anpec.org.br/previous-editions.php): 
doc201_2015 - Is tracking beneficial? Study of tracking using peer effects  (2016); 
doc235_2015 - THE INS AND OUTS OF UNEMPLOYMENT IN A DUAL LABOR MARKET;
doc128_2013 - EFEITOS DO INVESTIMENTO EM CAPITAL INTANGÍVEL E PATENTES NO VALOR DAS EMPRESAS BRASILEIRAS

## Summary

Briefly, we did the following:
* Part 1 - Scraping of htmls and important information (area of submission, coautors and universities)
* Part 2 - Download of files
* Part 3 - Convertion of files (pdf to txt; doc and docx to txt)
* Part 4 - pré-processing
* Part 4 - Stopwords (en, pt)
* Part 5 - stemming / Lemmatizing
* Part 5 - Topic Modelling: tf-idf
* Part 5 - latent dirichlet allocation (LDA)
* Part 5 - ressonance/novelty/transience calculations (formula based on Kullback-leiber divergence)


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

**Important:** some of this libraries need to be downloaded (pip install or
conda install).

**Important²:** those libraries cited as (cloned), in a perfect world, would be a submodule of the project. Do to the lack of knowlegde by the time this project was written, we just cloneded. In future projects, this problem is gonna be solved, but it will be a normal folder in this one.