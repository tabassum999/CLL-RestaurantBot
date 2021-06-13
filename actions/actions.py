# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
from actions.cuisine_restaurant import Restaurant_list
from rasa_core_sdk.events import SlotSet
import requests
from actions import test
import json
import pandas as pd


#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
class ActionCustomCuisine(Action):
    
    def name(self) -> Text:
        return "action_custom_cuisine"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.get_slot("cuisine"))
        print(tracker.get_intent_of_latest_message())
        # print(tracker.events_after_of_latest_restart())
        entity= tracker.get_slot("cuisine")
        if entity not in Restaurant_list.keys():
            dispatcher.utter_message(response="utter_sorry_cuisine")
            return [SlotSet("cuisine",None)]
        else:
            restaurants=Restaurant_list[entity]
            dispatcher.utter_message(text=f"Let me find some restaurants for {entity} cuisine for you")
            return [SlotSet("restaurants",restaurants)]
        
class ActionFindRestaurants(Action):
    def name(self) -> Text:
        return "action_find_restaurants"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        restaurants= tracker.get_slot("restaurants")
        restaurants=",".join(restaurants)
        dispatcher.utter_message(f"These are the restaurants I found {restaurants}")
        
        return [SlotSet("cuisine",None)]


    
class ActionSearchRestaurants(Action):
  def name(self):
    return 'action_search_restaurants'
    
  def run(self, dispatcher, tracker, domain):
    config={ "user_key":"dc4f13f34b2754f1b044d01e36008001"}
    found_restaurants=True
    zomato = test.initialize_app(config)
    loc = tracker.get_slot('location')
    cuisine = tracker.get_slot('cuisine')
    location_detail=zomato.get_location(loc, 1)
    d1 = json.loads(location_detail)
    lat=d1["location_suggestions"][0]["latitude"]
    lon=d1["location_suggestions"][0]["longitude"]
    #cuisines_dict={'american':1,'mexican':73,'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85}
    cuisines_dict=zomato.get_cuisines(d1["location_suggestions"][0]["city_id"])
    results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 50) ## get a list of 50 restaurants then filter top 5 by budget
    d = json.loads(results)
    ## WHen API limits exceeded
    if d['results_found'] == 0:
        response= "no results"
        dispatcher.utter_message("Sorry, We couldn't find any "+str(cuisine)+" restaurants in "+str(loc)+".")
        found_restaurants=False

    else:
        r_data=[]
        for i,r in enumerate(d["restaurants"]):
            r_l=[]
            r_l.append(r['restaurant']['id'])
            r_l.append(r['restaurant']['name'])
            r_l.append(float(r['restaurant']['user_rating']['aggregate_rating']))
            r_l.append(r['restaurant']['location']['address'])
            r_data.append(r_l)
        df=pd.DataFrame(data=r_data,columns=["ID","Name","Rating","Address"])
        df.set_index('ID', inplace=True)
        df=df.sort_values('Rating',ascending=False)
        if(len(df.Name)>=5):
            response="Top 5 "+str(cuisine)+" restaurants near "+str(loc)+" are: \n"
            for i in range(5):
                response+=str(i+1)+" "+df.Name[i]+" in "+df.Address[i]+" has been rated "+str(df.Rating[i])+" \n"
        elif(len(df.Name)>0 and len(df.Name)<5):  # Couldn't find 5 restaurants
            response="Sorry we could not find enough restaurants with given details \n"
            response+="Top "+str(len(df.Name))+" "+str(cuisine)+" restaurants near "+str(loc).rstrip()+" are: \n"
            for i in range(len(df.Name)):
                response+=str(i+1)+" "+df.Name[i]+" in "+df.Address[i]+" has been rated "+str(df.Rating[i])+" \n"
        else:
            response="Sorry, We couldn't find any restaurants matching your requirements."
            found_restaurants=False
        # except:
        #   dispatcher.utter_message("Sorry, We couldn't find any "+str(cuisine)+" restaurants in "+str(loc)+".")
        #   found_restaurants=False
        dispatcher.utter_message(response)
        return [SlotSet('found_restaurants',found_restaurants)]
       # dispatcher.utter_message(text="Hello World!")

        # return []


