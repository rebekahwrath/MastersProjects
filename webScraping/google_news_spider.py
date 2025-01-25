import os
import logging
import scrapy
import json
from collections import Counter
import matplotlib.pyplot as plt

# creating a SCRAPY spider to scrape Google News

class GoogleNewsSpider(scrapy.Spider):
    name = "google_news"
    output_file = 'articles.json'  # path to the JSON file where article titles will be stored

    # the start URL (Google News search)
    def start_requests(self):
        # check if articles.json exists already (created from previous searches)
        if os.path.exists(self.output_file):
            os.remove(self.output_file) # delete current articles.json file if it exists
            logging.info(f"Deleted existing file: {self.output_file}") # confirm deletion

        keywords = ['Tiktok', 'Ban', 'Trump'] # keywords to search for on Google News
        query = '+'.join(keywords)
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US%3Aen"
        yield scrapy.Request(url=url, callback=self.parse, meta={'keywords':keywords})

    # parse the XML RSS feed
    def parse(self, response):
        count = 0
        articles = []  # create a list to store article titles
        keyword_counts = Counter() # create a counter to count how often each keyword appears in each article title
        keywords = response.meta['keywords']
        
        # loop through each article title
        for item in response.xpath('//item'):
            if count >= 50:  # ensuring we only save 50 titles
                break
            title = item.xpath('title/text()').get() # get the article title
            if title: # check if the title was successfully extracted 
                article = {
                    'title': title,
                }
                articles.append(article) # add the title to the article title list 

                for keyword in keywords: # count the keywords in each article title
                    if keyword.lower() in title.lower(): # case insensitive
                        keyword_counts[keyword] +=1
                        
                count += 1 # update counter 
        
        # write articles to the JSON file once scraping is complete
        if articles:
            with open(self.output_file, 'w') as f:
                json.dump(articles, f, indent=4)
            logging.info(f"Scraped {len(articles)} articles and saved to {self.output_file}") # print to ensure spider is working & we have scraped 50 titles

        self.generate_histogram(keyword_counts)

    def generate_histogram(self, keyword_counts): # generate histogram with keyword counts 
        if keyword_counts:
            keywords = list(keyword_counts.keys())
            counts = list(keyword_counts.values())

            plt.figure(figsize=(10,6))
            plt.bar(keywords, counts, color='skyblue')
            plt.xlabel('Keyword')
            plt.ylabel('Frequency')
            plt.title('Keyword Frequency in Article Titles')
            plt.tight_layout()

            plt.savefig('keyword_histogram.png')
            logging.info('Histogram saved as keyword_histogram.png')

            plt.show()
        else:
            logging.info("No keywords found.")


# MAC RUNNING INSTRUCTIONS       
# to run the spider in your terminal use this command: scrapy runspider google_news_spider.py -o articles.json --loglevel=INFO
# to view the saved articles in your terminal use the command: cat articles.json




















