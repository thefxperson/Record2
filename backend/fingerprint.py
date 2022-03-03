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


def my_acoustid_search(api_key, file_path, verbose=True):
    best_result = {}
    best_result["score"] = 0.0
    results = acoustid.match(api_key, file_path, parse=False)

    # check query status
    if results["status"] != "ok":
        if verbose:
            print("ERROR: no acoustid results")
        return best_result

    # parse query
    for result in results["results"]:
        if result["score"] > best_result["score"]:
            best_result["title"] = result["recordings"][0]["title"]
            best_result["score"] = result["score"]
            artists = ""
            for artist in result["recordings"][0]["artists"]:
                artists += artist["name"]
                if "joinphrase" in artist:
                    artists += artist["joinphrase"]

            best_result["artist"] = artists
            best_result["id"] = result["id"]
            best_result["duration"] = result["recordings"][0]["duration"]

    return best_result
