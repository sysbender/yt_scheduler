Absolutely! Here’s a detailed **Project Requirements / Technical Specification** document for your `yt_scheduler` project, capturing the architecture, tech stack, file structure, and functional requirements. You can keep this in your repo as `requirements.md` or `project-spec.md`.

---

# **Project Requirements: YT Scheduler**

**Project Name:** YT Scheduler
**Purpose:** A containerized YouTube downloader and web editor system that allows users to schedule downloads from YouTube channels, playlists, or individual videos, with web-based URL management.

---

## **1. Technical Overview**

### **1.1 Architecture**

* **Two-container system (Docker Compose)**:

  1. **YT Downloader**

     * Downloads YouTube videos based on a list of URLs.
     * Supports channels, playlists, and single videos.
     * Automatically skips already downloaded videos.
     * Logs download activity.
     * Persistent data stored in `/data`.
  2. **Web Editor (FlaskCode)**

     * Web-based editor to manage URLs and check logs.
     * Uses same `/data` folder to read/write configuration and logs.
     * Accessible via HTTP on port 5000.
* Shared **persistent volume `/data`** for downloads, logs, and config files.
* `/app` folder contains the downloader Python script, mounted in both containers for potential web editing.

### **1.2 Tech Stack**

* **Python 3.11** (slim image for Docker)
* **Docker & Docker Compose**
* **FlaskCode** (installed via pip for the web editor)
* **YT-DLP / youtube-dl** for video downloads
* **Optional Libraries**: `requests`, `pandas`, `schedule`, `python-dotenv` (as needed)

---

## **2. File & Folder Structure**

```
yt_scheduler/
├── LICENSE
├── build.md
├── readme.md
├── docker-compose.yml
├── data/
│   ├── config/
│   │   ├── urls.txt         # List of URLs to download
│   │   └── downloaded.txt   # Record of completed downloads
│   ├── downloads/           # Downloaded videos stored here
│   └── logs/                # Logs from downloader
├── web-editor/
│   └── Dockerfile           # Dockerfile for FlaskCode container
└── yt_downloader/
    ├── Dockerfile           # Dockerfile for downloader container
    ├── requirements.txt     # Python dependencies
    └── yt_downloader.py     # Main downloader script
```

---

## **3. Functional Requirements**

### **3.1 Downloader**

1. **URL Handling**

   * Accept single video URL, playlist URL, or channel URL.
   * Automatically expand playlists and channels into individual video URLs.
2. **Normalization**

   * Video, playlist, and channel names normalized:

     * Non-alphanumeric characters replaced with `-`.
     * Consecutive dashes collapsed into one.
     * Optional lowercase and trimming of leading/trailing dashes.
3. **Download Folder Structure**

   * Channel/playlist downloads go into a folder named after the normalized channel/playlist.
   * Single videos not part of any playlist go into `unknown-playlist`.
4. **Skipping**

   * Skip already downloaded videos (via `downloaded.txt` or filename check).
5. **Logging**

   * Maintain logs in `/data/logs/yt_downloader.log`.
   * Include timestamps and download status.
6. **Auto-refresh**

   * Periodically check for new URLs added to `urls.txt` without restarting the container.

### **3.2 Web Editor (FlaskCode)**

1. **Features**

   * Browse and edit `urls.txt`.
   * View `downloaded.txt` and logs.
   * Optionally trigger downloads manually.
2. **Data Integration**

   * Uses `/data` as `RESOURCE_BASEPATH` to access shared files.

---

## **4. Docker Configuration**

### **4.1 Docker Volumes**

* `/data` → shared persistent storage for downloads, logs, and configuration.
* `/app` → Python scripts (mounted for editing and running).

### **4.2 docker-compose.yml**

* Two services:

  1. `yt-downloader` – builds from `yt_downloader/Dockerfile`, mounts `/app` and `/data`.
  2. `web-editor` – builds from `web-editor/Dockerfile`, mounts `/data` and optionally `/app`.

---

## **5. Development & Deployment**

### **5.1 Installation**

1. Clone repo:

   ```bash
   git clone <repo_url>
   cd yt_scheduler
   ```
2. Build & run containers:

   ```bash
   docker compose up --build -d
   ```

### **5.2 Adding URLs**

* Add new video, playlist, or channel URLs to `data/config/urls.txt`.
* Downloader will automatically pick them up without container restart.

### **5.3 Logs**

* Located in `data/logs/yt_downloader.log`.
* Web interface can be used for easy monitoring.

---

## **6. Optional Enhancements**

* Use Redis or SQLite for faster URL tracking instead of text files.
* Implement a cron-like scheduler inside the downloader container.
* Add email or push notifications when downloads complete.
* Support video quality selection in the downloader.

---

If you want, I can also **turn this into a polished Markdown doc** ready to include in your repo with headings, tables, and diagrams showing container interaction and folder structure. It would be perfect for future onboarding or documentation.

Do you want me to do that?
