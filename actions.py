from rasa_core.actions import Action
from rasa_core.events import SlotSet, AllSlotsReset

# from .utils import *

class ActionGetSlots(Action):
    """
    Get slot information in terminal (dev)
    """
    def name(self):
        return 'action_getslots'

    def run(self, dispatcher, tracker, domain):
        print(tracker.slots)
        dispatcher.utter_message("Slots is in terminal")
        return []

class ActionGreet(Action):
    """
    Greeting the user in messenger.

    1. Check user authorization
    2. Send specific branch of dialog depende
    """

    def name(self):
        return 'action_greet'

    def run(self, dispatcher, tracker, domain):

        if tracker.get_slot('guestname') and tracker.get_slot('room') and tracker.get_slot('is_authenticated') is None:
            tracker.update(SlotSet('is_authenticated', True))

        if tracker.get_slot('is_authenticated') is None:
            # reset all slots to None in begin
            tracker.update(AllSlotsReset())

            # send the introduce
            dispatcher.utter_template("utter_general.greet.initial")
            dispatcher.utter_template("utter_general.bot.whoareyou")
            dispatcher.utter_template("utter_general.bot.capabilities")
            dispatcher.utter_template("utter_general.guest.name")
        else:
            # send 'hello'
            dispatcher.utter_template("utter_general.greet", guestname=tracker.get_slot('guestname'))
        return []

class ActionSetAuthTrue(Action):
    """
    Set 'is_authenticated' slot in True
    """

    def name(self):
        return 'action_set_auth_true'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet('is_authenticated', True)]

class ActionLogout(Action):
    """
    Log out user from system and reset all slots.
    """

    def name(self):
        return 'action_logout'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template('utter_general.youloggedout', guestname=tracker.get_slot('guestname'))
        return [AllSlotsReset()]
