import requests
import utility
lichess_url = "https://lichess.org/"


##  Get the real time status of users
#   @param usernames list of the users
def getRealTimeUserStatus(usernames):
    r = requests.get(lichess_url + "api/users/status", ','.join([str(item) for item in usernames]))
    if r: return r.json()


##  Get the user public data
#   @param username of the user
def getUserPublicData(username):
    r = requests.get(lichess_url + f"api/user/{username}")
    if r: return r.json()


##  Get rating history of a user
#   @param username of the user
def getRatingHistory(username):
    r = requests.get(lichess_url + f"api/user/{username}/rating-history")
    if r: return r.json()


##  Get performance statistic of a user
#   @param username
#   @param perf the category (ultraBullet bullet blitz rapid classical correspondence chess960 crazyhouse antichess atomic horde kingOfTheHill racingKings threeCheck)
def getPerformanceStatistic(username, perf):
    r = requests.get(lichess_url + f"api/user/{username}/perf/{perf}")
    if r: return r.json()


##  Get members of the team
#   @param team_id the id of the team
def getTeamMembers(team_id):
    r = requests.get(lichess_url + f"api/team/{team_id}/users")
    if r: return r.json()


##  Get crosstable between 2 players
#   @param user1 the first user
#   @param user2 the second user
def getCrosstable(user1, user2):
    r = requests.get(lichess_url + f"api/crosstable/{user1}/{user2}")
    if r: return r.json()


##  Get multiple users by ID
#   @param usernames list of the users
def getUsers(usernames):
    r = requests.post(url="https://lichess.org/api/users", data=','.join(str(username) for username in usernames))
    if r: print(r.json())


##  Get daily puzzle
def getDailyPuzzle():
    r = requests.get(lichess_url + f"api/puzzle/daily")
    if r: return r.json() ###in reality it is a ndjson, check!


##  Get the dashboard of a player
#   @param username of user
#   @param days number of precedent days to check
def getUserDashboard(username, days = None):
    if days is not None:
        data = {'days' : days}
    else : data = None
    r = requests.get(lichess_url + f"api/storm/dashboard/{username}", data=data)#check !
    if r: return r.json()


##  Get join requests for the team
#   @param token to authenticate
#   @param team_id the id of the team
def getTeamJoinRequest(token, team_id):
    r = requests.get(lichess_url + f"api/team/{team_id}/requests", headers={"Authorization" : f"Bearer {token}"})
    if r: return r.json()


##  Accept a join request for the team
#   @param token to authenticate
#   @param team_id the id of the team
#   @param user_id it is the ID not the username
def acceptJoinRequest(token, team_id, user_id):
    r = requests.post(lichess_url + f"api/team/{team_id}/request/{user_id}/accept", headers={"Authorization" : f"Bearer {token}"})
    if r: return r.json()


##  Accept a join request for the team
#   @param token to authenticate
#   @param team_id the id of the team
#   @param user_id it is the ID not the username
def refuseJoinRequest(token, team_id, user_id):
    r = requests.post(lichess_url + f"api/team/{team_id}/request/{user_id}/decline", headers={"Authorization" : f"Bearer {token}"})
    if r: return r.json()


##  Send a message to all the team members
#   @param token to authenticate
#   @param team_id the id of the team
#   @param message to send in form-urlencoded format
def messageTeamMembers(token, team_id, message):
    r = requests.post(lichess_url + f"team/{team_id}/pm-all", data={"message" : message}, headers={"Authorization" : f"Bearer {token}"})
    if r: return r.json()


##  Get my profile data
#   @param token to authenticate
def getProfile(token):
    r = requests.get(lichess_url + f"api/account", headers={"Authorization" : f"Bearer {token}"})
    if r: return r.json()


def createTeamBattle(token, team_id="testing-apis", name="Sundayyy", description = "Have Fun", clockTime=10, clockIncrement=5, minutes=90, date=utility.nextSunday()):
    r = requests.post(
        url=lichess_url + "api/tournament",
        data={
            "name": name,
            "description": description,
            "clockTime": clockTime,
            "clockIncrement": clockIncrement,
            "minutes": minutes,
            "startDate": utility.toTimestamp(date),
            "conditions.teamMember.teamId": team_id},
        headers={"Authorization": f"Bearer {token}"})
    if r: return r.json()