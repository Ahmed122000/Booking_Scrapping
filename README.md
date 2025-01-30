# Hotel Scraper and API Service

## Project Description
This project provides a web scraping and API service for collecting detailed hotel information from Booking.com. It consists of two main components:

1. **Web Scraper**: A Python-based scraper that extracts hotel information such as address, images, room types, amenities, and reviews.
2. **Flask API**: A RESTful API built using Flask that allows users to interact with the scraper and retrieve hotel data in JSON format or save it as a downloadable file.

## Features
- Scrape hotel details from Booking.com for specific cities in Egypt.
- Extract information such as address, amenities, room types, and images.
- Save the scraped data as JSON files.
- API endpoints to:
  - Retrieve city codes for scraping.
  - Start a scraping process and get results.
  - Download scraped data as a file.

---

## File Structure

### 1. `booking_hotels.py`
This file contains the core scraping logic, implemented in the `Scraper` class.

**Key Features:**
- Initializes a Selenium WebDriver to interact with dynamic web pages.
- Parses hotel information using BeautifulSoup.
- Handles multiple cities and pagination for comprehensive scraping.
- Saves scraped data in JSON format.

### 2. `app.py`
This file implements the Flask API service, enabling interaction with the scraper.

**Endpoints:**
1. **`GET /codes`**: Returns a list of city codes for scraping.
   - **Response Format**:
     ```json
     {
       "cairo": "290692",
       "alexandria": "290263",
       ...
     }
     ```

2. **`GET /scrape`**: Initiates the scraping process.
   - **Query Parameters:**
     - `city`: Name of the city to scrape (required).
     - `city_code`: City code for Booking.com (required).
     - `pages`: Number of pages to scrape (default: 1).
     - `format`: Output format (`json` or `file`).
   - **Response:**
     - Returns hotel data in JSON format or a download link to the JSON file.

3. **`GET /download/<file_name>`**: Downloads a previously saved JSON file.
   - **Response:**
     - File download if it exists, otherwise an error message.

---

## Installation and Setup

### Prerequisites
- Python 3.7+
- Firefox browser
- Geckodriver for Selenium

### Required Python Libraries
Install the required libraries using the following command:
```bash
pip install -r requirements.txt
```

### `requirements.txt`
```
beautifulsoup4
selenium
requests
flask
```

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask API:
   ```bash
   python app.py
   ```

4. Access the API on `http://localhost:5000`.

---

## Usage

### Example API Usage
#### Retrieve City Codes
```bash
GET http://localhost:5000/codes
```
Response:
```json
{
  "cairo": "290692",
  "alexandria": "290263",
  "hurghada": "290029",
  ...
}
```

#### Start Scraping
```bash
GET http://localhost:5000/scrape?city=cairo&city_code=290692&pages=1&format=json
```
Response:
- JSON data of scraped hotels or a download link for the file:
  ```json
  {
    "message": "Scraping for cairo completed. Data saved",
    "download_link": "http://localhost:5000/download/cairo_hotels_1672503492.json"
  }
  ```

#### Download Data
```bash
GET http://localhost:5000/download/cairo_hotels_1672503492.json
```

---

## Logging
- Logs are saved in `Scraper.log` for monitoring scraping progress and errors.

---

## Limitations
- The scraper is designed specifically for Booking.com and might require updates if the website structure changes.
- Ensure adherence to Booking.com’s Terms of Service when using this tool.

---

## Contributing
Feel free to fork the repository and submit pull requests for improvements or bug fixes.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contact
For issues or suggestions, please create an issue in the repository or contact [ahmedhesham122000@gmail.com].


