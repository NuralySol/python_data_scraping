
#! Import all the needed libraries for scraping data from "https://classiccars.com/"
#! Added pandas to display and convert lists to Data Frames, and expanded to scrape car images
import requests
from bs4 import BeautifulSoup
import pandas as pd

# save the web string to url variable
url = "https://classiccars.com/"

# response variable to request.get(url) of the website to scrape
response = requests.get(url)

# Check if the request was successful (status code 200) GET = 200. (nested if and for loop code below)
if response.status_code == 200:
    # Parse the HTML content using bs4 and save it in the variable soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all listings for the day using the elements of the DOM
    car_listings = soup.find_all("a", class_="home-list-link")

    # Initialize an empty list to store car data (need an empty list to store for the creation of the Data Frame)
    car_data = []

    #! Extract and display information for each listing of the day using a for loop
    for car in car_listings:
        car_title = car.find("div", class_="h-title")
        car_description = car.find("div", class_="ah-description")
        car_price = car.find("b")
        car_image = car.find("img")  # Find the image tag within the listing

        #! Validator to handle missing cases where the DOM elements might be missing
        clean_title = car_title.get_text(strip=True) if car_title else "Title not found"
        clean_description = (
            car_description.get_text(strip=True)
            if car_description
            else "Description not found"
        )

        # Clean price by removing $ and commas, and convert to float if possible!
        if car_price:
            price_str = car_price.get_text(strip=True).replace("$", "").replace(",", "")
            try:
                clean_price = float(price_str)
            except ValueError:
                clean_price = "Price not available"
        else:
            clean_price = "Price not available"

        # Extract image URL if available
        if car_image and car_image.has_attr("src"):
            car_image_url = car_image["src"]
        else:
            car_image_url = "Image not available"
        
        # Extract the link to the car's detailed page
        car_link = car["href"] if car.has_attr("href") else "Link not available"

        # Append car_data to the list as a dictionary to be created as a Data Frame later
        car_data.append(
            {
                "Title": clean_title,
                "Description": clean_description,
                "Price": clean_price,
                "Link": f"https://classiccars.com{car_link}",
                "Image URL": car_image_url
            }
        )

    # Create a DataFrame from the car_data Object which in original form is a list.
    df_cars = pd.DataFrame(car_data)

    # Display the DataFrame to the terminal output to check if DF has been created
    print(df_cars)

    # Save the data frame to csv fixtures folder
    df_cars.to_csv("./fixtures/classic_cars_listings_with_images.csv", index=False)

    print("Car data, including images, has been successfully saved to 'classic_cars_listings_with_images.csv'")
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")

"""
The above script loops through each car listing and extracts details such as:
- Title (from div with class h-title)
- Description (from div with class ah-description)
- Price (from b tag)
- Link (from the href attribute of the <a> tag)
- Image URL (from the img tag)

If any of these elements are missing, the code gracefully handles it by assigning default values like 
"Title not found", "Description not found", "Price not available", or "Image not available".

The price is also cleaned by removing the $ and , characters, and converting it to a float if possible.

Storing Data in a DataFrame:
- The extracted car details are stored in a list of dictionaries.
- The list is then converted into a pandas DataFrame (df_cars).
- The DataFrame is saved as a CSV file in the fixtures folder.
"""