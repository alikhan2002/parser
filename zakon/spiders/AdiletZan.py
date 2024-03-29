import scrapy
from bs4 import BeautifulSoup, NavigableString, Tag
import json
import requests
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlencode

# Creates a ZenRows proxy URL for a given target_URL using the provided API key.
def get_zenrows_api_url(url, api_key):
    payload = {
        'url': url,
        'js_render': 'true',
        'antibot': 'true',
        'premium_proxy': 'true'
    }
    # Construct the API URL by appending the encoded payload to the base URL with the API key
    api_url = f'https://api.zenrows.com/v1/?apikey={api_key}&{urlencode(payload)}'
    return api_url
class AdiletzanSpider(scrapy.Spider):
    name = "AdiletZan"
    # allowed_domains = [""]
    # start_urls = ["https://kodeksy-kz.com/ka/ugolovnyj_kodeks/1.htm"]
    # start_urls = ["https://adilet.zan.kz/rus/search/docs/"]
    d = {}
    title = ""

    # def __init__(self):
    #     self.driver = webdriver.Chrome()
    def start_requests(self):
        url = 'https://adilet.zan.kz/rus/search/docs'
        api_key = '4ab2cd9162ede4ce8a8c67cc6c095aa6be6fb8e7'
        api_url = get_zenrows_api_url(url, api_key)
        yield scrapy.Request(url=api_url, callback=self.parse)
    def parse(self, response):
        # self.logger.info(f'RESPONSE: {response.text}')
        hrefs = response.css('div.serp a').getall()
        links = []
        for html_snippet in hrefs:

            soup = BeautifulSoup(html_snippet, 'html.parser')#ll

            href_value = soup.find('a')['href']
            links.append(href_value)

        # links = ['/rus/docs/K1700000120']
        for link in links:
            yield response.follow(
                f'https://adilet.zan.kz{link}',
                callback=self.parse_article
            )


        next_page = response.css('a.nextpostslink::attr(href)').get()
        # next_page = None
        if next_page is not None:
            next_page_url = 'https://adilet.zan.kz' + next_page
            yield response.follow(next_page_url, callback=self.parse)



        # for page in range(1, 468):
        #     # print(page)
        #     yield response.follow(
        #         f'https://kodeksy-kz.com/ka/ugolovnyj_kodeks/{page}.htm',
        #         callback=self.parse_article,
        #         # priority=page
        #     )
        # yield data

    def parse_article(self, response):
        html_content = response.css('[class="container_alpha slogan"]').get()
        soup = BeautifulSoup(html_content, 'html.parser')
        self.title = soup.get_text(separator='\n', strip=True)
        # print(self.title)
        if 'Утративший силу' in self.title:
            return
        html_content = response.css("div.gs_12").get()
        soup = BeautifulSoup(html_content, 'html.parser')

        # def handle_br_tags(element):
        #     for br in element.find_all("br"):
        #         br.replace_with("\n" + br.text)
        #     text = element.get_text(strip=True)  # Get text will now include newline characters where <br> tags were
        #     return text
        # text_content = ""
        # for element in soup.find_all(['p', 'table']):
        #     if element.name == 'p':
        #         # Handle <br> tags within paragraphs
        #         text = handle_br_tags(element)
        #         text_content += text +'\n\n'
        #     elif element.name == 'table':
        #         for row in element.find_all('tr'):
        #             # Process each cell, handling <br> tags within cells
        #             row_data = [handle_br_tags(cell) for cell in row.find_all(['td', 'th'])]
        #             text_content += '\t'.join(row_data) + '\n'
        #         text_content += '\n'  # Add an extra newline to separate tables or sections
        text_content = soup.get_text()
        # print(text_content)
        data = {
            'title': self.title,
            'text': text_content
        }
        # print(data)
        # pass
        self.d = data
        self.to_txt()

    def to_txt(self):

        temp = self.d['title'] + '\n' + self.d['text']
        dir = 'C:/Users/aliha/Desktop/NLP/parser/zakon/new_dataset/'
        cleaned_name = re.sub(r'[\\/*?:"<>|\r\n]', " ", self.title)[:100] + ".txt"
        path = dir + cleaned_name
        with open(f'{path}', 'w', encoding='utf-8') as f:
            f.write(temp)

# import requests
# from bs4 import BeautifulSoup
#
#
# url = 'https://adilet.zan.kz/rus/docs/K1400000226'
# soup = BeautifulSoup(requests.get(url).content, 'html.parser')
#
#
# out = {}
# tag = soup.select_one('h3')
# current_header = tag.text
# while True:
#     tag = tag.find_next_sibling()
#     if not tag:
#         break



#     if tag.name == 'h3':
#         current_header = tag.text
#     else:
#         out.setdefault(current_header, '')
#         out[current_header] += tag.get_text(strip=True)
# print(out)
#

#
# from docx import Document
# from bs4 import BeautifulSoup
# from docx.oxml import OxmlElement
# from docx.oxml.ns import qn
#
# def add_hyperlink(paragraph, url, text, color='#0000FF', underline=True):
#     part = paragraph.part
#     r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
#
#     hyperlink = OxmlElement('w:hyperlink')
#     hyperlink.set(qn('r:id'), r_id)
#     hyperlink.set(qn('w:history'), '1')
#
#     new_run = OxmlElement('w:r')
#     rPr = OxmlElement('w:rPr')
#     if color:
#         c = OxmlElement('w:color')
#         c.set(qn('w:val'), color)
#         rPr.append(c)
#
#     # Set underline property for hyperlinks
#     u = OxmlElement('w:u')
#     if underline:
#         u.set(qn('w:val'), 'single')  # Set underline
#     else:
#         u.set(qn('w:val'), 'none')  # Remove underline
#     rPr.append(u)
#
#     new_run.append(rPr)
#     new_run.text = text
#     hyperlink.append(new_run)
#     paragraph._p.append(hyperlink)
#
#     return hyperlink
#
# # Example HTML content for demonstration
# html_content = '''
# <p>For more information, please refer to <a href="https://example.com/article_400">Article 400</a> of the current Code.</p>
# '''
#
# soup = BeautifulSoup(html_content, 'html.parser')
#
# # Create a new Document
# doc = Document()
#
# # Parse the HTML and add content to the Word document
# for content in soup.find_all('p'):
#     p = doc.add_paragraph()
#     for element in content.contents:
#         if element.name == 'a':
#             # Call with underline=True to ensure hyperlinks are underlined
#             add_hyperlink(p, element['href'], element.text, underline=True)
#         else:
#             p.add_run(element if isinstance(element, str) else element.text)
#
# # Save the document
# doc.save('output_with_hyperlinks.docx')
#
# print("Content saved to output_with_hyperlinks.docx")

