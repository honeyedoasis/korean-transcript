import json
import datetime as dt
from shared import *

def format_time(milliseconds):
    # Convert milliseconds to timedelta
    time_delta = dt.timedelta(milliseconds=milliseconds)

    # Add timedelta to a reference date (e.g., 00:00:00)
    base_time = dt.datetime(1, 1, 1)  # Arbitrary date, doesn't matter
    final_time = base_time + time_delta

    # Format using strftime
    formatted_time = final_time.strftime("%H:%M:%S.") + str(time_delta.microseconds // 1000).zfill(3)
    return formatted_time


def parse_translation():
    captions = []

    gpt_out = []

    with open(f'translation/{PROJECT_ID}/ko-transcript.json', 'r', encoding='utf-8') as timings_file:
        with open(f'translation/{PROJECT_ID}/ai-translation.txt', 'r', encoding='utf-8') as translation_file:
            timings_data = json.load(timings_file)['results']['utterances']
            translated_lines = translation_file.read().splitlines()
            print(len(timings_data), len(translated_lines))
            print(translated_lines)
            for i, d in enumerate(timings_data):
                line = translated_lines[i]
                msg = (':'.join(line.split(':')[1:])).strip()
                # print(msg, lines)
                # print(i, d)
                start = d['start_at']
                end = start + d['duration']
                # msg = d['msg']
                caption = f'{format_time(start)} --> {format_time(end)}\n{msg}'
                captions.append(caption)

                if not msg.endswith('..'):
                    msg = msg.removesuffix('.')

                gpt_out.append(f'{i},{msg}')

    out_text = "WEBVTT\n\n"

    out_text += '\n\n'.join(captions)
    # print(captions)

    with open(f'translation/{PROJECT_ID}/{PROJECT_ID}.en.vtt', 'w', encoding='utf-8') as out_file:
        out_file.write(out_text)

if __name__ == '__main__':
    parse_translation()
