import acoustid

# acoustid API key
# don't push to github with this lmao
api_key = "API_KEY"

for score, rec_id, title, artist in acoustid.match(api_key, "./hurricane.mp3"):
    print(f"Matched {title} - {artist} with recording id {rec_id} and confidence {score}.")
#response = acoustid.match(api_key, "./diand.mp3", parse=False)
#print(response)
