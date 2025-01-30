from flask import Flask, request, jsonify, send_from_directory
from booking_hotels import Scraper
import json
import os
import time

app = Flask(__name__)
scraper = Scraper()

@app.route("/codes", methods=['GET'])
def get_codes():
    codes = {'cairo' : '290692',
            'alexandria': '290263',
            'hurghada': '290029',
            'sharm-el-sheikh':'302053',
            'ain-sokhna': '900040497', 
            'dahab': '293084',
            'el-alamein':'289704',
            'marsa-matruh': '298644',
            'luxor':'290821',
            'aswan':'291535'
            }
    return jsonify(codes), 200

@app.route("/scrape", methods=['GET'])
def get_data():
    city = request.args.get('city')
    city_code = request.args.get("city_code")
    pages= request.args.get('pages', 1,type=int)
    format = request.args.get('format', "json")

    if not city or not city_code: 
        return jsonify({"error": "City and City_code are required"}), 400
    try:
        hotels = scraper.get_hotels(city, city_code, pages)
    except Exception as e:
        return json({"error": f"An error occurred during scraping: {e}"}), 500
    
    
    if format == "file":
        filename= f"{city}_hotels_{int(time.time())}.json"  
        filepath=os.path.join(os.getcwd(), filename)

        try:
            with open(filepath, 'w') as json_file:
                json.dump(hotels, json_file, indent=2)  
        except Exception as e: 
            return jsonify({"error": f"failed to save file: {e}"}), 500  
        return jsonify({"message": f"Scraping for {city} completed. Data saved", 
                        "download_link": f"http://localhost:5000/download/{filename}"}), 200

    else: 
        return jsonify(hotels), 200
    

@app.route("/download/<file_name>", methods=['GET'])
def download(file_name):
    file_path= os.path.join(os.getcwd(), file_name)
    if not os.path.exists(file_path):
        return jsonify({"error": "file not found"}), 404
    
    return send_from_directory(os.getcwd(), file_name, as_attachment=True)



if __name__=="__main__": 
    app.run(debug=True)