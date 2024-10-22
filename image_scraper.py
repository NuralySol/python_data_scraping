import requests
from bs4 import BeautifulSoup
import os  #! For handling files and directories
import pandas as pd #! for creating a Data Frames out of scraped images from the url

# The URL of the website to scrape
url = "https://classiccars.com/"


# Function to dynamically extract a title from the URL
def extract_title_from_url(url):
    # Split the URL by '/' and get the last part
    filename = url.split("/")[-1]
    # Remove file extension and replace dashes with underscores
    title = filename.replace("-thumb.jpg", "").replace("-", "_")
    return title


# Function to fetch and save the image from a given URL
def fetch_url(image_url, folder_name):
    # Dynamically generate the title from the URL
    title = extract_title_from_url(image_url)

    # Check if the specified folder exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Set the local file path where the image will be saved
    file_path = os.path.join(folder_name, f"{title}.jpg")

    try:
        # Send a request to the URL to get the image content
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the image content to a local file
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Image saved as {file_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Function to scrape the website for image URLs
def scrape_car_images(url):
    try:
        # Send a request to the website
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all the car listings with images
            car_images = soup.find_all("img", class_="cm-tooltip")

            # Extract the image URLs
            image_urls = []
            for car_image in car_images:
                if car_image.has_attr("data-src"):
                    image_url = car_image["data-src"]
                    image_urls.append(image_url)
                    print(f"Found image URL: {image_url}")

            return image_urls

        else:
            print(
                f"Failed to retrieve content from the website. Status code: {response.status_code}"
            )
            return []

    except Exception as e:
        print(f"An error occurred while scraping the website: {e}")
        return []


# Main execution block - This ensures that the code only runs when the script is executed directly,
# and not when it is imported as a module into another script.

if __name__ == "__main__":

    # Step 1: Scrape the image URLs from the website by calling the 'scrape_car_images' function.
    # This function parses the website and extracts all image URLs.
    image_urls = scrape_car_images(url)

    # Step 2: Define the folder where the images will be saved.
    # 'os.path.join(os.getcwd(), "assets")' creates the folder path 'assets' inside the current working directory.
    folder_name = os.path.join(os.getcwd(), "assets")

    # Step 3: Loop through each image URL that was scraped.
    # For each image URL, call the 'fetch_url' function to download and save the image to the folder.
    for image_url in image_urls:
        fetch_url(image_url, folder_name)

"""
Summary:

This script scrapes car image URLs from the "https://classiccars.com/" website and downloads them into a specified folder. Here’s a breakdown of how it works:

1. **extract_title_from_url(url)**:
- Extracts and formats the title from the image URL to use it as the image filename.

2. **fetch_url(image_url, folder_name)**:
- Downloads and saves the image from the given URL to a local folder.
- If the folder doesn’t exist, it creates one.
- Handles errors during the download process and ensures the image is saved successfully.

3. **scrape_car_images(url)**:
- Scrapes the website for image URLs by finding all `<img>` tags with a specific class ("cm-tooltip").
- Extracts the `data-src` attribute which contains the actual image URL.

4. **Main execution**:
- The script scrapes all image URLs from the website and saves them in the "assets" folder inside the project directory.
- For each image URL, the script calls the `fetch_url` function to download and save the image.
"""
