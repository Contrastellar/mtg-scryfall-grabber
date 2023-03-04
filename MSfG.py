#/opt/homebrew/bin/python3
"""
Module for scraping usefull info off of the scryfall REST API when invoked as a module, versus a library

Author: Contrastellar (Gabriella Agathon)
2023
"""

import os
import time
import json
import argparse
import requests
import GrabCards


def jsonParse(obj):
    """
    Return a string object of the json passed in via obj
    """
    text = json.dumps(obj, sort_keys=True, indent=3)
    return text

def main():
    """
    main, allowing this to be invoked as a module from the command line.
    """

    # Current dir the script is running in, can be useful for debugging
    script_dir = os.path.abspath(os.path.dirname( __file__ ))

    description = "Script to pull card info from api.scryfall.com based on specific set"
    parser = argparse.ArgumentParser(description=description)

    #set to pull card data from
    parser.add_argument('set', metavar='set', help="3-5 letter/number ID that dictates which set to pull from")
    parser.add_argument('-c', '--cards', help="grab card names associated with specific IDs", action='store_true')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')

    # Parse arguments
    args = parser.parse_args()
    verboseSetting = bool(args.verbose)
    userSet = str(args.set)
    pullCardInfo = bool(args.cards)
    pageNum = 1

    if verboseSetting:
        print("Outputting verbosely\n"+script_dir)

    # Used to verify that the two sets are actually identical.
    cardSetURL = "https://api.scryfall.com/sets/" + userSet

    cardListURL = "https://api.scryfall.com/cards/search?include_extras=true&include_variations=true&order=set&q=e%3A"+ userSet +"&unique=prints&page=" + str(pageNum)

    setData = requests.get(cardSetURL, timeout=10000)
    responseData = requests.get(cardListURL, timeout=10000)

    if verboseSetting:
        print("Set URL  =   " + str(cardSetURL))

    if verboseSetting:
        print("Card URL =   " + str(cardListURL))

    if verboseSetting:
        print("Response code: " + str(responseData.status_code) + "\n")

    parsedSetFile = json.loads(jsonParse(setData.json()))
    parsedCardFile = json.loads(jsonParse(responseData.json()))

    if verboseSetting:
        print("Card set from the set search ...  ? -> " + parsedSetFile['name'])

    if verboseSetting:
        print("Card set from the card ID    ... " + parsedCardFile["data"][0]["collector_number"] + "? -> "+ parsedCardFile['data'][0]['set_name'])

    setNameFromSearch = parsedSetFile['name']
    setNameFromCard = parsedCardFile['data'][0]['set_name']

    if(verboseSetting):
        print("Are strings the same?")
        if(setNameFromCard == setNameFromSearch):
            print("Yes!")

        else:
            print("No! Exiting!")
            print("\n\n")
            return

    """
        At this point, we can pretty much get on with it
    """
    if(verboseSetting):
        print("Total cards --   " + str(parsedCardFile["total_cards"]))

        print("\n\n--!-- Does output have \"next page\"?")
        print(parsedCardFile['has_more'])

    # Declare MasterOutput for modification in the following blocks.
    MasterOutput = None

    # TODO - as it turns out its kinda fucked rn
    if(pullCardInfo):
        MasterOutput = GrabCards.GrabCards(UserSet=userSet, ResponseData=responseData, PageNum=pageNum, VerboseSetting=verboseSetting)
        # Serializing json
        outputObject = json.dumps(MasterOutput, indent=4)

        # Writing to sample.json
        with open("output/" + setNameFromSearch + "_card_name_info.json", "w", encoding="UTF8") as outfile:
            outfile.write(outputObject)

if __name__ == "__main__":
    main()