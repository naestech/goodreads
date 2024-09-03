import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

# function to fetch the rss feed from the provided url
def fetch_rss_feed(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch RSS feed: {response.status_code}")

# function to extract title and author from rss content
def extract_titles_and_authors(rss_content_list):
    books = []

    for rss_content in rss_content_list:
        root = ET.fromstring(rss_content)
        channel_info = root.find("channel")

        # parse and extract each item's title and author
        for item in channel_info.findall("item"):
            title = item.find("title").text if item.find("title") is not None else "No Title"
            description = item.find("description").text if item.find("description") is not None else ""
            
            # extract author from description
            author_start = description.find("author:") + len("author:")
            author_end = description.find("<br/>", author_start)
            author = description[author_start:author_end].strip() if author_start != -1 and author_end != -1 else "No Author"

            books.append((title, author))

    return books

# function to save titles and authors into an xml file
def save_titles_and_authors_to_xml(books, filename):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    for title, author in books:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "author").text = author

    # prettify and save the xml
    rough_string = ET.tostring(rss, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(filename, "w") as file:
        file.write(pretty_xml)

# main function
def main():
    # list of rss urls to fetch
    rss_urls = [
       # add rss urls here
    ]

    # fetch rss content from all urls
    rss_content_list = [fetch_rss_feed(url) for url in rss_urls]

    # extract titles and authors
    books = extract_titles_and_authors(rss_content_list)

    # save the titles and authors into an xml file
    save_titles_and_authors_to_xml(books, "title_author_rss_combined.xml")

    print("Titles and authors have been saved to 'title_author_rss_combined.xml'.")

if __name__ == "__main__":
    main()

