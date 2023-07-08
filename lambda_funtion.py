import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta



### Functionality Helper Functions ###
def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")
        
        
        
def build_validation_result(is_valid, violated_slot, message_content):
    """
    Defines an internal validation message structured as a python dictionary.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }

def validate_data(response, intent_request):
    """
    Validates the data provided by the user.
    """

    # Validate the amount, it should be > 0
    for rep in response:
        if rep is not None:
            rep = parse_float(
                rep
                )  # Since parameters are strings it's important to cast values
            if  1 > rep and rep > 4:
                return build_validation_result(
                    False,
                    "rep",
                    "Your response should be a number between 1 and 4, "
                    "please provide a correct response.",
                    )

    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)
    


 ## Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response   
    
### Fuction to build client's profile
def profile_constructor(intent_request):
     # Gets the invocation source, for Lex dialogs "DialogCodeHook" is expected.
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(slots, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))
    
    # Retrieve input values from the Lambda event
    date_of_birth = get_slots(intent_request) ["birthday"]
    retirement_age = get_slots(intent_request) ["retirement"]
    
    #Aggregate Risk Profile slots
    total = 0
    for slot_name, slot_value in get_slots(intent_request).items():
        if slot_name.startswith('qu_') and slot_value is not None:
            total += float(slot_value)
    

    # Calculate the current age
    current_date = datetime.now()
    birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
    current_age = current_date.year - birth_date.year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        current_age -= 1

    # Calculate the years until retirement and retirement date
    years_until_retirement = int(retirement_age) - current_age
    retirement_date = current_date + timedelta(days=years_until_retirement * 365)
    
    return close(
         intent_request["sessionAttributes"],
        "Fulfilled",
        { 
            "contentType": "PlainText",
            "content": """Thank you for your information;
            you are currently {} and have {} years until you retire.
            Your risk profile score is {} and
            your retirement date is {}.
            """.format(current_age, years_until_retirement, total, retirement_date.strftime("%Y-%m-%d"))
        }
    )

### Intents Dispatcher #####
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # Get the name of the current intent
    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "SuggestPortfolio":
        return profile_constructor(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
