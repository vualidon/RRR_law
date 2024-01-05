import os
import requests
from time import time
import multiprocessing
from dotenv import load_dotenv
load_dotenv()

# from utils._openai import generate_answer, rewrite
from generate import rewrite, generate_answer
from rank_bm25 import BM25Okapi
from trafilatura import fetch_url, extract
from newspaper import Article


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')




def google_search(query, start, num):
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx=84c7128382fe8459c&q={query}&safe=active&start={start}&num={num}"
    response = requests.get(url)
    return response.json()

def rrr_snippets(query):
    """
    use google search to retrieve snippets
    """
    questions = rewrite(question=query)
    print(questions)

    snippets = []
    for question in questions:
        for i in range(1):
            response = google_search(query=question, start=i*10+1, num=10)
            if 'items' not in response.keys():
                response = google_search(query=response['spelling']['correctedQuery'], start=i*10+1, num=10)
            for item in response['items']:
                snippet = item['snippet']
                snippets.append(snippet)
    snippets = "\n".join(snippets)
    print(snippets)
    return generate_answer(prompt=query, context=snippets)

def get_paragraphs(url):
    try:
        # article = fetch_url(url)
        article = Article(url)
        article.download()
        article.parse()
        return article.text.split("\n\n")
        # if article is not None:
            # return extract(article).split("\n")
    except:
        return []
    
def rrr_pages(query, n=10):
    """
    use google search to retrieve pages
    then get paragraphs from those pages
    finally, calculate bm25 scores for each paragraph
    """
    questions = rewrite(question=query)
    print(questions)
    urls = []
    for question in questions:
        response = google_search(query=question, start=1, num=3)
        # print(response)
        if 'items' not in response.keys():
            response = google_search(query=response['spelling']['correctedQuery'], start=1, num=3)
        urls.extend([item['link'] for item in response['items']])

    with multiprocessing.Pool(4) as pool:
        paras = pool.map(get_paragraphs, urls)
    
    paras = [para for para_list in paras for para in para_list]
    tokenized_corpus = [doc.split(" ") for doc in paras]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.split(" ")
    bm25_results = bm25.get_top_n(tokenized_query, paras, n=n)
    docs = "\n\n".join(bm25_results)

    print(docs)
    return generate_answer(prompt=query, context=docs)

if __name__=="__main__":
    # Test pages
    start = time()
    
    query = "Vượt đèn đỏ tông người thì bị sao ?"

    answer = rrr_pages(query=query, n=10)
    # answer = rrr_snippets(query=query)
    print("ANSWER:", answer)

    end = time()
    print("Time: ", end - start)