import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewlist = []


def get_soup(url):
    r = requests.get('http://192.168.99.100:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
                'product': soup.title.text.replace('Amazon.in:Customer reviews:', '').strip(),
                'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'rating': float(
                    item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
            print(review)
    except:
        pass


name = input("Enter the URL of product you want to scrape : ")
for x in range(1, 700):
    soup = get_soup(
        f'{name}''&pageNumber='f'{x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    if soup.find('li', {'class': 'a-last'}):
        pass
    else:
        break

df = pd.DataFrame(reviewlist)
product_name = df['product'][0]
csv_data = df.to_csv(index=False)
df.to_csv("%s.csv" % product_name, index=False)
print('Extracted')
