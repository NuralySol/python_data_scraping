import requests
from bs4 import BeautifulSoup
import pandas as pd

# The URL of the website to scrape the website contains 1-50 pages
url = "https://books.toscrape.com/"


# Function to scrape data for each book (use try and except for API call if == 200 GET then proceed)
def scrape_books_data(url):
    try:
        # Send a request to the website using the requests library with url argument which is defined above
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using the bs4 library since Python can not read HTML naturally
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all book listings on the page
            books = soup.find_all("article", class_="product_pod")

            # List to store book_data = [] an empty list
            book_data = []

            # Extract information from each book listing using the DOM hooks of the HTML page (save them to variables)
            for book in books:
                # Get the title of the book and store it in the title var
                title = book.h3.a["title"]

                # Get the price of the book and store it in the price var
                price = book.find("p", class_="price_color").text

                # Check the availability of the book store it in the availability var
                availability = book.find(
                    "p", class_="instock availability"
                ).text.strip()

                # Get the link to the book's details page and store it in the book_link var
                book_link = book.h3.a["href"]

                # Append the book details to the list to be called upon later! using the above variables
                book_data.append(
                    {
                        "Title": title,
                        "Price": price,
                        "Availability": availability,
                        "Details Link": f"https://books.toscrape.com/{book_link}",
                    }
                )
            #! return the book_data that is appended using the .append method and take it a dictionary
            return book_data

        else:
            print(
                f"Failed to retrieve content from the website. Status code: {response.status_code}"
            )
            # if failed to retrive GET other than 200, then return an empty list
            return []
    #! Error
    except Exception as e:
        print(f"An error occurred while scraping the website: {e}")
        #! return an empty list as an error
        return []


#! Function to get all book data from multiple pages dynamic aproach to the HTML pages.
def scrape_all_pages(base_url):
    page_num = 1
    # need an empty list of all_books_data = [] and spread it like in JS using extends down the code line.
    all_books_data = []

    # dynamic passing the url link f"{base_url}catalogue/page-{page_num}.html" with increament operator in While True:
    while True:
        page_url = f"{base_url}catalogue/page-{page_num}.html"

        # Scrape book data from the current page and += increament page_num of url string
        books_data = scrape_books_data(page_url)
        # break the loop when it reaches the logical end of the pages to increment
        if books_data:
            all_books_data.extend(books_data)
            page_num += 1
        else:
            break
    # return all_books_data to be called in the script
    return all_books_data


# Main execution (within the script itself)
if __name__ == "__main__":
    # Scrape all book data from the website (run the the main function)
    all_books = scrape_all_pages(url)

    # Create a DataFrame from the all_books
    df_books = pd.DataFrame(all_books)

    # Output the Data Frame in the terminal to see if Data Frame was actually created
    print(df_books)

    # Save the csv to the fixtures directory within the project not using the os module
    df_books.to_csv("./fixtures/books_data.csv", index=False)

"""
Summary:

This script scrapes book data (title, price, availability, and details link) from the website "Books to Scrape" across multiple pages. It uses the following key steps:

1. **Requests & BeautifulSoup**:
- Uses the `requests` library to send HTTP requests to the website.
- Uses the `BeautifulSoup` library to parse the HTML content and extract relevant data from the DOM (Document Object Model).

2. **Scraping Book Data**:
- The `scrape_books_data(url)` function fetches and extracts information about each book on the current page.
- It captures the title, price, availability, and details link for each book and appends this data into a list of dictionaries.

3. **Pagination Handling**:
- The `scrape_all_pages(base_url)` function handles pagination by incrementing the page number dynamically.
- It continues scraping each page until no more book data is available, collecting all book details in the process.

4. **DataFrame Creation**:
- The scraped data is stored in a pandas `DataFrame` for easy manipulation, output, and analysis.

5. **Saving Data to CSV**:
- The book data is saved to a CSV file named `books_data.csv` located in the `fixtures` directory within the project.

6. **Error Handling**:
- Try-except blocks handle errors during HTTP requests and page parsing, ensuring the program continues to run even if issues occur during scraping.
"""
