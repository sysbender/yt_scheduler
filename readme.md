

1. Setting up the environment
2. Downloading your first playlist or channel
3. Checking download progress
4. Adding new playlists while it’s running
5. Managing multiple playlists safely

---

# 📘 **YouTube Playlist Downloader — User Guide**

This guide assumes you’re using the Docker-based version of the `yt-dlp` scheduler setup described earlier.

---

## 🧰 1. Initial Setup

### 📦 Requirements

* Docker (and optionally Docker Compose)
* Internet access
* Basic command-line usage

### 📁 Folder structure on your host

Create a working folder, for example:

```bash
mkdir -p ~/yt_scheduler/{config,logs,downloads}
cd ~/yt_scheduler
```

You should have:

```
yt_scheduler/
├── config/        # contains urls.txt and downloaded.txt
├── logs/          # contains download.log
├── downloads/     # where videos will be saved
```

---

## ▶️ 2. Build and Run the Downloader

### **Step 1: Build the image**

From inside `yt_scheduler/` (where your `Dockerfile` is):

```bash
docker build -t yt-scheduler .
```

### **Step 2: Create the playlist/channel URL list**

In `config/urls.txt`, add one YouTube link per line.

Example:

```text
https://www.youtube.com/playlist?list=PLabc123...
https://www.youtube.com/@examplechannel
```

> 💡 You can mix playlists and channels — `yt-dlp` will handle both.

If you don’t want to paste manually, you can generate the list automatically:

```bash
yt-dlp --flat-playlist -i --get-id "https://youtube.com/playlist?list=PLabc123..." \
  | sed 's#^#https://youtu.be/#' >> config/urls.txt
```

### **Step 3: Start the container**

```bash
docker run -d \
  --name yt_downloader \
  -e MAX_PER_DAY=5 \
  -e DELAY_HOURS=4 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/downloads:/app/downloads \
  yt-scheduler
```

The downloader now:

* Reads all links from `config/urls.txt`
* Downloads up to **5 videos per day**
* Waits **4 hours** between downloads
* Logs to `logs/download.log`

You can adjust limits anytime by changing environment variables and restarting the container.

---

## 📋 3. Check Progress

### 🔍 View live logs

See what’s happening in real time:

```bash
docker logs -f yt_downloader
```

You’ll see messages like:

```
[2025-11-05 10:00:00] Starting download: https://youtu.be/abcd123
[2025-11-05 10:10:00] Completed: https://youtu.be/abcd123
[2025-11-05 10:10:00] Sleeping for 4.23 hours before next download.
```

### 🧾 Check the saved log file

All activity is also written to:

```
logs/download.log
```

You can view it anytime:

```bash
tail -n 50 logs/download.log
```

### 💾 Verify downloaded videos

All completed videos are stored in:

```
downloads/
```

Organized by playlist or channel name.

---

## ➕ 4. Adding a New Playlist or Channel

Yes — you **can safely add new playlists** while the container is running!

Here’s how:

1. Edit your `config/urls.txt` on the host machine.
   Add new YouTube playlist or channel URLs (one per line). Example:

   ```text
   https://www.youtube.com/playlist?list=PLabc123...
   https://www.youtube.com/@newchannel
   ```

2. **Save the file** — the container will automatically process new entries the next time it loops through the list.
   It won’t re-download videos already in `downloaded.txt`.

3. If you want to force it to check right away, you can restart the container:

   ```bash
   docker restart yt_downloader
   ```

   The script resumes where it left off, keeping all logs and archives intact.

---

## 🔁 5. Managing Multiple Playlists

You have two options:

### Option A — Single instance handles all playlists

* Just keep appending URLs to the same `config/urls.txt`.
* The script downloads all items sequentially.
* Good if you’re fine with one long queue.

### Option B — Separate containers per playlist

If you want each playlist handled independently, give each its own folders:

```
yt_scheduler/
├── playlist1/{config,logs,downloads}
├── playlist2/{config,logs,downloads}
```

Run each with a unique container name and volume bindings:

```bash
docker run -d \
  --name yt_playlist1 \
  -e MAX_PER_DAY=5 \
  -e DELAY_HOURS=4 \
  -v $(pwd)/playlist1/config:/app/config \
  -v $(pwd)/playlist1/logs:/app/logs \
  -v $(pwd)/playlist1/downloads:/app/downloads \
  yt-scheduler

docker run -d \
  --name yt_playlist2 \
  -e MAX_PER_DAY=3 \
  -e DELAY_HOURS=6 \
  -v $(pwd)/playlist2/config:/app/config \
  -v $(pwd)/playlist2/logs:/app/logs \
  -v $(pwd)/playlist2/downloads:/app/downloads \
  yt-scheduler
```

Each container runs independently and maintains its own limits and schedules.

---

## 🧹 6. Maintenance Tips

| Task                    | Command                          | Description                        |
| ----------------------- | -------------------------------- | ---------------------------------- |
| View running containers | `docker ps`                      | Check if your downloader is active |
| Stop container          | `docker stop yt_downloader`      | Pause downloads                    |
| Restart container       | `docker restart yt_downloader`   | Resume downloads                   |
| Remove old container    | `docker rm yt_downloader`        | Clean up                           |
| Update image            | `docker build -t yt-scheduler .` | Rebuild with latest code           |
| View free disk space    | `du -sh downloads/`              | Monitor video storage              |

---

## 🧠 7. FAQs

### ❓ Can I add a new playlist while one is still downloading?

✅ **Yes.**
Just append new URLs to `config/urls.txt`. The script checks that file each time it finishes or restarts.

---

### ❓ What happens if my system reboots or Docker stops?

✅ The script keeps progress in:

* `downloaded.txt` (prevents re-downloading)
* `logs/download.log` (records history)

When restarted, it picks up where it left off.

---

### ❓ How do I know when everything is done?

When the log ends with:

```
[YYYY-MM-DD HH:MM:SS] All videos processed.
```

and no new URLs remain in `config/urls.txt`.

---

### ❓ Can I change MAX_PER_DAY or DELAY_HOURS later?

Yes — just stop and restart with new values:

```bash
docker stop yt_downloader
docker rm yt_downloader
docker run -d \
  -e MAX_PER_DAY=10 \
  -e DELAY_HOURS=2 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/downloads:/app/downloads \
  yt-scheduler
```

---

### ❓ Is it safe/legal?

Use only for:

* Your own videos
* Public domain or Creative Commons content
  Downloading copyrighted videos without permission violates YouTube’s Terms of Service.

 
