import requests
from bs4 import BeautifulSoup
import pandas as pd

webpages = []
for i in range(10):
    webpages.append(f'http://quotes.toscrape.com/page/{i+1}/')

ls_df = []
for webpage in webpages:
    result = requests.get(webpage)

    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    
    # QUOTES
    quotes = soup.find_all('span', class_='text')
    ls_quote = []
    for quote in quotes:
        ls_quote.append(quote.text)

    #AUTHORS
    authors = soup.find_all('small', class_='author')
    ls_author = []
    for author in authors:
        ls_author.append(author.text)
    
    # TAGS
    tags = soup.find_all('div', class_='tags')
    ls_tag_prime = []
    for tag in tags:
        all_tags = tag.find_all('a', class_='tag')
        ls_tag = []
        for element in all_tags:
            ls_tag.append(element.text)
        ls_tag_prime.append(ls_tag)


    df = pd.DataFrame({
        'quotes' : ls_quote,
        'author' : ls_author,
        'tag' : ls_tag_prime
    })

    ls_df.append(df)

df_all = pd.concat(ls_df, ignore_index=True)
print(df_all)
df_all.to_csv('quotes-scrape.csv', index=False)