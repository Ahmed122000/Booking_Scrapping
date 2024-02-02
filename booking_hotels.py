import requests
import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#dictionary to hold the data of each hotel
hotels = {'title' : [], 
          'average_score' : [], 
          'grade': [], 
          '#reviewers':[]} 
#def get_hotels(country_code, page_numbers):
for i in range(3):
    #page url()
    url = f'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1FCAEiBWhvdGVsKIICOOgHSDNYA2hDiAEBmAEJuAEZyAEP2AEB6AEB-AENiAIBqAIDuAKZ7-2tBsACAdICJDQ5NDY3ZTNjLTZiYzMtNDFjNi05MGQ4LTk0NjAwNGNiZWRlY9gCBuACAQ&sid=0ca19a26ae77e73a83fd4cdc2f1ce287&aid=397594&city=-290692&offset={i*25}'

    #open the driver and get the page
    driver = webdriver.Firefox()
    driver.get(url)

    try:
        # Wait for some time for dynamic content to load
        wait = WebDriverWait(driver, 30)

    except TimeoutException as e:
        print(f"TimeoutException: {e}")
        #open the file to write the page HTML of the page in case of timeout
        with open('source_code_exception.html', 'w') as f: 
            f.write(driver.page_source)
        print(f"Page source at timeout: {driver.page_source}")


    #print the file after the try/exception end
    print('save the file out of try\n')
    with open('source_code.html', 'w') as f: 
            f.write(driver.page_source)

    page_source = driver.page_source
    driver.quit() #close the driver
    
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
        
        hotel_link = hotel_card.find('div', class_='a5922b8ca1').a['href']

        '''
        driver = webdriver.Firefox()
        driver.get(hotel_link)

        try:
            # Wait for some time for dynamic content to load
            wait = WebDriverWait(driver, 30)

        except TimeoutException as e:
            print(f"TimeoutException: {e}")
            #open the file to write the page HTML of the page in case of timeout
            with open('hotel_page__exception.html', 'w') as f: 
                f.write(driver.page_source)
            f.close() #close the file
        
        #print the file after the try/exception end
        print('save the hotel page correctly\n')
        with open('hotel_source_code.html', 'w') as f: 
            f.write(driver.page_source)

        hotel_page_source = driver.page_source
        f.close() #close the file
        driver.quit() #close the driver
        
        sub_soup = BeautifulSoup(hotel_page_source, 'lxml')
'''

        hotel_page_source = requests.get(hotel_link).text
        with open('hotel_source_code.html', 'w') as f: 
            f.write(hotel_page_source)
        
        sub_soup = BeautifulSoup(hotel_page_source, 'lxml')


        #save the data in the dictionary 
        hotels['title'].append(title)
        hotels['average_score'].append(average_score)
        hotels['grade'].append(grade)
        hotels['#reviewers'].append(reviewers)

        #print the data to check it 
        print(f'{title} \n{average_score}: {reviewers} --> {grade}\n\n')

#print the number of hotels we found    
print(len(hotels['title']))
        

#headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#    }

#'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1FCAEiBWhvdGVsKIICOOgHSDNYA2hDiAEBmAEJuAEZyAEP2AEB6AEB-AENiAIBqAIDuAKZ7-2tBsACAdICJDQ5NDY3ZTNjLTZiYzMtNDFjNi05MGQ4LTk0NjAwNGNiZWRlY9gCBuACAQ&sid=0ca19a26ae77e73a83fd4cdc2f1ce287&aid=397594&city=-290692'
#'https://www.booking.com/city/eg/cairo.en-gb.html?aid=397594&label=gog235jc-1BCAEiBWhvdGVsKIICOOgHSDNYA2hDiAEBmAEJuAEZyAEP2AEB6AEBiAIBqAIDuAKZ7-2tBsACAdICJDQ5NDY3ZTNjLTZiYzMtNDFjNi05MGQ4LTk0NjAwNGNiZWRlY9gCBeACAQ&sid=0ca19a26ae77e73a83fd4cdc2f1ce287'
#'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1FCAEiBWhvdGVsKIICOOgHSDNYA2hDiAEBmAEJuAEZyAEP2AEB6AEB-AENiAIBqAIDuAKZ7-2tBsACAdICJDQ5NDY3ZTNjLTZiYzMtNDFjNi05MGQ4LTk0NjAwNGNiZWRlY9gCBuACAQ&sid=0ca19a26ae77e73a83fd4cdc2f1ce287&aid=397594&city=-290692'
#'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1FCAEiBWhvdGVsKIICOOgHSDNYA2hDiAEBmAEJuAEZyAEP2AEB6AEB-AENiAIBqAIDuAKZ7-2tBsACAdICJDQ5NDY3ZTNjLTZiYzMtNDFjNi05MGQ4LTk0NjAwNGNiZWRlY9gCBuACAQ&sid=0ca19a26ae77e73a83fd4cdc2f1ce287&aid=397594&city=-290692&offset=25'
#'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1FCAEiBWhvdGVsKIICOOgHSDNYA2hDiAEBmAEJuAEZyAEP2AEB6AEB-AENiAIBqAIDuAKZ7-2tBsACAdICJDQ5NDY3ZTNjLTZiYzMtNDFjNi05MGQ4LTk0NjAwNGNiZWRlY9gCBuACAQ&sid=0ca19a26ae77e73a83fd4cdc2f1ce287&aid=397594&city=-290692&offset=50'
#'https://www.booking.com/searchresults.en-gb.html?label=New_English_EN_EG_26638726225-JVY46u8ezWpFK7e2iue9JwS217272691418%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi55519929396%3Atiaud-297601666475%3Adsa-300743127053%3Alp1005386%3Ali%3Adec%3Adm&sid=e70e5d967c68c41c15d237fa7a68b82c&aid=318615&city=-290263'
#page = requests.get('https://www.airbnb.com/', headers=headers).text
