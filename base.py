import json
import urllib.request
import requests

#From Anki connect documentation, sample request making function.
def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

#From anki connect documentation, sample call to API.
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
#Simple anki connect note creating function. 
#Change this to fit your note template. There's probably a way to do it on ankiconnect but this works for me.
def createNote(word, glossary, audio_url):
    return (
        {
            "deckName": "test1", #Change this for your target deckName
            "modelName": "Vocab card", #
            "fields": {
                "Word": word,
                "Glossary": glossary,
                "Sentence": "",
            },
            "options": {
                "allowDuplicate": False, #Change if you want duplicates
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


def fetch_data(word):
    #open file for logging purposes. 
    

    # Defining request templete
    request = urllib.request.Request(
        "https://www.google.com/search?q={}+meaning".format(word))
    # Necessary user agent for google (else you get a 403 request)
    request.add_header(
        'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')

    # Requesting meanings to open API dictionary (and turning into JSON)
    request_dictionary = requests.get(
        'https://api.dictionaryapi.dev/api/v2/entries/en/'+word)

    #If status code isn't 404 
    if request_dictionary.status_code<400:
        ## Formatting each dictionary entry into an array
        request_dictionary = request_dictionary.json()
        word = request_dictionary[0]["word"]
        definitions = "" #declaring definitions string
        for i in request_dictionary[0]["meanings"]:
            definitions += i["definitions"][0]["definition"] + "<br>"
    else: 
        definitions = ""
        word = ""
    #No need to scrape google website as all the audio files follow a similar address. 
    """"
    #
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
    """
    
    #Audio files from google (US pronunciation)
    audio_request = requests.get("https://ssl.gstatic.com/dictionary/static/sounds/20200429/{}--_us_1.mp3".format(word))

    #If the audio file exists, return that as the note link to sound, else return an empty string. 
    if(audio_request.status_code<400):
        audio = audio_request.url
    else: 
        audio = ""
    
    #Returns the word, definitions and audio link (if exist)
    return(
        [
            word,
            definitions,
            audio
        ]
    )

'''
 invoke('createDeck', deck='test1')
 result = invoke('deckNames')
 print('got list of decks: {}'.format(result))
 '''

#Reads txt file into a list (assumes eachword separated by newline, you can add the desired separator and or address here.)
with open("words.txt", 'r') as f: 
    text = f.read().split('\n')
#debug
print(text)
#list for notes
notes_to_add = []
for i in range(len(text)):
    #fetch data from API and google.
    note_data = fetch_data(text[i])
    #log file tester
    if note_data[1]=="":
        text[i] = text[i] + " -Audio"
    if note_data[2]=="":
        text[i] = text[i] + " -Def"
    #create note with spread values of the list returned from fetch_data
    note = createNote(*note_data)
    #appends to list the newly created note
    notes_to_add.append(note)



#note = createNote(*fetch_data("six"))
#print(notes_to_add)

#Call to API with action addNotes and the notes list as args. 
result = invoke("addNotes", notes=notes_to_add)

#Logger
stringu = "" #For storing the formatted list
for i in range(len(result)):
    stringu = stringu+ text[i] + " " + "id:" + str(result[i])+ '\n'

#Print to screen
print(stringu)

#Write logs to local file. 
with open("logs.txt", 'w') as f:
    f.write(stringu)



