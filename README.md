## Usage

 Create a Korean subtitle file using https://www.rtzr.ai/en/stt and translate the result via gemini

### Requirements

* https://www.python.org/downloads/
* Install project requirements `pip install -r requirements.txt`
* Create an account for https://www.rtzr.ai/en/stt
* Make a new application in https://developers.rtzr.ai/dashboard and fill out the `client_id` and `client_secret` in `auth.json`. **Ensure you save your client secret** as you can't see it again. The token will be left blank. 

Example `auth.json`
```json
{
    "client_id": "XXXXXXXXXXX",
    "client_secret": "XXXXXXXXXXX",
    "token": ""
}
```

### Running the program

**NOTE: There is a 50mb limit on the audio file** 

Firstly open the main config file: `shared.py`

```py
PROJECT_ID = 'my-project'
AUDIO_PATH = f'audio/{PROJECT_ID}.m4a'
NUM_MEMBERS = 0
SPEAKER_MAP = {
    # 0: 'JW',
    # 1: 'HY'
}
```

1. Set the output name for your subtitles: `PROJECT_ID` in `shared.py`
1. Get your audio file and put it in a folder called audio e.g. `audio/{PROJECT_ID}.m4a` 
1. Run main.py `python main.py` (this can take a while)
1. It will prompt you to create a translated file
1. Use https://aistudio.google.com/prompts/new_chat to translate this (see [example prompt](#example-prompt) below) 
1. Paste the resulting translation into `translation/{PROJECT_ID}/ai-translation.txt`
1. Enter `y` to confirm
1. Find the translated subtitles at `translation/{PROJECT_ID}/{PROJECT_ID}.en.vtt`

### Setting the speakers

**NOTE: This doesn't work very well and if the speaker map is wrong it can confuse gemini when translating :/**

If you want to map the speakers i.e. `JW: Hello`

Set the `NUM_MEMBERS` and `SPEAKER_MAP` accordingly.

```
NUM_MEMBERS = 2
SPEAKER_MAP = {
    0: 'JW',
    1: 'HY'
}
```

Now when you run the program using the instructions above, the speakers will be randomly assigned.

Adjust the SPEAKER_MAP so that the speaker matches the index and run the program again.


### Example prompt
```
(CONTEXT) Subtitles for a livestream by Jiwon of fromis_9.

(INSTRUCTIONS) Translate these subtitles into english
- Do not put ending full stops
- Strip out korean characters used for emotions such as ㅋㅋㅋㅋ or ㅠㅠ from the translation
- Do not delete merge or skip lines
- Keep each line brief and easy to read, like how real subtitles appear
- Make sure to use the same format as provided:

(FORMAT)
\```
%LINENUMBER%:%MESSAGE%
%LINENUMBER%:%MESSAGE%
cont.
\```

---

<PASTE ko-gpt.csv here>

```
