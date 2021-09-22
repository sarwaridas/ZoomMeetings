import jwt
import requests
import json
from time import time
from pandas import DataFrame


# Enter your API key and your API secret
API_KEY = "vdPilWx_RYSy37dFnM8OvA"
API_SEC = "jl6lVI7bwrpmPvRUNyIu5Z9lf9g5WaNuQDqg"

# create a function to generate a token
def generateToken():
    token = jwt.encode(
        # Create a payload of the token containing
        # API Key & expiration time
        {"iss": API_KEY, "exp": time() + 5000},
        # Secret used to generate token signature
        API_SEC,
        # Specify the hashing alg
        algorithm="HS256",
    )
    return token


# create json data for post requests
# configure settings
meetingdetails = {
    "topic": "The title of your zoom meeting",
    "type": 2,
    "start_time": "2021-09-23T10: 21: 57",
    "duration": "45",
    "timezone": "India",
    "agenda": "test",
    "recurrence": {"type": 1, "repeat_interval": 1},
    "settings": {
        "host_video": "true",
        "participant_video": "true",
        "join_before_host": "False",
        "mute_upon_entry": "False",
        "watermark": "true",
        "audio": "voip",
        "auto_recording": "cloud",
    },
}

# send a request with headers including
# a token and meeting details
def createMeeting():
    headers = {
        "authorization": "Bearer %s" % generateToken(),
        "content-type": "application/json",
    }
    r = requests.post(
        f"https://api.zoom.us/v2/users/me/meetings",
        headers=headers,
        data=json.dumps(meetingdetails),
    )

    # print("\n creating zoom meeting ... \n")
    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]

    return join_URL, meetingPassword


link = list()
pwd = list()

# run the create meeting function
for i in range(34):
    link.append(createMeeting()[0])
    pwd = createMeeting()[1]

df = DataFrame({"Meeting URLs": link, "Meeting Passwords": pwd})
df.to_csv("test.csv")
