import time
from datetime import datetime

import json
from pathlib import Path

import requests
import os
# from moviepy import *

import parse_json
import jwt

import parsetranslation
from shared import *

def get_auth():

    auth_path = Path('auth.json')
    if auth_path.exists():
        with open(auth_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print('Auth file not found, please enter id and secret.')
        client_id = input('Enter client_id:')
        client_secret = input('Enter client_id:')

        data = {
            f"client_id": client_id,
            f"client_secret": client_secret,
            "token": ""
        }

        print('Auth file created at auth.json')
        with open(auth_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return data

def get_transcript(transcribe_id, token):
    my_path = f'translation/{PROJECT_ID}/ko-transcript.json'
    if os.path.exists(my_path):
        with open(my_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    while True:
        resp = requests.get('https://openapi.vito.ai/v1/transcribe/' + transcribe_id, headers={
            'Authorization': f'Bearer {token}'
            }, )
        resp.raise_for_status()
        json_resp = resp.json()

        status = json_resp.get('status', 'EXIT')
        if status != 'transcribing':
            print('Finished (or error):', json_resp)
            break
        else:
            print('Waiting for transcription to finish..')
            print('\t', json_resp)
            time.sleep(15)

    with open(my_path, 'w', encoding='utf-8') as file:
        json.dump(json_resp, file, indent=4)
        return resp.json()

def send_file_to_process(token):
    my_path = f'translation/{PROJECT_ID}/transcript-id.json'
    if os.path.exists(my_path):
        with open(my_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    config = {
        'use_disfluency_filter': True
    }

    if NUM_MEMBERS > 1:
        config['use_diarization'] = True
        config['spk_count'] = NUM_MEMBERS

    try:
        print('Sending audio file', AUDIO_PATH)
        resp = requests.post('https://openapi.vito.ai/v1/transcribe', headers={
            'Authorization': f'Bearer {token}'
        }, data={
            'config': json.dumps(config)
        }, files={
            'file': open(AUDIO_PATH, 'rb')
        })
        resp.raise_for_status()
        resp_json = resp.json()
        print(resp_json)

        with open(my_path, 'w', encoding='utf-8') as file:
            json.dump(resp_json, file)

        return resp_json

    except Exception as e:
        print(f"Exception: {e}")

def make_token():
    auth = get_auth()

    options = {
        "verify_signature": False
    }

    print('Checking token:', auth['token'])
    if auth['token']:
        decode = jwt.decode(auth['token'], "", algorithms=["HS256"], options=options)

        time_exp = datetime.fromtimestamp(decode['exp'])
        if datetime.now() > time_exp:
            print('Token expired, generating new token')
        else:
            print('Token valid, expires at:', time_exp)
            return
    else:
        print('No token found, generating new token')

    resp = requests.post('https://openapi.vito.ai/v1/authenticate', data={
        'client_id': auth['client_id'],
        'client_secret': auth['client_secret']
    })
    resp.raise_for_status()
    auth['token'] = resp.json()['access_token']
    print('New token:', auth['token'])

    with open('auth.json', 'w', encoding='utf-8') as f:
        json.dump(auth, f, indent=4)

    return auth['token']


# def make_audio():
#     if not os.path.exists(AUDIO_PATH):
#         if os.path.exists(FILE_PATH):
#             clip = VideoFileClip(FILE_PATH)
#             clip.audio.write_audiofile(AUDIO_PATH)
#         else:
#             breakpoint()

def main():
    # make_audio()

    token = make_token()

    ai_path = Path(f'translation/{PROJECT_ID}/ai-translation.txt')
    ai_path.parent.mkdir(parents=True, exist_ok=True)
    open(ai_path, 'w').close()

    if id_json := send_file_to_process(token):
        print('File sent, waiting for transcription to be processed..')
        # time.sleep(5)
        transcribe_id = id_json['id']
        print('Transcription finished')
        transcript = get_transcript(transcribe_id, token)
        print('Converting transcript to subtitles')
        parse_json.generate_srt(transcript, PROJECT_ID)

        while True:
            if input(f'Enter the translation in "translation/{PROJECT_ID}/ai-translation.txt" and type [y]').lower() == 'y':
                parsetranslation.parse_translation()
                break
    else:
        print('failed to parse')

if __name__ == '__main__':
    main()

"""
How to use https://www.rtzr.ai/en/stt
1. Set project id in shared.py / number of speakers
2. Get audio file and paste it in AUDIO with the right name
3. Call main.py
4. Translate with gemini
5. Call save result   


The group is composed of eight members: Lee Saerom, Song Hayoung, Park Jiwon, Roh Jisun, Lee Seoyeon, Lee Chaeyoung, Lee Nagyung, and Baek Jiheon. When translating to english, if any of these are mentioned, use these names.

This is from a livestream by the kpop member Jiheon of fromis_9.

Translate these subtitles into english
- Do not put ending full stops
- Strip out korean characters used for emotions such as ㅋㅋㅋㅋ or ㅠㅠ from the translation
- Do not delete merge or skip lines
- Keep each line brief and easy to read, like how real subtitles appear
- Make sure to use the same format as provided:

```
%LINENUMBER%:%MESSAGE%
%LINENUMBER%:%MESSAGE%
cont.
```
---
"""


