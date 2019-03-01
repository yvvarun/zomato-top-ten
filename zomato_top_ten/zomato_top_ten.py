import sys
import traceback
import requests
import json
from prettytable import PrettyTable

class zomato:

    def __init__ (self, user_key):
        self.__base_url = "https://developers.zomato.com/api/v2.1/"
        if len(user_key) == 0:
            self.__user_key = "341dd3992c439c8eb7e9c2ba09eb8145"
        else:
            self.__user_key = user_key
        """
        key: user selected option
        value: actual title as returned by collections api of zomato
        """
        self.__collection_dict = {1:"Best Bars & Pubs", 2:"Microbreweries",\
                                3:"Trending this week", 4:"Pizza Time",\
                                5:"Great Breakfasts", 6:"Luxury Dining",\
                                7:"Sweet Tooth"}
        self.__table = PrettyTable()

    def __check_response_status (self, response):
        ret = 0
        status_code = response.status_code
        if status_code == 200:
            return 0
        elif status_code == 400:
            return -1
        elif status_code == 403:
            print('invalid user key: %s'%self.__user_key)
            return -1

    def __get_json_res(self, query):
        headers = {'Accept': 'application/json', 'user-key': self.__user_key}
        r = requests.get(self.__base_url + query, headers=headers)
        status = self.__check_response_status(r)
        if status == 0:
            res = json.loads(r.content.decode("utf-8"))
            return res
        else:
            return -1

    def __populate_table (self, res, city_name):
        self.__table.field_names = ["Restaurant name", "Rating", "Votes"]
        for r in res['restaurants']:
            name = r['restaurant']['name']
            location = r['restaurant']['location']['locality_verbose']
            if location.endswith(city_name.title()):
                location = location[:-len(city_name)]
                location = location.rstrip(', ')
            rating = r['restaurant']['user_rating']['aggregate_rating']
            votes = r['restaurant']['user_rating']['votes']
            self.__table.add_row([name + ", " + location, rating, votes])
        self.__table.sortby = "Rating"
        self.__table.reversesort = True

    def get_city_id (self, city_name):
        """
        takes city name as input.
        returns: city_id for city_name if found.
                 -1 on failure.
        """
        try:
            city_id = -1
            query = "cities?q={city_name}".format(city_name=city_name)
            res = self.__get_json_res(query)
            if res != -1:
                if len(res['location_suggestions']) > 0:
                    for location in res['location_suggestions']:
                        if location['country_name'] == 'India':
                            city_id = location['id']
                            break
                else:
                    print('invalid city name: %s'%city_name)
                    return -1
            else:
                return -1
            return city_id
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Exception traceback: %s"%str(traceback.format_exception\
                (exc_type, exc_value, exc_traceback)))

    def get_collection_id (self, city_name, collection_option):
        """
        takes city name and collection option as input.
        returns: collection_id of a selected collection option in a city.
                 -1 on failure.
        """
        try:
            city_id = self.get_city_id(city_name)
            collection_id = -1
            query = "collections?city_id={city_id}".format(city_id=city_id)
            res = self.__get_json_res(query)
            if res != -1:
                if len(res['collections']) > 0:
                    for c in res['collections']:
                        if c['collection']['title'].title() == \
                           self.__collection_dict[collection_option].title():
                            collection_id = c['collection']['collection_id']
                else:
                    print('invalid collection option: %d'%collection_option)
            else:
                return -1
            return collection_id
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Exception traceback: %s"%str(traceback.format_exception\
                (exc_type, exc_value, exc_traceback)))

    def get_top_ten_list (self, city_name, collection_option):
        """
        takes city name and collection option as input.
        displays table of top 10 list in a tabular format.
        returns: 0 on success.
                 -1 on failure
        """
        try:
            city_id = self.get_city_id(city_name)
            collection_id = self.get_collection_id(city_name, collection_option)
            query = "search?entity_id={entity_id}&entity_type=city&"\
                    "count=100&collection_id={collection_id}&"\
		    "sort=rating&order=desc"\
                    .format(entity_id=city_id,
		    collection_id=collection_id)
            res = self.__get_json_res(query)
            if res != -1:
                if len(res['restaurants']) > 0:
                    self.__populate_table(res, city_name)
                    """
                    if collection_option is "Bars/Pubs", include Microbreweries as well
                    to the search
                    """
                    if collection_option == 1:
                        collection_id = self.get_collection_id(city_name, 2)
                        query = "search?entity_id={entity_id}&entity_type=city&"\
                                "count=100&collection_id={collection_id}&"\
				"sort=rating&order=desc"\
                                .format(entity_id=city_id,
				collection_id=collection_id)
                        res = self.__get_json_res(query)
                        if res != -1:
                            if len(res['restaurants']) > 0:
                                self.__populate_table(res, city_name)
                    print(self.__table.get_string(start=0,end=10))
                    return 0
            else:
                return -1
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Exception traceback: %s"%str(traceback.format_exception\
                (exc_type, exc_value, exc_traceback)))

def main():
    try:
        user_key = input("Enter user key (Press Enter to use owner's key): ")
        city_name = input("Enter city: ")
        collection_option = int(input("Get top 10 restaurants for: \n"\
                               "1. Bars/Pubs \n"\
                               "2. Microbreweries \n"\
                               "3. Trending restaurants \n"\
                               "4. Pizza restaurants \n"\
                               "5. Breakfasts \n"\
                               "6. Luxury Dining \n"\
                               "7. Desserts \n"))

        z = zomato(user_key)
        z.get_top_ten_list(city_name, collection_option)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("Exception traceback: %s"%str(traceback.format_exception\
                (exc_type, exc_value, exc_traceback)))


if __name__ == "__main__":
    main()
