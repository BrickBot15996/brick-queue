# This is the current plan of the functionalities for BrickQueue

1. Website where teams can register their team and a WebHook URL to send the Discord messages to.

- How do we limit the WebHook URLs per team? I don't think there is a way to check if someone is part of a team before accepting their WebHook URL

2. WebHook URLs get stored in an SQL DB (probably PostgreSQL) alongside the team numbers they are supposed to track.

3. The app pulls the links from the DB and saves a dict in memory with teamNumber: listOfURLS pairs.

4. The app finds the active event(s) for the first team and saves all teams at the event in another dict to ensure no double tracking of the same event.

5. After getting all events the initial step is finished.

- How often do we reload the teams? There will have to be a mechanism in place to reload whenever a new team registers (with a minimum delay of like 15 mins between resets, and ensuring the current loop of processing events is finished before reloading)
- If no team registers, reloading daily should be good enough.

6. The things we need to keep track of are:

- Event:
  - Number of fields (used to estimate when you should queue for a match)
  - Latest played match
  - Tracked teams in the event
- Team:
  - Match list
  - Last match played
  - Next match
