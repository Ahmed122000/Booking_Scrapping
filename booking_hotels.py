import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



hotels = {} #dictionary to hold the hotels with their data 
def get_rooms(page_source):
    room_detail = {}
    page = BeautifulSoup(page_source, 'lxml')

    address = page.find('span', class_='hp_address_subtitle js-hp_address_subtitle jq_tooltip')
    room_detail['address'] = address.text if address != None else 'Unkown'
    
    imgs = []
    images = page.find_all('div', class_='bh-photo-grid-thumb-cell')
    for image in images:
        if(image.img != None):
            img_source = image.img['src']
            imgs.append(img_source)

    link_image = page.find_all('a', class_='bh-photo-grid-item bh-photo-grid-side-photo active-image')
    for url in link_image:
        if(url.img != None):
            url = url.img['src']
            imgs.append(url)

    link_image = page.find('a', class_='bh-photo-grid-item bh-photo-grid-photo1 active-image')
    if(link_image != None):
        link_image = link_image.img
        if(link_image != None):
            link_image = link_image['src']
            imgs.append(link_image)
    

    room_detail['images'] = imgs

    description = page.find('p', class_='a53cbfa6de b3efd73f69')
    room_detail['description'] = description.text if description != None else 'Unknown'

    aminty = page.find_all('span', class_='a5a5a75131')
    aminities = [x.text if x != None else 'Unknown' for x in aminty]
    room_detail['aminties'] = aminities


    rooms = page.find_all('div', class_='ed14448b9f b817090550 e7f103ee9e')
                                        
    room_detail['room_type'] = []
    room_detail['#individual'] = []
    room_detail['#bedrooms'] = []
    for room in rooms:
        if(room == None):
            continue
        if(room.a == None):
            continue
        room_type = room.a.span.text
        
        bedroom = room.find('span', class_='baf7cb1417')
        bedroom = 'Unknown' if bedroom is None else bedroom.text
        
        people = 'Unknown' if bedroom is 'Unknown' else bedroom.split()[0] 
        room_detail['room_type'].append(room_type)
        room_detail['#individual'].append(people)
        room_detail['#bedrooms'].append(bedroom)
         
    return room_detail

def get_hotels(country, city, city_code, page_numbers=1):

    for i in range(page_numbers):

        #page url(), we can update the code {&city} and number of page {&offset}
        url = f'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1FCAEiBWhvdGVsKIICOOgHSDNYA2hDiAEBmAEJuAEZyAEP2AEB6AEB-AENiAIBqAIDuAKZ7-2tBsACAdICJDQ5NDY3ZTNjLTZiYzMtNDFjNi05MGQ4LTk0NjAwNGNiZWRlY9gCBuACAQ&sid=0ca19a26ae77e73a83fd4cdc2f1ce287&aid=397594&city=-{city_code}&offset={i*25}'

        #open the driver and get the page
        driver = webdriver.Firefox()
        #print(f'opening the link: {url}')
        driver.get(url)

        try:
            # Wait for some time for dynamic content to load
            wait = WebDriverWait(driver, 30)

        except TimeoutException as e:
            print(f"TimeoutException: {e}")
            #open file to write the page HTML of the page in case of timeout
            #with open('source_code_exception.html', 'w') as f: 
            #    f.write(driver.page_source)
            #print(f"Page source at timeout: {driver.page_source}")


        #print the file after the try/exception end
        #print('save the file with no exception\n')
        #with open('source_code.html', 'w') as f: 
        #    f.write(driver.page_source)

        page_source = driver.page_source
        driver.quit() #close the driver
        print(f'finding hotels in page {i+1}......')
        
        #start scrapping
        soup = BeautifulSoup(page_source, 'lxml')
        #get the hotel card of each hotel 
        hotel_cards = soup.find_all('div', class_="c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4")
        
        #go through each card and check its info 
        for hotel_card in hotel_cards:
            hotel = {'city':city, 
                     'country':country, } #temp dictionary to hold the data of each hotel

            if(hotel_card == None):
                print('hotel_card == None')
                continue

            #get the title and create new entry to save the new hotel
            title = hotel_card.find('div', class_ = 'f6431b446c a15b38c233')
            if title != None:
                title = title.text
            else:
                continue


            #get hotel image source link
            img = hotel_card.find('img', class_='f9671d49b1')
            img_source = img['src'] if img != None else 'no_image_found'
           
            #get average score
            average_score = hotel_card.find('div', class_ ='a3b8729ab1 d86cee9b25')
            hotel['average_score'] = average_score.text if average_score != None else 'Unknown'
            
            #get the grade
            grade = hotel_card.find('div', class_='a3b8729ab1 e6208ee469 cb2cbb3ccb')
            hotel['grade'] = grade.text if grade != None else 'Unknown'

            #get number of reviewers
            reviewers = hotel_card.find('div', class_='abf093bdfe f45d8e4c32 d935416c47')
            hotel['#reviewers'] = reviewers.text if reviewers != None else 'Unknown'

            #get link for the subpage of each hotel
            hotel_link = hotel_card.find('div', class_='a5922b8ca1').a['href']

            #get the subpage of the hotel to scrap it
            hotel_page_source = requests.get(hotel_link).text
            #with open('hotel_source_code.html', 'w') as f: 
             #   f.write(hotel_page_source)
            
            #sub_soup = BeautifulSoup(hotel_page_source, 'lxml')
            room_details = get_rooms(hotel_page_source)

            #save the data in the dictionary 
            for key in room_details.keys():
                hotel[key] = room_details[key]

            hotels[title] = hotel
            #print the data to check it 
            #print(f'{title} \n{average_score}: {reviewers} --> {grade}\n\n')
        print(f'page {i+1} in {city}....done!') 
        print(f'{len(hotel_cards)} hotels are found')   
    #print the number of hotels we found    
    print(f'{len(hotels)} hotels are found until now!')
            

if __name__== '__main__':
    input_country = input('enter the city to get its hotels: \n> ')
    
    countries = {'egypt':
                 {'cairo' : '290692',
                  'alex': '290263',
                  'hurghada': '290029',
                  'sharm-el-sheikh':'302053',
                  'ain-sokhna': '900040497', 
                  'dahab': '293084',
                  'el-alamein':'289704',
                  'marsa-matruh': '298644',
                  'luxor':'290821',
                  'aswan':'291535'
                  }, 
                }
    
    pages = {'cairo' : 40,
             'alex': 19,
             'hurghada': 40,
             'sharm-el-sheikh': 16,
             'ain-sokhna': 9, 
             'dahab': 11,
             'el-alamein': 20,
             'marsa-matruh': 5,
             'luxor': 10,
             'aswan': 6
             }
    
    print('Starting Scrapping......')
    for city in countries[input_country]:
        try:
            print(f'finding {pages[city]} page(s) of {city} hotels......')
            get_hotels(input_country, city, countries[input_country][city],pages[city])
                # Save to a JSON file
            with open(f'{input_country}_{city}_hotels.json', 'w') as json_file:
                json.dump(hotels, json_file, indent=2)    
            print(f'\n\nthe total hotels found for now are: {len(hotels)}')
            hotels = {}

        except Exception as e:
            print('An error Occur...!!!')
            print('Saving the last result')
            with open(f'{input_country}_{city}_hotels.json', 'w') as json_file:
                json.dump(hotels, json_file, indent=2)    
            print(f'\n\nthe total hotels found for now are: {len(hotels)}')
            hotels = {}

