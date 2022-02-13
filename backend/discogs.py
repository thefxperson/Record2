import requests

# process albums in a user's library:
def process_item(item, find_main_release=True):
    # find main release url from master urls
    if find_main_release:
        master_req = session.get(item["basic_information"]["master_url"])
        url = master_req.json()["main_release_url"]
    else:
        url = item["basic_information"]["resource_url"]

    # create reduced dict from Discogs response
    return {"artist":       item["basic_information"]["artists"][0]["name"],
            "artist_id":    item["basic_information"]["artists"][0]["id"],
            "title":        item["basic_information"]["title"],
            "id":           item["basic_information"]["id"],
            "url":          url}

def process_album(album):
    tracklist = []
    for track in album["tracklist"]:
        tracklist.append({"title":      track["title"],
                          "duration":   track["duration"]})

    return tracklist

def print_album(album):
    print(f"{album['title']} - {album['artist']}")
    print(f"Artist ID: {album['artist_id']}\nAlbum ID: {album['id']}")
    print("==============================================")
    for track in album["tracklist"]:
        print(f"{track['title']}\t\t\t- {track['duration']}")
    print("\n")


# TODO: write rate limiting decorator or use requests
# create session that sends user agent with every request
"""session = requests.Session()
session.headers.update({"User-Agent": "Record2/0.0.1"})

user = ["USER1", "USER2"]
url = f"https://api.discogs.com/users/{user[1]}/collection/folders/0/releases"
response = session.get(url)
json_response = response.json()

albums = []
#n_items = int(x.json()["pagination"]["items"])
# use forever loop to iterate through pages -- auto breaks at last page
while True:
    # pull all items from a page
    for item in json_response["releases"]:
        album = process_item(item, find_main_release=False)
        album_response = session.get(album["url"])
        album_json = album_response.json()
        album["tracklist"] = process_album(album_json)
        albums.append(album)
        print_album(album)

    # if there is another page, load its data
    try:
        next_url = json_response["pagination"]["urls"]["next"]
    except KeyError:            # final page
        break
    else:
        # request next page of data
        response = session.get(next_url)




for album in albums:
    print_album(album)"""
