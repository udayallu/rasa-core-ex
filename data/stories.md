## Introduction
* general.greet                
  - action_greet
  > check_get_guest_details
* general.unclear
  - utter_general.chat.unclear

## Guest details 1
> check_get_guest_details
* general.guest.name{"guestname": "yegor"}
  - utter_general.bot.thankyou
  - utter_general.guest.room
* general.guest.room{"room": "805"}
  - utter_general.bot.thankyou
  - action_set_auth_true

## Say name
  * general.guest.name{"guestname": "kirill"}
  - utter_general.bot.thankyou

## Check my name
* general.whatismyname
  - utter_general.whatismyname

## Get slots
* general.bot.slots
  - action_getslots

## Say goodby
* general.goodbye
  - utter_general.goodbye

## Say logout
* general.guest.logout
  - action_logout