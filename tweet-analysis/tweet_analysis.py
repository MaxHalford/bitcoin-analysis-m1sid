import bs4 as BeautifulSoup

annees = [x for x in range(2009, 2016)]

html = ''
for an in annees:
    html += html
    with open('../data/tweets/negatifs/{}.html', 'r').format(an) as myfile:
        html = myfile.read().replace('\n', '')
