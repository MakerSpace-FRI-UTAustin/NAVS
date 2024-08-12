from google.cloud import speech 
from recording import *
#establishes client connection


client = speech.SpeechClient.from_service_account_file('key.json')

def d1(input):
    trig = "give me directions to "
    loc = input.lower().index(trig)
    input = input[loc + len(trig) : len(input)]
    return input
    
def d2(input):
    trig = "give me directions from "
    loc = input.lower().index(trig)
    input = input[loc + len(trig) : len(input)]
    input = input.split(" to ")
    return input

def stt():
#sets file name
#if user say directions in this format "Give me directions to _____" or "Give me directions from _____ to _______"
    file_name = audio()

    #reads in the mp3 data
    with open(file_name, 'rb') as i:
        mp3_data = i.read()

    #sets audio file and instantiates the recongition process
    audio_file = speech.RecognitionAudio(content=mp3_data)

    #sets speed and language for the voice
    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        enable_automatic_punctuation = True,
        language_code = "en-US"
    )

    #finishes client session
    response = client.recognize(
        config = config, 
        audio = audio_file
    )

    origin = "" #raspberry pi location
    destination = ""

    if("give me directions to" in response.lower()):
        destination = d1(response)
    else:
        o_words = d2(response)
        origin = o_words[0]
        destination = o_words[1]
    out = [origin, destination]
    return out