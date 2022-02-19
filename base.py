import json
import string
import urllib.request
import requests
from bs4 import BeautifulSoup
import time


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(
        urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

#Sample simple note creating function, takes three strings (glossary already formatted in html)

def createNote(word, glossary, audio_url):
    return (
        {
            "deckName": "test1",
            "modelName": "Vocab card",
            "fields": {
                "Word": word,
                "Glossary": glossary,
                "Sentence": "",
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "test1",
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "tags": [
                "english"
            ],
            "audio": [{
                "url": audio_url,
                "filename": "english_"+word+".mp3",
                "fields": [
                    "Audio"
                ]
            }]
        }
    )


def fetchData(word):
    # Defining request templete
    request = urllib.request.Request(
        "https://www.google.com/search?q={}+meaning".format(word))
    # Necessary user agent for google (else you get a 403 request)
    request.add_header(
        'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')

    # Requesting meanings to open API dictionary (and turning into JSON)
    request_dictionary = requests.get(
        'https://api.dictionaryapi.dev/api/v2/entries/en/'+word).json()

    # Getting HTML
    audio = urllib.request.urlopen(request)
    # Decoding from utf-8
    audio_html = audio.read().decode('utf-8')
    # Making beautiful soup object (and using html parser )
    audio_soup = BeautifulSoup(audio_html, "html.parser")
    # Finding audio file
    audio_tag = audio_soup.find_all("audio")

    # If the soup search returns no matches link is an empty string, else if it returns a search but doesn't contain a 
    # "source" value, returns an empty string too.
    if(len(audio_tag)):
        if(audio_tag[0].source):
            link= "https:" + audio_tag[0].source["src"]
        else: link=""
    else: link= ""
    
    definitions = ""
    ## Formatting each dictionary entry into an array
    for i in request_dictionary[0]["meanings"]:
        definitions += i["definitions"][0]["definition"] + "<br>"
    
    
    return(
        [
            request_dictionary[0]["word"],
            definitions,
            link
        ]
    )


# invoke('createDeck', deck='test1')
# result = invoke('deckNames')
# print('got list of decks: {}'.format(result))

# reads words from words.txt in the same folder

with open("words.txt", 'r') as f:
    text = f.read().split('\n')

print(text)

notes_to_add = []
for i in text:
    print(i)
    note_data = fetchData(i)
    note = createNote(*note_data)
    print(note)
    notes_to_add.append(note)
    print(notes_to_add)


#note = createNote(*fetchData("six"))
print(notes_to_add)

invoke("addNotes", notes=notes_to_add)

result = invoke('findNotes', query='deck:test1')
print(result)
