import requests
import json




def initialize_app(config):
    return Zomato(config)

class Zomato:
    def __init__(self, config):
        self.user_key = config["user_key"]

    def get_restaurants(self,location,cuisine):
        url = "https://developers.zomato.com/api/v2.1/search?q="+location+"&cuisine="+cuisine

        payload={}
        headers = {
            'user-key': 'dc4f13f34b2754f1b044d01e36008001',
            'Cookie': 'csrf=b3c5188f45f433d03da50059e1ea637d; fbcity=8; fbtrack=c1b86171035181312075634f320418d8; zl=en; AWSALBTG=K0Dkp7mfAF+8yKm+LmaveFqlIR9Ujt6+LmHxXwdf+HKlwi9IcOf6O9I680hIYlOn0WkJO5H//6oSoxibsFtZrdByy837OBiK9SASWXIYSBOwfmQRMeeY3pRu6pYWErEFkwRXo5u29zKu5oJ6NFYkGxT7EkqEncGJMc0PsonAoi7Pg7EpFQ4=; AWSALBTGCORS=K0Dkp7mfAF+8yKm+LmaveFqlIR9Ujt6+LmHxXwdf+HKlwi9IcOf6O9I680hIYlOn0WkJO5H//6oSoxibsFtZrdByy837OBiK9SASWXIYSBOwfmQRMeeY3pRu6pYWErEFkwRXo5u29zKu5oJ6NFYkGxT7EkqEncGJMc0PsonAoi7Pg7EpFQ4='
            }

        response = requests.request("GET", url, headers=headers, data=payload)
        result=response.json();
        restaurant=result["restaurants"]
        restaurants=[]
        for i in restaurant:
            if((i["restaurant"]["location"]["locality"]==location|(i["restaurant"]["location"]["city"]==location))&(i["restaurant"]["cuisines"]==cuisine)):
                restaurants.append(i["restaurant"]["name"])
        return restaurants
    
    
    def restaurant_search(self, query="", latitude="", longitude="", cuisines="", limit=5):
        """
        Takes either query, latitude and longitude or cuisine as input.
        Returns a list of Restaurant IDs.
        """
        cuisines = "%2C".join(cuisines.split(","))
        if str(limit).isalpha() == True:
            raise ValueError('LimitNotInteger')
        #base_url + "search?q=" + str(query) + "&count=" + str(limit) + "&cuisines=" + str(cuisines), headers=headers).content).decode("utf-8")
        url = "https://developers.zomato.com/api/v2.1/search?q="+str(query)+"&cuisine="+cuisines+"&lat="+str(latitude)+"&lon="+str(longitude)

        payload={}
        headers = {
        'user-key': 'dc4f13f34b2754f1b044d01e36008001',
        'Cookie': 'csrf=5af7fcea928d8858ace32a70afc64c5f; fbcity=11585; fbtrack=c1b86171035181312075634f320418d8; zl=en; AWSALBTG=MGSFonO4IpCWUAb7e8VB03zpqMzceIxCkulWkEpEOkVGJ5UB5KxrbNA3hPUW+pXX5QW2nA2Hy2tlpkVBCLapcbIqZlF8Fu3pl4t87s3dOa13GzqaiV5FCN40PLn5nFArEcN7IYDoNS6EjQYrUMIp3gdUiFnlKwAjErsR9HzHR7G4m8ixFkA=; AWSALBTGCORS=MGSFonO4IpCWUAb7e8VB03zpqMzceIxCkulWkEpEOkVGJ5UB5KxrbNA3hPUW+pXX5QW2nA2Hy2tlpkVBCLapcbIqZlF8Fu3pl4t87s3dOa13GzqaiV5FCN40PLn5nFArEcN7IYDoNS6EjQYrUMIp3gdUiFnlKwAjErsR9HzHR7G4m8ixFkA='
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        result=response.json()
        return result
        
#get_restaurants("Madhurawada","Biryani")               

    def get_cuisines(self,cityid):
        """
        Takes City ID as input.
        Returns a sorted dictionary of all cuisine IDs and their respective cuisine names.
        """
        
        url="https://developers.zomato.com/api/v2.1/cuisines?city_id="+str(cityid)
        payload={}
        headers = {
            'user-key': 'dc4f13f34b2754f1b044d01e36008001',
            'Cookie': 'csrf=e482bc19b50efa20d8bd00013213bc7f; fbcity=11585; fbtrack=c1b86171035181312075634f320418d8; zl=en; AWSALBTG=gwgonUm+4a3koc/epVdb8Ue4n5BjsRc9ZQm9B5EgYRhFPjqCBYA8OephWZVKLVCFe1L2LXhogVY5ZnfPRqdFRl82VhD0ID+WRGlPA3vahNdmHjP7HMZMOWCRBWFodGSBqYDvxGIC+8dfKOY0BDD6b8g7rkkvFyWAz7O460UmszO2UzC+Pfo=; AWSALBTGCORS=gwgonUm+4a3koc/epVdb8Ue4n5BjsRc9ZQm9B5EgYRhFPjqCBYA8OephWZVKLVCFe1L2LXhogVY5ZnfPRqdFRl82VhD0ID+WRGlPA3vahNdmHjP7HMZMOWCRBWFodGSBqYDvxGIC+8dfKOY0BDD6b8g7rkkvFyWAz7O460UmszO2UzC+Pfo='
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        result=response.json();
        #restaurant=result["restaurants"]
        if len(result['cuisines']) == 0:
            raise ValueError('InvalidCityId')
        temp_cuisines = {}
        cuisines = {}
        for cuisine in result['cuisines']:
            temp_cuisines.update({cuisine['cuisine']['cuisine_id'] : cuisine['cuisine']['cuisine_name']})

        for cuisine in sorted(temp_cuisines):
            cuisines.update({cuisine : temp_cuisines[cuisine]})

        return cuisines
        
    def get_location(self, query="", limit=5):
        
        """
        Takes either query, latitude and longitude or cuisine as input.
        Returns a list of Restaurant IDs.
        """
        if str(limit).isalpha() == True:
            raise ValueError('LimitNotInteger')
        url = "https://developers.zomato.com/api/v2.1/locations?query="+query+"&count="+str(limit)

        payload={}
        headers = {
        'user-key': 'dc4f13f34b2754f1b044d01e36008001',
        'Cookie': 'csrf=db4a393b2e5be21719d5182e0f4d6cb5; fbcity=11585; fbtrack=c1b86171035181312075634f320418d8; zl=en; AWSALBTG=iHMiSOI0EilRZFvh9gCYJHk0Ekfpdc4ew7BROlQ1xOy/mKpZ4uIK6OrwvjbR3LaNjkMjoPMquwF8QmuOP8ZtJ7UqR0IeQG4p2n4hCp231qMFrwTonY9EKZWtAjNdzmL9byXQ5PFzVtgqcA8fWtGz4ivn825DKZ4P0JzHR8vfNDPCascl+2k=; AWSALBTGCORS=iHMiSOI0EilRZFvh9gCYJHk0Ekfpdc4ew7BROlQ1xOy/mKpZ4uIK6OrwvjbR3LaNjkMjoPMquwF8QmuOP8ZtJ7UqR0IeQG4p2n4hCp231qMFrwTonY9EKZWtAjNdzmL9byXQ5PFzVtgqcA8fWtGz4ivn825DKZ4P0JzHR8vfNDPCascl+2k='
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        result=response.json();       
        return result
