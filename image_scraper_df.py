import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Save the web URL to the 'url' variable
url = "https://classiccars.com/"

# Function to dynamically extract a title from the URL
def extract_title_from_url(image_url):
    # Split the URL by '/' and get the last part
    filename = image_url.split("/")[-1]
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
            with open(file_path, 'wb') as file:
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
            print(f"Failed to retrieve content from the website. Status code: {response.status_code}")
            return []

    except Exception as e:
        print(f"An error occurred while scraping the website: {e}")
        return []

# Main execution
if __name__ == "__main__":
    # Scrape the image URLs from the website
    image_urls = scrape_car_images(url)

    # Folder to save images
    folder_name = os.path.join(os.getcwd(), "assets")

    # List to store image data
    image_data = []

    # Download and save each image, and store metadata
    for image_url in image_urls:
        fetch_url(image_url, folder_name)
        image_data.append({"Title": extract_title_from_url(image_url), "URL": image_url})

    # Convert image data to a DataFrame
    df_images = pd.DataFrame(image_data)

    # Display the DataFrame
    print(df_images)

    # Optionally, save the DataFrame to a CSV file
    df_images.to_csv("./fixtures/scraped_images.csv", index=False)