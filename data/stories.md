## flight form happy path and affirm booking form
* book_flight
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye

## flight form happy path and affirm booking form
* book_flight
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye


## flight form happy path and affirm booking form
* book_flight
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - flight_form 
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye

## flight form happy path and affirm booking form
* book_flight
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form--> 
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
    
## flight form happy path and deny booking form
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
* deny
    - action_stop

## flight form happy path and(kidding-deny) affirm booking form
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
* deny
    - action_stop
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
* deny
    - action_stop

## flight form happy path and(kidding-deny) affirm booking form
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
* deny
    - action_stop
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
* deny
    - action_stop
        
## flight form happy path and affirm booking form(chitchat-deny)
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - action_chitchat
    - booking_form    
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
* deny
    - action_stop

## flight form happy path and affirm booking form(chitchat-affirm-deny)
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->   
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
* deny
    - action_stop
    
## flight form happy path and affirm booking form(chitchat-affirm-affirm-deny)
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->  
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
* deny
    - action_stop

## flight form happy path and affirm booking form(chitchat-affirm-affirm-deny)
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
* deny
    - action_stop
    
## flight form happy path and affirm booking form(chitchat-affirm-affirm-deny)
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
* deny
    - action_stop
* faq
    - respond_faq
    - action_reverted
    
## ask weather
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    
## ask weather
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye

## ask weather
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
    
## ask weather
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
* book_flight
    - flight_form                  <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                  <!--Run the flight_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - action_goodbye
    
## flight form happy path and affirm booking form
* book_flight
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - flight_form
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye

## flight form happy path and affirm booking form
* book_flight
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - flight_form
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->    
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - flight_form
    - form{"name": "flight_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - flight_form
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye

## flight form happy path and affirm booking form
* book_flight
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye

## flight form happy path and affirm booking form
* book_flight
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
* ask_weather
    - weather_form
    - form{"name": "weather_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->
    - booking_form                   <!--Run the booking_form action-->
    - form{"name": "booking_form"}   <!--Activate the form-->
    - form{"name": null}            <!--Deactivate the form-->  
    - action_goodbye
    
# chitchat affirm
* affirm
    - action_chitchat
    
# chitchat deny
* deny
    - action_stop
    
# chichat inform
* inform
    - flight_form                   <!--Run the flight_form action-->
    - form{"name": "flight_form"}   <!--Activate the form-->
    
# chichat inform
* enter_data
    - action_chitchat
    
## check_ticket
* check_ticket
    - utter_check_ticket
    - action_reverted
    
## cancel_ticke
* cancel_ticket
    - utter_cancel_ticket
    - action_reverted
    
## Some question from FAQ
* faq
    - respond_faq
    - action_reverted
