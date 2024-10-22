#! Import all the needed libraries for scraping data from "https://classiccars.com/"
#! Added pandas to display and convert lists to Data Frames
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Save the web URL to the 'url' variable
url = "https://classiccars.com/"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful (status code 200) 
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup and save it in the 'soup' variable
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all car listings for the day using relevant DOM elements
    car_listings = soup.find_all("a", class_="home-list-link")

    # Initialize an empty list to store car data
    car_data = []

    #! Extract information from each car listing
    for car in car_listings:
        car_title = car.find("div", class_="h-title")
        car_description = car.find("div", class_="ah-description")
        car_price = car.find("b")

        # Handle missing cases and clean the data
        clean_title = car_title.get_text(strip=True) if car_title else "Title not found"
        clean_description = (
            car_description.get_text(strip=True)
            if car_description
            else "Description not found"
        )

        # Clean price by removing $ and commas, and convert to float if possible
        if car_price:
            price_str = car_price.get_text(strip=True).replace("$", "").replace(",", "")
            try:
                clean_price = float(price_str)
            except ValueError:
                clean_price = None  # Set to None for invalid price entries
        else:
            clean_price = None

        # Extract the link to the car's detailed page
        car_link = car["href"] if car.has_attr("href") else "Link not available"

        # Append car_data to the list for later DataFrame creation
        car_data.append(
            {
                "Title": clean_title,
                "Description": clean_description,
                "Price": clean_price,
                "Link": f"https://classiccars.com{car_link}",
            }
        )

    # Create a DataFrame from the car_data
    df_cars = pd.DataFrame(car_data)

    # Display the DataFrame in the terminal for review
    print(df_cars)

    # Drop rows where 'Price' is None (invalid price entries)
    df_cars_filtered = df_cars.dropna(subset=["Price"])

    # Create a figure for plotting the prices of the cars
    plt.figure(figsize=(12, 6))

    # Plot a bar chart for car prices with titles
    bars = plt.barh(
        df_cars_filtered["Title"],
        df_cars_filtered["Price"],
        color="lightblue",
        edgecolor="black",
    )

    plt.title("Car Prices from ClassicCars.com", fontsize=16, weight="bold")
    plt.xlabel("Price of Classic Cars in $", fontsize=14)
    plt.ylabel("Car Title", fontsize=14)

    # Add annotations to each bar with the respective price value on the plot itself (use the Matloblib library)
    for bar, price in zip(bars, df_cars_filtered["Price"]):
        plt.text(
            bar.get_width() + 5000,
            bar.get_y() + bar.get_height() / 2,
            f"${price:,.0f}",
            va="center",
            ha="left",
            fontsize=10,
            color="black",
        )

    plt.tight_layout()

    plt.show()

else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")

    """
Summary of the Code:

1. Request Handling:
- Sends an HTTP GET request to the `classiccars.com` website.
- Checks if the request was successful with status code 200.

2. Data Extraction:
- Uses BeautifulSoup to parse the HTML content.
- Extracts information from each car listing: car title, description, price, and link to the detailed page.

3. Data Cleaning:
- Price data is cleaned by removing the dollar signs and commas.
- Price is converted to a float if valid, otherwise, None is assigned.
- Handles missing data by assigning default values for missing titles, descriptions, and links.

4. Data Storage:
- Organizes the extracted data in a pandas DataFrame.
- Filters out rows with missing or invalid price entries.

5. Data Visualization:
- Creates a horizontal bar plot displaying car prices.
- Adds annotations to each bar showing the price in dollars.
- Adjusts layout and annotations for better readability.
"""
