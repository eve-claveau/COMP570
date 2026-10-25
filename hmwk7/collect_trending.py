# scrape the homepage of Montreal Gazette

# scrape the key information off the article page itself
import argparse
import pandas as pd
from bs4 import BeautifulSoup as BS
import requests
import json
import time

def main_2():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", required=True, help="name of the output file in json format")
    args = parser.parse_args()
    with open("html_source/page_source.html") as fi:
        html = fi.read()
    links = []
    soup = BS(html, "html.parser")
    # get the links to trending stories from homepage
    news_element = soup.select(".pm-card__heading-link")
    print(f'len(news_element)')
    for e in news_element:
        links.append(e['href'])
        print(e['href'], e.text)
    # use caching to avoid overly taxing the Montreal Gazette website
    trending = []
    for i in range(5):
        response = requests.get(links[i])
        soup = BS(response.text, "html.parser")
        info = soup.find("script", {"class":"yoast-schema-graph"})
        json_data = json.loads(info.string)
        record = {
            "title": "",
            "publication date": "",
            "author": "",
            "blurb": ""            
        }
        for item in json_data:
            if item.get("@type") == "Article":
                record["title"] = item.get('headline')
                record["publication_date"] = item.get('datePublished')
                record["blurb"] = item.get('Description')
            if item.get("@type") == "Person":
                record["author"] =  item.get('name')
        print(record)
        trending.append(record)
    json.dump(trending, args.o)

def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", required=True, help="name of the output file in json format")
    args = parser.parse_args()
    
    with open("html_source/page_source.html") as fi:
        html = fi.read()
        
    links = []
    soup = BS(html, "html.parser")
    
    # get the links to trending stories from homepage
    # Added the featured article class as well so you don't miss the #1 story
    news_element = soup.select(".pm-featured-article-vertical__heading-link, .pm-card__heading-link")
    print(f'Found {len(news_element)} article links on the homepage.')
    
    for e in news_element:
        href = e.get('href')
        if href and href.startswith('/'):
            href = f"https://montrealgazette.com{href}"
        if href not in links: # Prevent duplicates
            links.append(href)

    trending = []
    
    # Setup headers to look like a normal Google Chrome browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    limit = min(5, len(links))
    for i in range(limit):
        print(f"Scraping {i+1}/5: {links[i]}")
        
        # Pass the headers into the request!
        response = requests.get(links[i], headers=headers)
        
        # Check if we got blocked anyway
        if response.status_code != 200:
            print(f"Failed to fetch {links[i]} - Status Code: {response.status_code}")
            continue
            
        soup = BS(response.text, "html.parser")
        
        info = soup.find("script", {"class": "yoast-schema-graph"})
        if not info:
            print("  -> Could not find the JSON-LD schema on this page.")
            continue
            
        json_data = json.loads(info.string)
        graph_items = json_data.get("@graph", [])
        
        record = {
            "title": "",
            "publication date": "",
            "author": "",
            "blurb": ""            
        }
        
        for item in graph_items:
            if item.get("@type") == "Article":
                record["title"] = item.get('headline', '')
                record["publication date"] = item.get('datePublished', '')
            elif item.get("@type") == "WebPage":
                record["blurb"] = item.get('description', '')
            elif item.get("@type") == "Person":
                record["author"] = item.get('name', '')
                
        trending.append(record)
        
        # Add a tiny delay to be polite to their servers
        time.sleep(1)
        
    with open(args.o, 'w', encoding='utf-8') as fo:
        json.dump(trending, fo, indent=4, ensure_ascii=False)
    
    print(f"\nSuccessfully saved {len(trending)} records to {args.o}")

if __name__ == "__main__":
    main()
    