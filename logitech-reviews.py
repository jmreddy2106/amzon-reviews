import requests
from scrapy.http import HtmlResponse
import pandas as pd
import time
import math

reviews = []
res = requests.get(
    'https://www.amazon.in/Logitech-B170-Wireless-Mouse-Black/product-reviews/B01J0XWYKQ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
response = HtmlResponse(url=res.url, body=res.content)
product_name = response.xpath('//h1/a/text()').extract_first(default=' ').strip()
total_reviews = response.xpath('//span[contains(text(),"Showing")]/text()').extract_first(default='').strip().split()
total_reviews = total_reviews[-2]
total_reviews = int(total_reviews.replace(',', '').strip())
reviews_per_page = math.ceil(int(total_reviews) / 10)

for i in range(0, reviews_per_page):
    time.sleep(1)
    try:
        url1 = f'https://www.amazon.in/Logitech-B170-Wireless-Mouse-Black/product-reviews/B01J0XWYKQ/ref=cm_cr_arp_d_paging_btm_next_{str(i + 1)}?ie=UTF8&reviewerType=all_reviews&pageNumber={str(i + 1)}'
        res = requests.get(url1)
        response = HtmlResponse(url=res.url, body=res.content)
        loop = response.xpath('//div[contains(@class,"a-section review")]')

        for part in loop:
            # review_title = part.xpath('.//a[contains(@Class,"review-title-content")]/span/text()').extract_first(
            #     default=' ').strip()
            #
            # rating = \
            # part.xpath('.//a[contains(@title,"out of 5 stars")]/@title').extract_first(default=' ').strip().split()[
            #     0].strip()
            reviewer_name = part.xpath('.//span[@class="a-profile-name"]/text()').extract_first(default=' ').strip()
            print(reviewer_name)
            description = ''.join(
                part.xpath('.//span[contains(@class,"review-text-content")]/span/text()').extract()).strip()
            # helpful_count = \
            #     part.xpath('.//span[contains(@class, "cr-vote-text")]/ text()').extract_first(default='').strip().split()[
            #     0].strip()
            reviews.append([reviewer_name, description])
            df = pd.DataFrame(reviews,
                              columns=['ReviewerName', 'Description'])
            # exporting csv
            df.to_csv("./amazon-reviews.csv", index=False)

    except requests.exceptions.HTTPError as e:
        print(e.response.text)

print('No of Reviews are :' + str(total_reviews))
