import datetime
import json
import datetime as dt

PROJECT_ID = '[250312] jiheon ig live'

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

    with open(f'translation/{PROJECT_ID}/ko-transcript.json', 'r', encoding='utf-8') as json_file:
        with open(f'translation/{PROJECT_ID}/ai-translation.txt', 'r', encoding='utf-8') as csv_file:
            data = json.load(json_file)['results']['utterances']
            lines = csv_file.read().splitlines()
            print(len(data), len(lines))
            for i, d in enumerate(data):
                line = lines[i]
                msg = (':'.join(line.split(':')[1:])).strip()
                print(i, d)
                start = d['start_at']
                end = start + d['duration'] + 200
                caption = f'{format_time(start)} --> {format_time(end)}\nTODO {msg}'
                captions.append(caption)

                if not msg.endswith('..'):
                    msg = msg.removesuffix('.')

    out_text = "WEBVTT\n\n"

    out_text += '\n\n'.join(captions)

    with open(f'translation/{PROJECT_ID}/timings.en.vtt', 'w', encoding='utf-8') as out_file:
        out_file.write(out_text)

if __name__ == '__main__':
    parse_translation()
