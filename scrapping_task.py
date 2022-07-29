from bs4 import BeautifulSoup as bs, Tag
import pandas as pd
import requests


def get_soup(url):
    open_flipkart = requests.get(url).text
    soup = bs(open_flipkart, "html.parser")
    return soup


def extract_data():
    soup = get_soup("https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9")
    html_table_data = []
    href_attr = []

    get_table = soup.find('table', {'class': 'wikitable'})
    heading_list = list(map(lambda s: s.string.strip(), get_table.find_all('th')))

    for table_row in get_table.tbody.children:
        if isinstance(table_row, Tag):
            data_row = []
            a_tag = list(table_row.children)[1].find_next('td').find('a')
            # Novel link
            try:
                href_attr.append("http://www.wikipedia.com/" + a_tag['href'])
            except:
                pass

            for data_cell in table_row.children:
                if isinstance(data_cell, Tag):
                    data_cell = data_cell.get_text().strip()
                    if data_cell not in heading_list:
                        data_row.append(data_cell)
            html_table_data.append(list(data_row))
    html_table_data = list(filter(None, html_table_data))

    df = pd.DataFrame(html_table_data, index=list(range(0, len(html_table_data))), columns=heading_list)
    new_df = pd.DataFrame({'book': href_attr})
    df = df.join(new_df)
    df.to_csv("table.xlsx", index=False, encoding="utf-8")


extract_data()
