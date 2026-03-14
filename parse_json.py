import json
import datetime as dt
from shared import *

speaker_map = []

def format_time(milliseconds):
    # Convert milliseconds to timedelta
    time_delta = dt.timedelta(milliseconds=milliseconds)

    # Add timedelta to a reference date (e.g., 00:00:00)
    base_time = dt.datetime(1, 1, 1)  # Arbitrary date, doesn't matter
    final_time = base_time + time_delta

    # Format using strftime
    formatted_time = final_time.strftime("%H:%M:%S.") + str(time_delta.microseconds // 1000).zfill(3)
    return formatted_time

def generate_srt(transcript, project_id):
    captions = []
    gpt_out = []

    data = transcript['results']['utterances']
    print(data)
    speakers = set()
    for i, d in enumerate(data):
        print(i, d)
        start = d['start_at']
        end = start + d['duration']
        msg = d['msg']

        spk_id = d.get('spk')
        if (spk_id is not None) and (spk_id in SPEAKER_MAP):
            msg = f'{SPEAKER_MAP[spk_id]}: {msg}'
            if spk_id != 0:
                breakpoint()

        caption = f'{format_time(start)} --> {format_time(end)}\n{msg}'
        captions.append(caption)

        gpt_out.append(f'{i}:{msg}')

        speakers.add(d['spk'])

    out_text = "WEBVTT\n\n"

    out_text += '\n\n'.join(captions)
    # print(captions)
    # print(speakers)

    with open(f'translation/{project_id}/{project_id}.ko.vtt', 'w', encoding='utf-8') as out_file:
        out_file.write(out_text)

    with open(f'translation/{project_id}/ko-gpt.csv', 'w', encoding='utf-8') as out_file:
        gpt_text = '\n'.join(gpt_out)
        out_file.write(gpt_text)
