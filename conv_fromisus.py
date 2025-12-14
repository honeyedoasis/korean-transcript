import json
import datetime as dt
from main import PROJECT_ID

def format_time(milliseconds):
    # Convert milliseconds to timedelta
    time_delta = dt.timedelta(milliseconds=milliseconds)

    # Add timedelta to a reference date (e.g., 00:00:00)
    base_time = dt.datetime(1, 1, 1)  # Arbitrary date, doesn't matter
    final_time = base_time + time_delta

    # Format using strftime
    formatted_time = final_time.strftime("%H:%M:%S")
    return formatted_time


def main():
    captions = []

    with open(f'translation/{PROJECT_ID}/{PROJECT_ID}.json', 'r', encoding='utf-8') as json_file:
        with open(f'translation/{PROJECT_ID}/gpt-eng.txt', 'r', encoding='utf-8') as csv_file:
            data = json.load(json_file)['results']['utterances']

            lines = csv_file.read().splitlines()

            last_minute = -1
            for i, d in enumerate(data):
                line = lines[i]
                msg = (':'.join(line.split(':')[1:])).strip()
                print(i, d)
                start = d['start_at']
                end = start + d['duration']
                # msg = d['msg']

                start_formatted = format_time(start)
                minutes = int(start_formatted.split(':')[1])
                if minutes != last_minute:
                    captions.append(f'\n{start_formatted} GPT')
                    last_minute = minutes

                if not msg.endswith('..'):
                    msg = msg.removesuffix('.')

                caption = f'LN{i} {msg}'
                captions.append(caption)

    out_text = '\n'.join(captions)
    # print(captions)

    with open(f'translation/{PROJECT_ID}/{PROJECT_ID}-sus.txt', 'w', encoding='utf-8') as out_file:
        out_file.write(out_text)

if __name__ == '__main__':
    main()
