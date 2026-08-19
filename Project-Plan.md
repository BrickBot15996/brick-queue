# FTC Match Queue & Scouting Alert System (BrickQueue)

## 1. System Overview & Objective
BrickQueue is an automated event monitoring, team scouting, and queue management system designed for FIRST Tech Challenge (FTC) teams. Because third-party platforms like FTC Nexus require event organizer adoption—which is absent at Romanian League Meets, League Tournaments, and National Championships—this system operates autonomously by ingesting data directly from official and community APIs, alongside real-time video stream computer vision.

The system delivers real-time notifications to a designated Discord channel:
- **Event Kickoff**: Greets the team on the first day of competition with event metadata.
- **Schedule Announcement**: Broadcasts the full qualification match list once published.
- **Match Strategy & Scouting Cards**: Delivers pre-match breakdowns (alliance color, partner/opponent rankings, records, and auto/teleop/endgame OPR breakdowns).
- **Dynamic Queue Alerts**: Dispatches an alert telling the team to report to the queueing area exactly one match in advance of standard queueing timing, adjusted dynamically for single- or multi-field venues.

---

## 2. System Architecture

```
+-----------------------------------------------------------------------------------+
|                                BrickQueue Stack                                   |
|                                                                                   |
|  +---------------------------+             +----------------------------------+   |
|  |   Official FTC Events API |             |          FTC Scout API           |   |
|  |   - Schedule generation   |             |   - Total / Auto / TeleOp /      |   |
|  |   - Match results/scores  |             |     Endgame OPR                  |   |
|  |   - Event status          |             |   - Historical team records      |   |
|  +-------------+-------------+             +-----------------+----------------+   |
|                |                                             |                    |
|                +----------------------+----------------------+                    |
|                                       |                                           |
|                                       v                                           |
|  +-----------------------------------------------------------------------------+  |
|  |                     Core Orchestrator & State Engine                        |  |
|  |  - Event State Machine (Schedule -> In-Progress -> Completed)               |  |
|  |  - Queue Calculation Engine (Field-aware threshold triggers)                |  |
|  |  - State Reconciliation Engine (Auto catch-up on system reboot)             |  |
|  |  - Storage: SQLModel / SQLAlchemy (PostgreSQL / SQLite)                     |  |
|  +---------------------+-----------------------------------+-------------------+  |
|                        ^                                   |                      |
|                        |                                   v                      |
|  +---------------------+-------------------+   +-----------+------------------+   |
|  | YouTube Stream Monitor & OCR Engine     |   | Interactive Discord Bot      |   |
|  | - Automated YouTube live stream search  |   | (discord.py / Slash Commands)|   |
|  | - Stream ingestion via yt-dlp & OpenCV  |   | - Match scouting cards       |   |
|  | - Frame extraction & EasyOCR parsing    |   | - Queue pings & alerts       |   |
|  | - Zero-latency match progress detection |   | - On-demand query commands   |   |
|  +-----------------------------------------+   +------------------------------+   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Data Sources & Ingestion Pipeline

### 3.1 Official FTC Events API
- **Base URL**: `https://ftc-api.firstinspires.org/v2.0/`
- **Endpoints**:
  - `GET /{season}/events?eventCode={eventCode}`: Event metadata, venue, and start/end dates.
  - `GET /{season}/schedule/{eventCode}/qual/hybrid`: Match schedule, team assignments, alliance colors, and match sequence numbers.
  - `GET /{season}/matches/{eventCode}`: Real-time match completion states, score breakdowns, and penalties.
- **Authentication**: HTTP Basic Auth using FIRST API token credentials.

### 3.2 FTC Scout API
- **Base URL**: `https://api.ftcscout.org/v1/`
- **Endpoints**:
  - `GET /teams/{teamNumber}`: Metadata, team name, and school/organization.
  - `GET /events/{season}/{eventCode}/teams`: Event-specific performance data including Total OPR, Autonomous OPR, TeleOp OPR, Endgame OPR, and Win-Loss-Tie records.

### 3.3 YouTube Live Stream & Computer Vision Pipeline
- **Stream Discovery**: The system queries the YouTube Data API v3 using the search pattern `[EVENT_NAME] FTC` to locate the official live broadcast.
- **Stream Resolution**: `yt-dlp` extracts the raw HLS `.m3u8` stream URL.
- **Frame Processing**: OpenCV (`cv2.VideoCapture`) captures video frames at fixed intervals (every 2–3 seconds).
- **OCR Processing**: EasyOCR runs on designated bounding boxes (Regions of Interest) corresponding to the on-screen score overlay graphic to detect:
  - Active match number (e.g., `Qual 12`).
  - Active game phase (`Autonomous`, `TeleOp`, `Endgame`, `Match Over`).
- **Purpose**: Eliminates the 2-to-5-minute latency between a match physically finishing and the official score being posted to the FTC Events API.

---

## 4. Queue Calculation Logic

The queue trigger is computed based on the total number of competition fields:

$$\text{Queue Trigger Match} = M_{\text{target}} - N_{\text{fields}} - 1$$

Where:
- $M_{\text{target}}$: The team's next scheduled match number.
- $N_{\text{fields}}$: The number of active playing fields at the venue.

### Trigger Matrix
| Number of Fields | Target Match | Standard Queue Match | Bot Notification Trigger |
| :--- | :--- | :--- | :--- |
| **1 Field** | Match 10 | Match 9 (1 match ahead) | **Match 8** (starts/finishes) |
| **2 Fields** | Match 10 | Match 8 (2 matches ahead) | **Match 7** (starts/finishes) |

---

## 5. Discord Notification Flow

```
[Day 1 Morning]
       │
       ▼
[1. Event Kickoff Message] ────────────────► "Good luck at [EVENT_NAME]!" + Event Info Embed
       │
       ▼
[Schedule Published to API]
       │
       ▼
[2. Match Schedule Message] ───────────────► Complete list of matches and alliance pairings
       │
       ▼
[Loop: For Each Qualification Match]
       │
       ├──► When (Current Match == Queue Trigger Match):
       │      │
       │      ├──► [3. Match Scout Preview] ──► Alliance color, partner/opponent OPRs & records
       │      │
       │      └──► [4. Queue Alert] ──────────► High-priority ping: "Proceed to Queue Area"
       │
       ▼
[All Qualification Matches Completed]
```

### Discord Message Specifications
1. **Event Kickoff Message**:
   - Sent on the morning of the event.
   - Includes event name, venue location, participating team count, and configured field count.
2. **Match Schedule Message**:
   - Sent as soon as the qualification schedule appears on the FTC Events API.
   - Tabulates match numbers, red alliance teams, and blue alliance teams.
3. **Match Scouting Card**:
   - Dispatched alongside the queue notification.
   - Displays match number, scheduled time, assigned alliance color, and driver station.
   - Detailed statistics for all 4 teams: Rank, W-L-T Record, Total OPR, Auto OPR, TeleOp OPR, Endgame OPR.
4. **Queue Alert**:
   - Urgent alert pinging the drive team role.
   - States target match, field identifier, alliance color, and current match on the field.

---

## 6. Uptime Resilience & State Management

The bot includes an automatic reconciliation loop to recover safely from server reboots, network interruptions, or process restarts without duplicating alerts:

```
[System Startup / Restart]
           │
           ▼
[Read Local Database State] (e.g., Last processed match = 6)
           │
           ▼
[Fetch Current State from FTC Events API] (e.g., Current match = 10)
           │
           ├─► If (Current Match > Last Processed Match):
           │     ├── Ingest missed match scores into scouting history
           │     ├── Suppress expired queue alerts (Matches 7, 8, 9)
           │     └── Post a single "System Reconnected" status embed
           │
           ▼
[Resume Real-Time Polling and Video OCR]
```

---

## 7. Interactive Discord Bot Commands

- `/track_event <event_code>`: Initializes tracking for an event code.
- `/set_fields <count>`: Sets the number of active fields (1 or 2).
- `/next_match`: Displays the team's next upcoming match and full scouting preview on demand.
- `/scout_team <team_number>`: Queries FTC Scout metrics and OPR breakdown for any team.
- `/override_match <match_number>`: Manually sets the current match index if APIs or streams encounter issues.
- `/status`: Displays system health, stream connection status, and current tracking state.

---

## 8. Technical Implementation Roadmap

### Phase 1: Data Ingestion & Storage Architecture (Weeks 1–2)
1. **Project Setup**:
   - Initialize Python project with `uv` or `poetry`.
   - Set up `SQLModel` ORM with models for `Event`, `Team`, `Match`, and `NotificationLog`.
2. **API Clients**:
   - Build asynchronous HTTP client (`aiohttp` / `httpx`) for the FTC Events API with authentication and retry logic.
   - Build client for the FTC Scout API to fetch OPR breakdowns and records.
3. **Database Layer**:
   - Implement storage operations for saving schedules, updating live scores, and logging sent notifications.

### Phase 2: Core Orchestration & Discord Bot (Weeks 3–4)
1. **Discord Bot Gateway**:
   - Build `discord.py` bot supporting Slash Commands (`/track_event`, `/set_fields`, `/next_match`, `/scout_team`, `/override_match`, `/status`).
   - Implement rich embed formatting for schedules, scouting cards, and queue alerts.
2. **State Machine & Queue Dispatcher**:
   - Implement background polling worker running every 15–30 seconds.
   - Implement schedule diffing to trigger schedule announcements.
   - Implement dynamic queue calculation formula ($M_{\text{target}} - N_{\text{fields}} - 1$).
   - Implement state reconciliation loop to handle server reboots cleanly.

### Phase 3: Live Stream OCR Pipeline (Weeks 5–6)
1. **Stream Resolution**:
   - Build YouTube API crawler to locate event livestreams.
   - Extract raw HLS streams via `yt-dlp`.
2. **Vision & OCR Engine**:
   - Implement frame grabber using OpenCV (`cv2.VideoCapture`).
   - Implement bounding-box cropping around the match status graphic.
   - Integrate `EasyOCR` to extract match numbers and match state transitions in real time.
   - Connect OCR output to the Core Orchestrator to trigger queue alerts ahead of official API score submission.

### Phase 4: Integration Testing & Deployment (Week 7)
1. **Testing**:
   - Replay archived event streams to test OCR accuracy and evaluate trigger latency against official API timestamps.
   - Perform end-to-end load and failure recovery testing.
2. **Deployment**:
   - Containerize application with Docker and Docker Compose.
   - Configure automatic container restart policies (`restart: unless-stopped`).
