import json
import re
with open('zakon.json','r', encoding='utf-8') as f:
    d = json.load(f)
    # print(d)
# d.sort()

print(d)
pattern = r'Уголовный Кодекс РК Статья (\d+)'

parsed_entries = []
for entry in d:
    match = re.search(pattern, entry['text'])
    if match:
        number = int(match.group(1))
        parsed_entries.append((number, entry))

sorted_entries = sorted(parsed_entries, key=lambda x: x[0])

sorted_json_data = [entry[1] for entry in sorted_entries]

d = sorted_json_data
def append_text(json_data):
    text = json_data["text"]

    formatted_text = text.replace('\n', '\n')

    return formatted_text

all_text = ""
for json_data in d:
    all_text += append_text(json_data) + "\n\n"  # Add two new lines between texts

# Save all text to a single .txt file
with open("new.txt", "w", encoding="utf-8") as file:
    file.write(all_text)

print("All text saved to all_formatted_text.txt successfully.")
