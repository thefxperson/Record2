import acoustid
import json

# acoustid API key
"""f_keys = open("../secrets.json", "r")
text = f_keys.readline()
keys = json.loads(text)
api_key = keys["ACOUSTID_API_KEY"]
f_keys.close()

for score, rec_id, title, artist in acoustid.match(api_key, "./hurricane.mp3"):
    print(f"Matched {title} - {artist} with recording id {rec_id} and confidence {score}.")"""
#response = acoustid.match(api_key, "./diand.mp3", parse=False)
#print(response)

def acoustid_search(api_key, file_path):
    best_result = {}
    best_result["score"] = 0.0
    for score, rec_id, title, artist in acoustid.match(api_key, file_path):
        print(f"Matched {title} - {artist} with recording id {rec_id} and confidence {score}.", flush=True)
        if score > best_result["score"] and artist != None:
            best_result["rec_id"] = rec_id
            best_result["title"] = title
            best_result["artist"] = artist
            best_result["score"] = score

    return best_result
