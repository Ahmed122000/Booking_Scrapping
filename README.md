
# Booking Scraping

This project automates the extraction of hotel data from the Booking.com website using Python. It scrapes hotel listings for details such as hotel name, address, images, amenities, ratings, and room types. The project handles dynamic content loading, processes and cleans the scraped data, and stores it in a structured format (JSON).

## Features
- Scrapes hotel listings from multiple cities
- Extracts detailed hotel information (name, address, amenities, etc.)
- Handles dynamic content loading using Selenium WebDriver
- Stores the scraped data in a structured **JSON** format
- Incorporates error handling and timeout exceptions for robustness
- Supports scraping up to 40 pages per city, collecting over 1,000 hotels

## Technologies Used
- **Python**
- **BeautifulSoup**: For parsing HTML and extracting data.
- **Requests**: For making HTTP requests.
- **Selenium WebDriver**: For handling JavaScript-rendered pages.
- **JSON**: For storing and structuring the scraped data.

## Installation

To get this project up and running on your local machine, follow the steps below:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Ahmed122000/Booking_Scrapping.git
    cd Booking_Scrapping
    ```

2. **Install the required Python packages**:

    It’s recommended to use a virtual environment. You can create one using the following commands:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use 'venv\Scriptsctivate'
    ```

    Then install the dependencies:

3. **Download WebDriver** (for Selenium):
   
   To use Selenium, you need to download a WebDriver (e.g., ChromeDriver) that matches your browser version. Place it in your project directory or specify its path in your script.

## Usage

1. **Run the scraper**: To start scraping hotel data, run the `scraper.py` script. The data will be saved in a `hotels.json` file.

    ```bash
    python booking_hotels.py
    ```

2. **Scrape specific cities**: You can modify the script to scrape data for specific cities by changing the city list in the code or passing arguments to the script.

3. **View scraped data**: The resulting data is stored in a `hotels.json` file, which contains all the extracted information in a structured format.

## Example Output (JSON)

The `hotels.json` file contains information like:

```json
[
  {
    "hotel_name": "Hotel ABC",
    "address": "123 Street, City",
    "amenities": ["Free Wi-Fi", "Swimming Pool", "Spa"],
    "rating": 4.5,
    "room_types": ["Single", "Double", "Suite"],
    "images": ["url1", "url2"]
  },
  ...
]
```

## Contributing

Feel free to fork this repository and submit pull requests for improvements or new features. If you find bugs, please report them via GitHub Issues.

---

If you have any questions or need help with the project, feel free to open an issue or contact me directly.
