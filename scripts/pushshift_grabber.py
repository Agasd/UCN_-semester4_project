import requests
from datetime import datetime
import traceback
import re
subreddit = "bitcoin"

url = "https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&subreddit={}&before="

start_time = datetime.utcnow()


def downloadFromUrl(filename, object_type):
    print(f"Saving {object_type}s to {filename}")

    count = 0
    handle = open(filename, 'a')
    previous_epoch = int(start_time.timestamp())
    while True:
        new_url = url.format(object_type, subreddit) + str(previous_epoch)
        json = requests.get(new_url)
        json_data = json.json()
        if 'data' not in json_data:
            break
        objects = json_data['data']
        if len(objects) == 0:
            break

        for object in objects:
            previous_epoch = object['created_utc'] - 1
            count += 1
            if object_type == 'comment':
                try:
                    created = str(object["created_utc"]).encode(encoding='ascii', errors='ignore').decode()
                    text = str(object["body"]).encode(encoding='ascii', errors='ignore').decode()
                    temp = text
                    output_text = ' '.join([re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in temp.split("\n")])
                    handle.write(created + ";;;;;" + output_text)
                    handle.write("\n")
                except Exception as err:
                    print(f"Couldn't print comment: https://www.reddit.com{object['permalink']}")
                    print(traceback.format_exc())
            elif object_type == 'submission':
                if object['is_self']:
                    if 'selftext' not in object:
                        continue
                    elif "[removed]" in object["selftext"]:
                        continue
                    try:
                        created = str(object["created_utc"]).encode(encoding='ascii', errors='ignore').decode()
                        title = str(object["title"]).encode(encoding='ascii', errors='ignore').decode()
                        text = str(object["selftext"]).encode(encoding='ascii', errors='ignore').decode()
                        temp = title+" "+text
                        output_text = ' '.join([re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in temp.split("\n")])
                        handle.write(created + ";;;;;"+ output_text)
                        handle.write("\n")
                    except Exception as err:
                        print(f"Couldn't print post: {object['url']}")
                        print(traceback.format_exc())

        print("Saved {} {}s through {}".format(count, object_type,
                                               datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d")))

    print(f"Saved {count} {object_type}s")
    handle.close()


downloadFromUrl("reddit_bitcoin_raw.csv", "submission")
downloadFromUrl("reddit_bitcoin_raw.csv", "comment")
