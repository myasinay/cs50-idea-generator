import json
import random
import re
import os
from jsonschema import validate

# Base directory of where JSON files stored
basedir = os.path.abspath(os.path.dirname(__file__))
docs_folder = os.path.join(basedir, 'static/docs/')

# Loading the json data
data = json.loads(open(docs_folder + "data.json").read())

# Get JSON Schema for custom data files
with open(docs_folder + "data.schema.json", 'r') as file:
    schema = json.load(file)

# Allowed file upload extensions
ALLOWED_EXTENSIONS = {'json'}


def getItemRandomly(items, probability = 1):
    """Gets random item with the given key from the data"""
    if random.random() > probability:
        return " "
    else:
        randomNumber = random.randint(0, len(items) - 1)
        return items[randomNumber]


def generateIdea():
    """Main idea generator"""
    # Get mood, theme, genre etc.
    mood = getItemRandomly(data["mood"], 0.4)
    theme =  getItemRandomly(data["theme"])
    genre = getItemRandomly(data["genre"])
    random.seed()
    themeAlternative = getItemRandomly(data["theme"])
    genreAlternative = getItemRandomly(data["genre"])
    perspective = getItemRandomly(data["perspective"])
    # Prevent genres and themes from being the same
    while theme == themeAlternative:
        themeAlternative = getItemRandomly(data["theme"])
    # Prevent genres and themes from being the same
    while genre == genreAlternative:
        genreAlternative = getItemRandomly(data["genre"])

    # Generate the character
    character_nature = getItemRandomly(data["character"]["nature"])
    character_description = getItemRandomly(data["character"]["description"], 0.8)
    character_description_post = getItemRandomly(data["character"]["description_post"], 0.6)
    character = character_description + ' ' + character_nature + ' ' + character_description_post

    # Set the setting
    setting = getItemRandomly(data["settings"]["place"]).format(
        description = getItemRandomly(data["settings"]["description"]))

    goal = getItemRandomly(data["goal"])
    wildcard = getItemRandomly(data["wildcard"])

    # Put words into sentences
    sentence = getItemRandomly(data["template"]).format(
        mood = mood,
        theme = theme,
        themeAlternative = themeAlternative,
        perspective = perspective,
        genre = genre,
        genreAlternative = genreAlternative,
        character = character,
        setting = setting,
        wildcard = wildcard,
        goal = goal)


    return finalize(sentence)


def finalize(sentence):
    """"Formatting the output"""
    # Remove leading and trailing whitespaces
    sentence = sentence.strip()
    # Remove the extra whitespaces between words
    sentence = re.sub(r'\s+', ' ', sentence)

    # Define vowels
    vowels = "aeiou"
    # Check the first letter of the sentence and decide the first letter
    first_letter = "A "
    if sentence[0] in vowels:
        first_letter = "An "

    # Format the output
    # It does not give accurate results but still good enough
    sentence = f"{first_letter}{sentence}."
    return sentence


def custom_data(file):
    """"Loading and validating custom data"""

    temp_data = json.loads(file.read())
    # Validate
    try:
        validate(temp_data, schema)
        global data
        data = temp_data
        return True
    # Return error
    except Exception:
        return False


def allowed_file(filename):
    """"Checking for the custom data file extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
