# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import ActionReverted
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted
import random
import re
import requests
import configparser
import logging
# url

import json
import datetime

INTENT_DESCRIPTION_MAPPING_PATH = "actions/intent_description_mapping.csv"

class FlightForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self):
        return "flight_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "fromloc_city",
            "toloc_city",
            "depart_time",
        ]

    @staticmethod
    def fromloc_city_db() -> List[Text]:
        """Database of supported cuisines"""
        dbList = []
        with open("ticket.json") as f:
            data = json.loads(f.read())
            for item in data:
                if item['From'].upper() not in dbList:
                    dbList.append(item['From'].upper())
        return dbList

    @staticmethod
    def toloc_city_db() -> List[Text]:
        """Database of supported cuisines"""
        dbList = []
        with open("ticket.json") as f:
            data = json.loads(f.read())
            for item in data:
                if item['To'].upper() not in dbList:
                    dbList.append(item['To'].upper())
        # print(dbList)
        return dbList
        # return ["hong kong", "macau", "tokyo", "seoul", "new york", "seattle", "london", "paris", "berlin", "taipei", "singapore", "beijing"]


    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        fromcity = tracker.get_slot('fromloc_city')
        tocity = tracker.get_slot('toloc_city')
        time = tracker.get_slot('depart_time')
        if type(time) == dict:
            time1 = time["from"].split(".")[0].replace("T", " ")
            time1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')

            time2 = time["to"].split(".")[0].replace("T", " ")
            time2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')

            # dispatcher.utter_message("between {}  and {} .".format(time1, time2))
        elif type(time) == str:
            time1 = time.split(".")[0].replace("T", " ")
            time1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
            # dispatcher.utter_message("at {} ".format(time1))
            time2 = time1 + datetime.timedelta(days=2)
            time1 = time1 + datetime.timedelta(days=-1)
            # dispatcher.utter_message("at {} {} ".format(time1, time2))
        dispatcher.utter_message("Ok. Search the flight tickets from {} to {} between {} and {}.".format(fromcity, tocity, time1, time2))
        # myFormat = "{:<10} \t{:<10} \t{:<20} \t{:<10} \t{:<10} \t{:<20} \t{:<10}"
        # list1 = [myFormat.format("From", "To", "Airlines", "Seats", "Flight No", "Date", "Price")]
        list1 = []
        with open("ticket.json") as f:
            data = json.loads(f.read())
            for item in data:
                item_date = datetime.datetime.strptime(item["Date"], '%Y-%m-%d %H:%M:%S')
                if item['From'].upper() == fromcity.upper() and \
                        item['To'].upper() == tocity.upper() and \
                        time1 <= item_date <= time2:
                    list1.append(
                        "Flight : "+item['Flight No'] +
                        "  \nFrom-To : "+item['From']+" - "+item['To'] +
                        "  \nAirline : "+item['Airlines'] +
                        "  \nDate : "+item['Date'] +
                        "  \nPrice :"+item['Price']
                        # myFormat.format(item['From'], item['To'], item['Airlines'], str(item['Seats']), item['Flight No'], item['Date'],  item['Price'])
                    )
        if len(list1) > 1:
            flights_list = ""
            for i in range(len(list1)):
                flights_list += (list1[i]+"\n\n")
            dispatcher.utter_message(flights_list)
            return [FollowupAction("booking_form")]
        else:
            dispatcher.utter_message("Sorry! There are no flights available.")
            return [FollowupAction("action_research")]



    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "fromloc_city": [
                self.from_entity(intent=["inform", "book_flight", "city"], entity="city", role="fromloc.city_name"),
                self.from_text(intent="city"),
                self.from_intent(intent="affirm", value="chitchat"),
            ],
            "toloc_city": [
                self.from_entity(intent=["inform", "book_flight", "city"], entity="city", role="toloc.city_name"),
                self.from_text(intent="city"),
                self.from_intent(intent="affirm", value="chitchat"),
            ],
            "depart_time": [
                self.from_entity(entity="time"),
                self.from_intent(intent="affirm", value="chitchat"),
            ]
        }

    def validate_fromloc_city(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"fromloc_city": None}
        if type(value) == list:
            value = value[0]
        value = value.upper()
        if value == tracker.get_slot('toloc_city'):
            dispatcher.utter_message("Your DEPARTURE and DESTINATION cannot be the same.")
            return {"fromloc_city": None}
        elif value in self.fromloc_city_db():
            # validation succeeded, set the value of the "fromloc_city" slot to value
            dispatcher.utter_message("You will depart from "+value)
            return {"fromloc_city": value}
        else:
            dispatcher.utter_message(template="utter_wrong_fromloc_city")
            db = "CITY:"
            for city in self.fromloc_city_db():
                db += ("\n- ✈" + city.upper())
            dispatcher.utter_message(db)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"fromloc_city": None}


    def validate_toloc_city(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"toloc_city": None}
        if type(value) == list:
            value = value[0]
        value = value.upper()
        if value == tracker.get_slot('fromloc_city'):
            dispatcher.utter_message("Your DEPARTURE and DESTINATION cannot be the same.")
            return {"toloc_city": None}
        elif value in self.toloc_city_db():
            # validation succeeded, set the value of the "toloc_city" slot to value
            dispatcher.utter_message("Your destination is " + value)
            return {"toloc_city": value}
        else:
            dispatcher.utter_message(template="utter_wrong_toloc_city")
            db = "CITY:"
            for city in self.toloc_city_db():
               db += ("\n- ✈"+city.upper())
            dispatcher.utter_message(db)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"toloc_city": None}

    def validate_depart_time(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"depart_time": None}
        if (type(value) == dict or (type(value) == str) and re.match('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}\+\d{2}:\d{2}',value) is not None):
            dispatcher.utter_message("Departure time is "+str(value))
            return {"depart_time": value}
        elif 'at night' in value:
            dispatcher.utter_message('at night')
            return {"depart_time": None} # 待修改
        else:
            return {"depart_time": None}

class BookingForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self):
        return "booking_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "flight_no",
            "class_type",
            "seat_type",
            "user_name",
            "passport_no",
            "email",
        ]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        flight_no = tracker.get_slot("flight_no")
        class_type = tracker.get_slot("class_type")
        seat_type = tracker.get_slot("seat_type")
        seat_title = ["W", "A"]
        if seat_type == "window seat":
            seat_title = seat_title[0]
        elif seat_type == "aisle seat":
            seat_title = seat_title[1]
        else:
            seat_title = seat_title[random.randint(0, 1)]
        user_name = tracker.get_slot("user_name")
        passport_no = tracker.get_slot("passport_no")
        email = tracker.get_slot("email")
        with open("ticket.json") as f:
            data = json.loads(f.read())
            # myFormat = "{:<10} {:<10} {:<20} {:<10} {:<10} {:<20} {:<10}"
            # list1 = [myFormat.format("From", "To", "Airlines", "Seats No.", "Flight No.", "Date", "Price")]
            list1 = []
            for item in data:
                if item["Flight No"].upper() == flight_no.upper() and \
                        item['From'].upper() == tracker.get_slot("fromloc_city") and \
                        item['To'].upper() == tracker.get_slot("toloc_city"):
                    Flight_No = item['Flight No']
                    From = item['From']
                    To = item['To']
                    Airline = item['Airlines']
                    Date = item['Date']
                    Seat = seat_title+str(random.randint(0, int(item['Seats'])))
                    Price = item['Price']
                    list1.append(
                        "Flight : " + Flight_No +
                        "  \nFrom - To : " + From + " - " + To +
                        "  \nAirline : " + Airline +
                        "  \nDate : " + Date +
                        "  \nSeat : " + Seat +
                        "  \nPrice : " + Price
                    )
                    # list1.append(myFormat.format(item['From'], item['To'], item['Airlines'], seat_title+str(random.randint(0, int(item['Seats']))), item['Flight No'], item['Date'], item['Price']))
        if len(list1) > 0:
            dispatcher.utter_message("Well, I have you booked on a flight that will fit your schedule. The tickets will arrive by mail in a few days.")
            dispatcher.utter_message("Here is your flight ticket information.")
            ticket = ""
            for i in range(len(list1)):
                ticket += (list1[i])
            ticket += "  \nName: {}  \nClass: {}  \nPassport No.: {}".format(str(user_name).upper(), str(class_type).upper(), str(passport_no))
            dispatcher.utter_message(ticket)
        else:
            dispatcher.utter_message("Sorry! There are no flights available...\n\nPlease check the Flight No.")
            return [ActionReverted(), SlotSet("flight_no", None)]

        # dispatcher.utter_message("NAME: {}  \nCLASS: {}  \nPassport No.: {}".format(str(user_name).upper(), str(class_type).upper()), str(passport_no))

        dispatcher.utter_message(template="utter_precautions_for_boarding")
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "flight_no": [
                self.from_entity(entity="flight_no"),
                self.from_text(intent="enter_data"),
                self.from_intent(intent="affirm", value="chitchat"),

            ],
            "class_type": [
                self.from_entity(intent=["enter_data", "book_flight", "city"], entity="class_type"),
                self.from_intent(intent="affirm", value="chitchat"),
            ],
            "seat_type": [
                self.from_entity(intent="enter_data", entity="seat_type"),
                self.from_intent(intent="deny", value="not specify"),
                self.from_intent(intent="affirm", value="chitchat"),
            ],
            "user_name": [
                self.from_entity(entity="name", role="english_full_name"),
                self.from_entity(entity="name"),
                self.from_text(intent="enter_data"),
                self.from_text(intent="city"),
                self.from_intent(intent="affirm", value="chitchat"),
                #self.from_text() ##
            ],
            "passport_no": [
                self.from_entity(entity="passport_no"),
                #self.from_entity(entity="phone-number"),
                self.from_text(intent="enter_data"),
                self.from_intent(intent="affirm", value="chitchat"),
            ],
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="enter_data"),
                self.from_intent(intent="affirm", value="chitchat"),
            ]
        }
    def validate_flight_no(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"flight_no": None}
        value = str(value).strip().upper()
        value2 = None
        if re.search("[a-zA-Z]{2,5}\d{2,3}", value) is not None:
            value2 = re.search("[a-zA-Z]{2,5}\d{2,3}", value).group()
        with open("ticket.json") as f:
            data = json.loads(f.read())
            for item in data:
                if value == str(item["Flight No"]).upper():
                    # validation succeeded, set the value of the "flight_no" slot to value
                    dispatcher.utter_message("OK. The flight "+value+" is available")
                    return {"flight_no": value}
                elif value2 == str(item["Flight No"]).upper():
                    dispatcher.utter_message("OK. The flight " + value2 + " is available")
                    return {"flight_no": value2}
        dispatcher.utter_message(template="utter_wrong_flight_no")
        # validation failed, set this slot to None, meaning the
        # user will be asked for the slot again
        return {"flight_no": None}

    def validate_class_type(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"class_type": None}
        else:
            return {"class_type": value}

    def validate_seat_type(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"seat_type": None}
        else:
            return {"seat_type": value}

    def validate_passport_no(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"passport_no": None}
        value = str(value).upper()
        if re.match("^[a-zA-Z0-9]{5,17}$", value) is not None:
            dispatcher.utter_message("OK. Your Passport No. is "+value)
            return {"passport_no": value}
        elif re.search("[a-zA-Z]{0,2}\d{5,17}", value) is not None:
            value = re.search("[a-zA-Z]{0,2}\d{5,17}", value).group()
            if re.match("^[a-zA-Z]{0,2}\d{5,17}$", value) is not None:
                dispatcher.utter_message("OK. Your Passport No. is " + value)
                return {"passport_no": value}
        else:
            dispatcher.utter_message(template="utter_wrong_passport_no")
            dispatcher.utter_message("Passport No. is usually located on the same page as the person's photograph in your passport. [see more...](https://en.wikipedia.org/wiki/Passport)  \n  \nExample:  \n- ✔ A123456789  \n- ✔ DE9876543")
            return {"passport_no": None}

    def validate_user_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"user_name": None}
        value = str(value).upper()
        if re.match("^[a-zA-Z]+(\s[a-zA-Z])*(\s?,\s?|\s)[a-zA-Z]+(\s?-\s?[a-zA-Z]+)*$", value) is not None:
            dispatcher.utter_message("OK. Your English full name is "+value)
            return {"user_name": value}
        else:
            dispatcher.utter_message(template="utter_wrong_user_name")
            dispatcher.utter_message("You can refer to the following examples:  \n- ✔ WANG,XIO-MIN (Last name,First name)  \n- ✔ Johnny Depp(First name Last name)  \n- ✔ Leonardo DiCaprio(First name Last name)")
            return {"user_name": None}

    def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if str(value) == "chitchat":
            dispatcher.utter_message(template="utter_chitchat")
            return {"email": None}
        value = str(value).strip()
        if re.match("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+([.]\w{2,3})+$", value):
            dispatcher.utter_message("OK. Your Email Address is "+value)
            return {"email": value}
        else:
            dispatcher.utter_message(template="utter_wrong_email")
            return {"email": None}


class ActionGreet(Action):
    """"Revertible mapped action for utter_greet"""
    def name(self):
        return 'action_greet'

    def run(self, dispatcher, tracker, domain):
        name = next(tracker.get_latest_entity_values("name"), None)
        if tracker.get_slot("user_name") is not None:
            dispatcher.utter_message(template="utter_user_greet")
        elif name is not None:
            name = str(name).upper()
            dispatcher.utter_message("Hello~ "+name)
            if re.match("^[a-zA-Z]+(\s[a-zA-Z])*(\s?,\s?|\s)[a-zA-Z]+(\s?-\s?[a-zA-Z]+)*$", name) is not None:
                return [UserUtteranceReverted(), ActionReverted(), SlotSet("user_name", name)]
        else:
            dispatcher.utter_message(template="utter_greet")
            return [UserUtteranceReverted(), ActionReverted()]

class ActionGoodbye(Action):
    """"Revertible mapped action for utter_goodbye"""
    def name(self):
        return 'action_goodbye'

    def run(self, dispatcher, tracker, domain):
        if (tracker.get_slot("user_name") is not None):
            dispatcher.utter_message(template="utter_user_goodbye")
        else:
            dispatcher.utter_message(template="utter_goodbye")
        return [Restarted()]

class ActionThankYou(Action):
    """"Revertible mapped action for utter_greet"""
    def name(self):
        return 'action_thankyou'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_noworries")
        dispatcher.utter_message(template="utter_mood_greet")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionMoodGreat(Action):
    """"Revertible mapped action for utter_greet"""
    def name(self):
        return 'action_mood_great'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_mood_greet")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionMoodUnhappy(Action):
    """"Revertible mapped action for utter_greet"""
    def name(self):
        return 'action_mood_unhappy'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_mood_unhappy")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionOutOfScope(Action):
    """"Revertible mapped action for utter_out_of_scope"""

    def name(self):
        return "action_out_of_scope"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_out_of_scope")
        dispatcher.utter_message(template="utter_explain_whatspossible")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionChitchat(Action):
    """"Revertible mapped action for utter_is_bot"""

    def name(self):
        return "action_chitchat"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_chitchat")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionResponseInsult(Action):
    """"Revertible mapped action for utter_is_bot"""

    def name(self):
        return "action_response_insult"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_respond_insult")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionIsBot(Action):
    """"Revertible mapped action for utter_is_bot"""

    def name(self):
        return "action_is_bot"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_iamabot")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionExplain(Action):
    """"Revertible mapped action for utter_goodbye"""
    def name(self):
        return 'action_explain_why'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_explain_why")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionIntoduction(Action):
    """"Revertible mapped action for utter_goodbye"""
    def name(self):
        return 'action_intro'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_iamabot")
        dispatcher.utter_message(template="utter_explain_whatspossible")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionGetStart(Action):

    def name(self):
        return "action_get_start"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_get_start")
        return [FollowupAction("flight_form")]

class ActionResearch(Action):

    def name(self):
        return "action_research"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_research")
        return [FollowupAction("action_reset_flight_form")]

class ActionStop(Action):
    """"Revertible mapped action for utter_goodbye"""
    def name(self):
        return 'action_stop'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_research_restart_continue_goback_with_button")
        return [UserUtteranceReverted()]

class ActionContinue(Action):
    """"Revertible mapped action for utter_goodbye"""
    def name(self):
        return 'action_continue'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_continue")
        return [UserUtteranceReverted(), ActionReverted()]

class ActionGoBack(Action):
    """"Revertible mapped action for utter_goodbye"""
    def name(self):
        return 'action_goback'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_goback")
        return [UserUtteranceReverted(), UserUtteranceReverted(), ActionReverted()]

class ActionResetFlightForm(Action):
    """"Revertible mapped action for utter_goodbye"""
    def name(self):
        return 'action_reset_flight_form'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("fromloc_city", None), SlotSet("toloc_city", None), SlotSet("depart_time", None), FollowupAction("flight_form")]

class myReverted(Action):
    """"Revertible mapped action for utter_goodbye"""
    def name(self):
        return 'action_reverted'

    def run(self, dispatcher, tracker, domain):
        return [UserUtteranceReverted(), ActionReverted()]

class WeatherForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self):
        return "weather_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "weather_city",
        ]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        dispatcher.utter_message("I will provide the "+str(tracker.get_slot("weather_city")).upper()+" weather forecast for the next 5 days")
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"

        querystring = {"q": tracker.get_slot('weather_city')}

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "6907d22d7amshbe256fd9bf5d738p10bc28jsna0b8b41587f9"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()
        if data['cod'] == '200':
            cnt = 0
            total = 0
            list = []
            for i in range(5):
                l = []
                l.append(data['list'][cnt]['dt_txt'].split(" ")[0])
                for j in range(8):
                    total += int(data['list'][cnt]['main']['temp']) - 273.15
                    cnt += 1
                total = int(total / 8)
                l.append("Temp. : " + str(total)+"°C")
                total = 0
                list.append(l)
                l.append(str(data['list'][i]['weather'][0]['description']).title())
                dispatcher.utter_message(str(list[i][0])+"  \n"+str(list[i][1])+"  \n"+str(list[i][2]))
        else:
            dispatcher.utter_message("Sorry, I can’t find any weather information about this place")
        return [SlotSet("weather_city", None)]



    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "weather_city": [
                self.from_entity(intent=["ask_weather", "inform"], entity="city"),
                self.from_text(intent="city"),
            ],
        }

    def validate_weather_city(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        value = str(value).lower()
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"

        querystring = {"q": value}

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "6907d22d7amshbe256fd9bf5d738p10bc28jsna0b8b41587f9"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()
        if data['cod'] == '200':
            return {"weather_city": value}
        else:
            dispatcher.utter_message("Sorry, I can’t find any weather information about this place")
            return {"weather_city": None}

class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv(INTENT_DESCRIPTION_MAPPING_PATH)
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(",")}
        )

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        if len(intent_ranking) > 1:
            diff_intent_confidence = intent_ranking[0].get(
                "confidence"
            ) - intent_ranking[1].get("confidence")
            if diff_intent_confidence < 0.2:
                intent_ranking = intent_ranking[:2]
            else:
                intent_ranking = intent_ranking[:1]

        # for the intent name used to retrieve the button title, we either use
        # the name of the name of the "main" intent, or if it's an intent that triggers
        # the response selector, we use the full retrieval intent name so that we
        # can distinguish between the different sub intents
        first_intent_names = [
            intent.get("name", "")
            if intent.get("name", "") not in ["faq"] #
            else tracker.latest_message.get("response_selector")
            .get(intent.get("name", ""))
            .get("full_retrieval_intent")
            for intent in intent_ranking
        ]

        message_title = (
            "Sorry, I'm not sure I've understood " "you correctly 🤔 Do you mean..."
        )

        entities = tracker.latest_message.get("entities", [])
        entities = {e["entity"]: e["value"] for e in entities}

        entities_json = json.dumps(entities)

        buttons = []
        for intent in first_intent_names:
            button_title = self.get_button_title(intent, entities)
            if "/" in intent:
                # here we use the button title as the payload as well, because you
                # can't force a response selector sub intent, so we need NLU to parse
                # that correctly
                buttons.append({"title": button_title, "payload": button_title})
            else:
                buttons.append(
                    {"title": button_title, "payload": f"/{intent}{entities_json}"}
                )

        buttons.append({"title": "Something else", "payload": "/out_of_scope"})

        dispatcher.utter_message(text=message_title, buttons=buttons)

        return []

    def get_button_title(self, intent: Text, entities: Dict[Text, Text]) -> Text:
        default_utterance_query = self.intent_mappings.intent == intent
        utterance_query = (self.intent_mappings.entities == entities.keys()) & (
            default_utterance_query
        )

        utterances = self.intent_mappings[utterance_query].button.tolist()

        if len(utterances) > 0:
            button_title = utterances[0]
        else:
            utterances = self.intent_mappings[default_utterance_query].button.tolist()
            button_title = utterances[0] if len(utterances) > 0 else intent

        return button_title.format(**entities)

class ActionDefaultFallback(Action):

    def name(self):
        return "my_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_default")
        dispatcher.utter_message(template="utter_restart_with_button")
        return [UserUtteranceReverted()] # Fallback policy 執行完畢需自動清除對話紀錄((UserUtteranceReverted()