import untangle
import time

url_query_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
url_query_pubmed = url_query_base + '?db=pubmed&term={}&mindate={}&maxdate={}&retstart={}&retmax={}'

url_fetch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
url_fetch_abstract = url_fetch_base + '?db=pubmed&id={}&retmode=xml'

query_step_size = 100
query_term = 'nature[journal]'
min_date = '2015/01/01'
max_date = '2015/12/31'

start_ind = 1
article_id_all = ''
url_query_subset = url_query_pubmed.format(query_term, min_date, max_date, start_ind, query_step_size)

abstracts = []
rec_count = 1000  # initial record count, any number larger than start_ind is ok.
while start_ind <= rec_count:
    print 'processing {}...'.format(start_ind)

    # query pubmed for article id's
    time.sleep(0.34)
    url_query_subset = url_query_pubmed.format(query_term, min_date, max_date, start_ind, query_step_size)
    xml_result = untangle.parse(url_query_subset)
    rec_count = int(xml_result.eSearchResult.Count.cdata)
    start_ind = start_ind + query_step_size
    
    # extract article id's from query result
    article_id = ','.join([x.cdata for x in xml_result.eSearchResult.IdList.Id])
    article_id_all = article_id_all + article_id
    
    # query pubmed for abstracts using article id's
    abstract_xml = untangle.parse(url_fetch_abstract.format(article_id))
    
    # Get abstract for each paper
    count_abstract = len(abstract_xml.PubmedArticleSet.PubmedArticle)
    for i in range(0, count_abstract):
        # if abstract exists, add to the abstract list
        elements = [x._name for x in abstract_xml.PubmedArticleSet.PubmedArticle[i].MedlineCitation.Article.children]
        if 'Abstract' in elements:
            abstract_string = abstract_xml.PubmedArticleSet.PubmedArticle[i].MedlineCitation.Article.Abstract.AbstractText.cdata
            abstracts.append(abstract_string)
    print 'Current number of abstracts: ' + str(len(abstracts))



