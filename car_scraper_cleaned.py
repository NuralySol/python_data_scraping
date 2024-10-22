
#! Import all the needed libraries for scraping data from "https://classiccars.com/"
import requests
from bs4 import BeautifulSoup

url = "https://classiccars.com/"

response = requests.get(url)

# Check if the request was successful (status code 200) GET = 200. 
if response.status_code == 200:
    # Parse the HTML content using bs4 and save it in the variable soup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all listings for the day using the elements of the DOM
    car_listings = soup.find_all("a", class_="home-list-link")
    
    #! Extract and display information for each listing of the day using a for loop
    for car in car_listings:
        car_title = car.find("div", class_="h-title")
        car_description = car.find("div", class_="ah-description")
        car_price = car.find("b")
        
        #! Validator to handle missing cases where the DOM elements might be missing
        clean_title = car_title.get_text(strip=True) if car_title else "Title not found"
        clean_description = car_description.get_text(strip=True) if car_description else "Description not found"
        
        # Clean price by removing $ and commas, and convert to float if possible!
        if car_price:
            price_str = car_price.get_text(strip=True).replace('$', '').replace(',', '')
            try:
                clean_price = float(price_str)
            except ValueError:
                clean_price = "Price not available"
        else:
            clean_price = "Price not available"
        
        car_link = car['href'] if car.has_attr('href') else "Link not available"
        
        #! Print the output in the console (terminal)
        print(f"Car Title: {clean_title}")
        print(f"Description of the car: {clean_description}")
        print(f"Price: {clean_price}")
        print(f"More Info at this link: https://classiccars.com{car_link}")
        print("-" * 100) #! Line separator for cleaner output
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}") 