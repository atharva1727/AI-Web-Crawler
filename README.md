# AI-Web-Crawler
An AI-powered web crawler built in Python using the Breadth-First Search (BFS) algorithm. It features a modern GUI for real-time progress tracking, handles dynamic content, and respects robots.txt directives


<p align="center">
  <img src="https://github.com/atharva1727/AI-Web-Crawler/blob/main/webcrawler.png" width="90" alt="Web Crawler Icon"/>
</p>

<h1 align="center">🌐 AI Web Crawler — BFS Edition</h1>

<p align="center">
  <b>An AI-Powered Web Crawler with a Real-Time GUI, Built on Breadth-First Search</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Tkinter-GUI-FF6F00?style=for-the-badge" />
  <img src="https://img.shields.io/badge/ttkbootstrap-Modern%20UI-1C3C3C?style=for-the-badge" />
  <img src="https://img.shields.io/badge/BeautifulSoup-Parsing-43B02A?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
</p>

<p align="center">
  ⭐ If this project helped you, please consider starring the repo!
</p>

---

## 📖 Overview

**AI Web Crawler (BFS Edition)** is a desktop application that systematically explores and indexes web pages starting from a single seed URL, using the **Breadth-First Search (BFS)** algorithm. It respects every site's `robots.txt` directives, avoids redundant crawling with a visited-URL set, and gives the user full control over the crawl through a clean, modern **Tkinter + ttkbootstrap** interface.

The crawler runs on a background thread so the GUI never freezes, streams live progress and logs to the screen, and lets the user export all indexed URLs to a local file at the end of a session. Beyond being a working tool, it's a practical mini case study in **graph traversal algorithms**, **ethical/compliant crawling**, and **responsive multithreaded desktop UI design**.

This project was built as part of an Artificial Intelligence lab activity (BFS-based crawling and page indexing) and later polished into a standalone, reusable application.

---

## 📑 Table of Contents

- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How BFS Crawling Works](#-how-bfs-crawling-works)
- [Workflow Diagram](#-workflow-diagram)
- [Architecture Overview](#-architecture-overview)
- [Folder Structure](#-folder-structure)
- [Installation Guide](#-installation-guide)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
- [Testing & Validation](#-testing--validation)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)
- [License](#-license)

---

## ❓ Problem Statement

Manually exploring a website's link structure — or writing a one-off script for it — doesn't scale, and naive crawlers often re-visit the same pages, ignore `robots.txt`, get stuck on dynamic content, or lock up the interface while fetching pages.

This project implements a crawler that:

- Traverses pages **level by level** using BFS, starting from a single seed URL
- **Avoids redundant crawling** via a visited-URL set
- **Respects `robots.txt`** rules before fetching any page
- Runs crawling **off the main thread** so the GUI stays responsive at all times
- Gives the user **live visibility and control** — progress tracking, logs, pause/resume/stop, and export

---

## 🎯 Objectives

- Design and implement an **AI-powered web crawler** using the **Breadth-First Search** algorithm
- Develop a **graphical user interface (GUI)** that allows full user interaction with the crawler
- Systematically **index web pages** starting from a seed URL while respecting `robots.txt`
- Provide features such as **progress tracking**, **URL visualization**, **pause/resume/stop** controls, and **save indexed URLs**
- **Handle dynamic content** gracefully and prevent redundant crawling
- Evaluate crawler **adaptability** across different websites and assess GUI **usability**

---

## ✨ Features

✅ **BFS Traversal** — Explores the web graph level-by-level using a FIFO queue (`collections.deque`)

✅ **Robots.txt Compliance** — Checks `can_fetch()` permissions via `RobotFileParser` before crawling any URL

✅ **Duplicate-Free Crawling** — A visited-set guarantees each URL is indexed only once

✅ **Responsive GUI** — Crawling runs on a background `threading.Thread`; the interface never freezes

✅ **Live Progress Tracking** — Real-time crawled-page counter and an indeterminate progress bar

✅ **Streaming Log Console** — A dedicated Logs tab shows every crawl, skip, and error as it happens

✅ **Pause / Resume / Stop** — Full control over an in-progress crawl at any time

✅ **Clickable Results** — Click any indexed URL in the results table to open it directly in your browser

✅ **Hover Preview** — Hovering over a row shows the full URL in a status label

✅ **URL Normalization** — Strips trailing slashes and validates scheme (`http`/`https` only) before enqueuing

✅ **Export to File** — Save all indexed URLs to `crawled_urls.txt` in one click

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python 3.9+ |
| **GUI Framework** | Tkinter, ttkbootstrap (`flatly` theme) |
| **Web & Parsing** | Requests, BeautifulSoup4 |
| **Standard Library** | `urllib.parse`, `urllib.robotparser`, `collections.deque`, `threading`, `webbrowser` |
| **Core Concepts** | Breadth-First Search, Robots Exclusion Protocol, Multithreaded GUI Programming |

---

## 🧠 How BFS Crawling Works

Starting from the seed URL, the crawler maintains a **queue** of URLs to visit and a **set** of URLs already visited:

1. Dequeue the next URL (FIFO — this is what makes it BFS rather than DFS).
2. Skip it if already visited, or if `robots.txt` disallows it.
3. Fetch the page and confirm it's HTML (`Content-Type` check).
4. Parse all `<a href>` links with BeautifulSoup, normalize each one, and enqueue any that haven't been seen yet.
5. Repeat until the queue is empty or the user stops the crawl.

Because new links are always appended to the **back** of the queue, the crawler fully exhausts one "depth level" of links before moving to the next — mirroring a level-order traversal of the implicit web graph.

---

## 🔁 Workflow Diagram

```
   [ Enter Seed URL ]
            |
            v
   [ Initialize Queue + Visited Set ]
            |
            v
   [ Dequeue Next URL ] <-------------------+
            |                               |
            v                               |
   [ Check robots.txt permissions ]         |
            |                               |
     allowed? --- no --> [ Skip URL ] ------+
            |
           yes
            |
            v
   [ Fetch Page & Parse Links (BeautifulSoup) ]
            |
            v
   [ Normalize + Enqueue New Links ] --------+
            |
            v
   [ Update GUI: URL List, Progress, Logs ]
            |
            v
   [ Queue Empty or Stopped? ] --- no --> back to Dequeue
            |
           yes
            v
   [ Crawl Finished ]
```

---

## 🏗️ Architecture Overview

The application is organized around a single `WebCrawlerGUI` class that separates concerns into distinct responsibilities:

- **GUI Layer** (`setup_gui`) — Builds the Home and Logs tabs, buttons, progress bar, and results table using ttkbootstrap widgets
- **Control Layer** (`start_crawl`, `stop_crawl`, `toggle_pause`) — Manages crawl state and enables/disables buttons appropriately
- **Crawling Engine** (`bfs_crawl`) — Runs on a background `threading.Thread`, performs the BFS loop, and pushes UI updates back to the main thread safely via `root.after()`
- **Compliance Layer** (`is_allowed_by_robots`) — Parses each domain's `robots.txt` using `RobotFileParser` before fetching any page
- **Utility Layer** (`normalize_url`, `save_to_file`, `handle_click`, `update_hover`) — URL normalization, file export, and interactive link handling

This separation keeps the crawling logic fully decoupled from the GUI, so either half can be extended independently — for example, swapping Tkinter for a web front end without touching the BFS engine at all.

---

## 📂 Folder Structure

```
ai-web-crawler-bfs/
│
├── web_crawler_gui.py        # Main application (GUI + BFS crawler logic)
├── requirements.txt
├── .gitignore
├── README.md
│
├── assets/
│   └── banner.png
│
└── screenshots/
    ├── home_screen.png
    ├── seed_url_entered.png
    └── crawling_in_progress.png
```

---

## ⚙️ Installation Guide

```bash
# 1. Clone the repository
git clone https://github.com/atharva1727/ai-web-crawler-bfs.git

# 2. Navigate into the project directory
cd ai-web-crawler-bfs

# 3. Create a virtual environment
python -m venv venv

# 4. Activate the virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
```

**`requirements.txt`**
```
requests
beautifulsoup4
ttkbootstrap
```

---

## 🚀 Usage Guide

```bash
# Run the application
python web_crawler_gui.py
```

Once the window opens:

1. Enter a **seed URL** (e.g. `https://www.example.com`)
2. Click **Start** to begin the BFS crawl
3. Watch indexed pages populate in real time, with the page count and progress bar updating live
4. Use **Pause / Resume** to control the crawl, or **Stop** to end it at any point
5. Click any URL in the results table to open it directly in your browser
6. Click **💾 Save URLs** to export everything indexed to `crawled_urls.txt`
7. Switch to the **Logs** tab to review the full crawl history, including skipped and failed URLs

---

## 🖼️ Screenshots

### 🏠 Home Screen — Ready to Crawl
Clean, minimal starting state before any crawl has begun.

![Home Screen](https://github.com/atharva1727/AI-Web-Crawler/blob/main/home_screen.png)

### ⌨️ Seed URL Entered
The user provides a seed URL and is ready to hit **Start**.

![Seed URL Entered](https://github.com/atharva1727/AI-Web-Crawler/blob/main/seed_url_entered.png)

### ⚡ Crawl In Progress — Live Results
Indexed pages populate in real time as the BFS traversal explores the site level by level.

![Crawling in Progress](https://github.com/atharva1727/AI-Web-Crawler/blob/main/crawling_in_progress.png)

---

## ✅ Testing & Validation

The crawler was validated against the following criteria:

- All crawled URLs load correctly in a browser and are valid, well-formed links
- URLs from `robots.txt`-disallowed paths never appear in the results
- No duplicate entries are present across a full crawl session
- The GUI reflects real-time crawling progress, page counts, and activity logs
- Tested across both static and dynamic websites to evaluate coverage and adaptability
- Manually verified `robots.txt` compliance on multiple domains
- Pause/resume behavior and edge cases (timeouts, broken links, non-HTML content) were exercised and handled gracefully

---

## 🔮 Future Enhancements

- 🧠 **Smarter Crawling** — Use an LLM to classify and prioritize pages by relevance before crawling them
- 📊 **Analytics Dashboard** — Visualize crawl depth, domain distribution, and response times
- ☁️ **Cloud Deployment** — Run scheduled crawls on a server and store results in a database
- 🎯 **Content-Aware Filtering** — Automatically skip non-relevant file types and duplicate content
- 🤝 **Multi-Domain Crawling** — Crawl and compare multiple seed domains in parallel sessions
- 🌀 **Dynamic Content Support** — Integrate headless-browser rendering (e.g. Playwright) for JavaScript-heavy sites

---

## 👨‍💻 Author

<p align="center">
  <b>Atharva Shevate</b><br>
  AI Engineer | GenAI, Automation & Applied ML
</p>

<p align="center">
  <a href="https://linkedin.com/in/atharva-shevate-082b602a7">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://github.com/atharva1727">
    <img src="https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  <a href="https://atharva1727.github.io/Atharva--Portfolio">
    <img src="https://img.shields.io/badge/Portfolio-Visit-FF5722?style=for-the-badge&logo=googlechrome&logoColor=white" />
  </a>
</p>

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it with attribution.

---

<p align="center">
  ⭐ If you found this project interesting, don't forget to give it a star!
</p>
