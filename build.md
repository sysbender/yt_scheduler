Perfect! Since FlaskCode is now a **git submodule**, we can adjust your `docker-compose.yml` and instructions so everything works smoothly. Here’s the updated setup:

---

## **1️⃣ Updated `docker-compose.yml`**

```yaml
services:
  downloader:
    build:
      context: ./yt_downloader   # Path to your downloader Dockerfile
    container_name: yt_downloader
    restart: unless-stopped
    volumes:
      - ./app/downloads:/app/downloads
      - ./app/logs:/app/logs
      - ./app/config:/app/config
    environment:
      - MAX_PER_DAY=5
      - DELAY_HOURS=4

  web-editor:
    build:
      context: ./flaskcode      # Submodule folder
    container_name: flaskcode
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - RESOURCE_BASEPATH=/app
    volumes:
      - ./app:/app
```

✅ Notes:

* `./flaskcode` points to the **submodule**.
* Your `app/` folder is mounted for editing `urls.txt` and viewing logs.

---

## **2️⃣ Folder structure**

After adding the submodule, your repo should look like this:

```
yt_scheduler/
├─ yt_downloader/       # Your downloader Dockerfile & Python script
├─ flaskcode/           # Submodule for FlaskCode
├─ app/
│  ├─ config/           # urls.txt, downloaded.txt, etc.
│  ├─ logs/             # downloader.log
│  └─ downloads/
├─ docker-compose.yml
└─ .gitmodules          # Submodule info
```

---

## **3️⃣ Commands to build and run**

1. Initialize the submodule (if cloned from scratch):

```bash
git submodule update --init --recursive
```

2. Build and start containers:

```bash
docker compose up --build -d
```

3. Access the web editor:

```
http://localhost:5000
```

* You can now **edit `urls.txt`** and check logs from the web interface.

4. Check downloader logs:

```bash
docker logs -f yt_downloader
```

---

## **4️⃣ Updating the submodule**

If FlaskCode releases updates:

```bash
cd flaskcode
git pull origin main
cd ..
git add flaskcode
git commit -m "Update FlaskCode submodule"
git push
```

---

This setup keeps **downloader** and **web editor** separate, allows **editing URLs via the web**, and ensures **FlaskCode is versioned** as part of your repo.

---

If you want, I can also **update your downloader Python script** so it will **detect new URLs dynamically** from the `urls.txt` file edited in FlaskCode, without restarting the container. This would fully integrate the two.

Do you want me to do that?
