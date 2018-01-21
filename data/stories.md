## story 1
* _general.greet                
  - action_greet
  > check_get_guest_details
* _general.unclear
  - utter_general.chat.unclear

## Guest details 1
> check_get_guest_details
* _general.guest.name[guestname=yegor]
  - utter_general.bot.thankyou
  - utter_general.guest.room
* _general.guest.room[room=805]
  - utter_general.bot.thankyou
  - action_set_auth_true

## Say name
* _general.guest.name[guestname=yegor]
  - utter_general.bot.thankyou

## Check my name
* _general.whatismyname
  - utter_general.whatismyname

## Get slots
* _general.bot.slots
  - action_getslots

## Say goodby
* _general.goodbye
  - utter_general.goodbye

## Say logout
* _general.guest.logout
  - action_logout

## Currency
* _general.currency.request
  - action_currency_answer
