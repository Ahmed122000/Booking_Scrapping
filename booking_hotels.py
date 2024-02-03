import requests
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



hotels = {'title' : [], 
          'average_score' : [], 
          'grade': [], 
          '#reviewers':[]
        } 
def get_rooms(page_source):
    room_detail = {}
    page = BeautifulSoup(page_source, 'lxml')
    address = page.find('span', class_='hp_address_subtitle js-hp_address_subtitle jq_tooltip').text
    description = page.find('p', class_='a53cbfa6de b3efd73f69').text
    aminty = page.find_all('span', class_='a5a5a75131')
    aminities = [x.text for x in aminty]
    rooms = page.find_all('div', class_='ed14448b9f b817090550 e7f103ee9e')
    for room in rooms:
         room_type = room.a.span.text
         bedroom = room.find('span', class_='baf7cb1417').text
         people = bedroom.split()[0]
         print(f'room type is: {room_type}, with {bedroom}, fit for {people} individuals') 
    
    room_detail['address'] = address

    print(f'address is: {address}') 
    print(f'aminty are: {aminities}')


def get_hotels(city_code, page_numbers=1):
    #dictionary to hold the data of each hotel

    #def get_hotels(country_code, page_numbers):
    for i in range(page_numbers):
        #page url()
        #we can update the code {&city} and number of page {&offset}
        url = f'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1FCAEiBWhvdGVsKIICOOgHSDNYA2hDiAEBmAEJuAEZyAEP2AEB6AEB-AENiAIBqAIDuAKZ7-2tBsACAdICJDQ5NDY3ZTNjLTZiYzMtNDFjNi05MGQ4LTk0NjAwNGNiZWRlY9gCBuACAQ&sid=0ca19a26ae77e73a83fd4cdc2f1ce287&aid=397594&city=-{city_code}&offset={i*25}'

        #open the driver and get the page
        driver = webdriver.Firefox()
        print(f'opening the link: {url}')
        driver.get(url)

        try:
            # Wait for some time for dynamic content to load
            wait = WebDriverWait(driver, 30)

        except TimeoutException as e:
            print(f"TimeoutException: {e}")
            #open file to write the page HTML of the page in case of timeout
            with open('source_code_exception.html', 'w') as f: 
                f.write(driver.page_source)
            print(f"Page source at timeout: {driver.page_source}")


        #print the file after the try/exception end
        print('save the file with no exception\n')
        with open('source_code.html', 'w') as f: 
                f.write(driver.page_source)

        page_source = driver.page_source
        driver.quit() #close the driver
        print(f'hotels in page {i+1}')
        #start scrapping
        soup = BeautifulSoup(page_source, 'lxml')
        #get the hotel card of each hotel 
        hotel_cards = soup.find_all('div', class_="c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4")
        
        #go through each card and check its info 
        for hotel_card in hotel_cards:
            #get the title
            title = hotel_card.find('div', class_ = 'f6431b446c a15b38c233').text
            
            #get average score
            average_score = hotel_card.find('div', class_ ='a3b8729ab1 d86cee9b25').text
            
            #get the grade
            grade = hotel_card.find('div', class_='a3b8729ab1 e6208ee469 cb2cbb3ccb').text
            
            #get number of reviewers
            reviewers = hotel_card.find('div', class_='abf093bdfe f45d8e4c32 d935416c47').text
    
            #get link for the subpage of each hotel
            hotel_link = hotel_card.find('div', class_='a5922b8ca1').a['href']

            #get the subpage of the hotel to scrap it
            hotel_page_source = requests.get(hotel_link).text
            with open('hotel_source_code.html', 'w') as f: 
                f.write(hotel_page_source)
            
            #sub_soup = BeautifulSoup(hotel_page_source, 'lxml')
            get_rooms(hotel_page_source)

            #save the data in the dictionary 
            hotels['title'].append(title)
            hotels['average_score'].append(average_score)
            hotels['grade'].append(grade)
            hotels['#reviewers'].append(reviewers)

            #print the data to check it 
            print(f'{title} \n{average_score}: {reviewers} --> {grade}\n\n')

    #print the number of hotels we found    
    print(f'{len(hotels["title"])}')
            

if __name__== '__main__':
     cities = {'cairo' : '290692',
               'alex': '290263'}
     pages = {'cairo' : 1, 'alex':1}
     print('Starting Scrapping......')

     for key in cities.keys():
          print(f'finding {pages[key]} page(s) of {key} hotels......')
          get_hotels(cities[key],pages[key])