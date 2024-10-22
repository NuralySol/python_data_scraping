
#! import all the needed libraries for the scrapping of the data "https://classiccars.com/"
import requests
from bs4 import BeautifulSoup

url = "https://classiccars.com/"

response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup and save it in the variable soup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all listings for the day using the elements of the DOM
    car_listings = soup.find_all("a", class_="home-list-link")
    
    #! Extract and display information for each listing of the day using for loop (convert data types from strings to floats and remove the $ signs from the output of the of print)
    for car in car_listings:
        car_title = car.find("div", class_="h-title")
        car_description = car.find("div", class_="ah-description")
        car_price = car.find("b")
        
        #! validator to handle the missing cases where the DOM elements might be missing 
        clean_title = car_title.get_text(strip=True) if car_title else "Title not found"
        clean_description = car_description.get_text(strip=True) if car_description else "Description not found"
        clean_price = car_price.get_text(strip=True) if car_price else "Price not available"
        car_link = car['href'] if car.has_attr('href') else "Link not available"
        
        #! print the output in the console (terminal)
        print(f"Car Title: {clean_title}")
        print(f"Description of the car: {clean_description}")
        print(f"Price: {clean_price}")
        print(f"More Info at this link: https://classiccars.com{car_link}")
        print("-" * 50) #! line seperator for cleaner output
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")