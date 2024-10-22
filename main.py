# Python data scraping lesson (need the below imports to read HTML)
import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "http://shakespeare.mit.edu/lll/full.html"

# Sending a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print(f"Response Status: {response.status_code} (Success)")
else:
    print(f"Failed to retrieve content: {response.status_code}")

# Parsing the content with BeautifulSoup
bsobj = BeautifulSoup(response.content, "html.parser")

# Printing the BeautifulSoup object
print("Soup Object Created:\n", bsobj)

# Finding all the <h3> tags in the HTML
h3_list = bsobj.find_all("h3")

# Printing the raw list of <h3> tags
print(f"\nRaw HTML List of <h3> Tags:\n {h3_list}")

# Creating a clean list of the text content of each <h3> tag
clean_list = [i.get_text() for i in h3_list]

# Printing the clean list using list comprehension
for i, item in enumerate(clean_list, 1):
    print(f"Output list comprehension: {i}. {item}")

# Different ways of iterating over the list
numbers = [1, 2, 3, 4, 5, 5, 5, 5, 5]
fives = []

#! Loop through the numbers list and add all 5's to the fives list (lists are iterable)
for num in numbers:
    if num == 5:
        fives.append(num)

print(f"numbers print: {numbers}")
print(f"fives print without list comrehension: {fives}")

#! list comprehensions (always returns lists)
fives = [num for num in numbers if num == 5]
print(f"fives print uising the list comprehension: {fives}")


week = ["mon", "tue", "wed"]

# Capitalized using the list comprehension using the .capitalize method for string manipulation ()
capitalized_week = [day.capitalize() for day in week]

print(f"capitalized_week print{capitalized_week}")

#! cleaned_list object using the list comprehension to save to an object ot be called upon later
cleaned_list = [i.get_text() for i in h3_list]
print(f"cleaned_list: {cleaned_list}")

#! getting the first phrase
phrase = bsobj.find("a", {"name": "1.1.9"}).get_text()
print(f"phrase getting using: {phrase}")

#! getting the other phrase with a different variable 
phrase_1 = bsobj.find("a", {"name": "1.1.13"}).get_text()
print(f"phrase_1 getting using: {phrase_1}")
x