import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

# function to fetch the rss feed from the provided url
def fetch_rss_feed(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch RSS feed: {response.status_code}")

# function to pretty-print xml
def prettify(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# function to parse and format the rss feed
def format_rss_feed(rss_content):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    # parse the original rss content
    root = ET.fromstring(rss_content)
    channel_info = root.find("channel")

    # copy over channel metadata
    for tag in ["title", "link", "description", "language", "pubDate"]:
        element = channel_info.find(tag)
        if element is not None:
            ET.SubElement(channel, tag).text = element.text

    # copy image info if available
    image_info = channel_info.find("image")
    if image_info is not None:
        image = ET.SubElement(channel, "image")
        for tag in ["url", "title", "link"]:
            element = image_info.find(tag)
            if element is not None:
                ET.SubElement(image, tag).text = element.text

    # parse and reformat each item in the feed
    for item in channel_info.findall("item"):
        new_item = ET.SubElement(channel, "item")
        for tag in ["title", "link", "guid", "author", "category", "pubDate"]:
            element = item.find(tag)
            if element is not None:
                ET.SubElement(new_item, tag).text = element.text
        
        # add rating and pages as description if available
        description = item.find("description")
        if description is not None:
            ET.SubElement(new_item, "description").text = description.text

    return prettify(rss)

# main function
def main():
    # provide the rss url
    rss_url = # add rss urls here

    # fetch the rss content
    rss_content = fetch_rss_feed(rss_url)

    # format the rss feed
    formatted_rss = format_rss_feed(rss_content)

    # save to file
    with open("formatted_goodreads_to_read.xml", "w") as file:
        file.write(formatted_rss)
    
    print("RSS feed has been formatted and saved to 'formatted_goodreads_to_read.xml'.")

if __name__ == "__main__":
    main()

