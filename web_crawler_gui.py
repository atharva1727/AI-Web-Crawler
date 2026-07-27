"""
BFS Web Crawler — AI-Powered Web Crawler with a Real-Time GUI
================================================================

A desktop application that crawls the web starting from a seed URL using
Breadth-First Search (BFS), respects robots.txt, avoids duplicate crawling,
and displays live progress through a modern Tkinter + ttkbootstrap GUI.

Author: Atharva Shevate
License: MIT
"""

import time
import threading
import webbrowser
from collections import deque
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *


class WebCrawlerGUI:
    """Main application class: owns both the Tkinter GUI and the BFS crawl engine."""

    def __init__(self, root):
        self.root = root
        self.root.title("🌐 BFS Web Crawler")
        self.root.geometry("1000x700")

        # --- Core crawl state ---
        self.visited = set()          # Set of URLs already crawled (prevents duplicates)
        self.queue = deque()          # FIFO queue that drives the BFS traversal
        self.running = False          # True while a crawl is actively in progress
        self.paused = False           # True while the crawl is paused by the user
        self.hover_url = tk.StringVar()

        # --- Styling ---
        self.style = tb.Style("flatly")

        self.setup_gui()

    # ------------------------------------------------------------------
    # GUI Construction
    # ------------------------------------------------------------------
    def setup_gui(self):
        self.notebook = tb.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.tab_main = tb.Frame(self.notebook)
        self.tab_logs = tb.Frame(self.notebook)
        self.notebook.add(self.tab_main, text="Home")
        self.notebook.add(self.tab_logs, text="Logs")

        # --- Header ---
        header = tb.Label(
            self.tab_main,
            text="🌐 BFS Web Crawler",
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary",
        )
        header.pack(pady=(10, 10))

        # --- Seed URL input row ---
        url_frame = tb.Frame(self.tab_main, padding=10)
        url_frame.pack(fill=X, padx=20)

        tb.Label(url_frame, text="Seed URL:", font=("Segoe UI", 12)).pack(side=LEFT)

        self.url_entry = tb.Entry(url_frame, width=70, font=("Segoe UI", 11))
        self.url_entry.pack(side=LEFT, padx=10)

        self.start_button = tb.Button(
            url_frame, text="Start", bootstyle="success", command=self.start_crawl
        )
        self.start_button.pack(side=LEFT, padx=5)

        self.pause_button = tb.Button(
            url_frame,
            text="Pause",
            bootstyle="warning",
            command=self.toggle_pause,
            state=DISABLED,
        )
        self.pause_button.pack(side=LEFT, padx=5)

        self.stop_button = tb.Button(
            url_frame, text="Stop", bootstyle="danger", command=self.stop_crawl, state=DISABLED
        )
        self.stop_button.pack(side=LEFT, padx=5)

        self.save_button = tb.Button(
            url_frame, text="💾 Save URLs", bootstyle="info", command=self.save_to_file
        )
        self.save_button.pack(side=LEFT, padx=5)

        # --- Progress row ---
        progress_frame = tb.Frame(self.tab_main, padding=(20, 5))
        progress_frame.pack(fill=X)

        self.progress_label = tb.Label(
            progress_frame, text="Crawled Pages: 0", font=("Segoe UI", 10)
        )
        self.progress_label.pack(side=LEFT)

        self.progress_bar = tb.Progressbar(
            progress_frame, mode="indeterminate", bootstyle="info-striped", length=200
        )
        self.progress_bar.pack(side=RIGHT)

        # --- Results table ---
        list_frame = tb.Labelframe(
            self.tab_main, text="Crawled URLs (click to open)", padding=10, bootstyle="info"
        )
        list_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.url_list = tb.Treeview(list_frame, columns=("url",), show="headings")
        self.url_list.heading("url", text="URL")
        self.url_list.column("url", anchor="w")
        self.url_list.pack(fill=BOTH, expand=True)
        self.url_list.bind("<Button-1>", self.handle_click)
        self.url_list.bind("<Motion>", self.update_hover)

        self.hover_label = tb.Label(
            self.tab_main, textvariable=self.hover_url, font=("Segoe UI", 9), bootstyle="secondary"
        )
        self.hover_label.pack(pady=(0, 10))

        # --- Logs tab ---
        self.log_text = tb.ScrolledText(self.tab_logs, height=30)
        self.log_text.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # --- Status bar ---
        self.status = tb.Label(
            self.root, text="Ready", relief="sunken", anchor="w", font=("Segoe UI", 9)
        )
        self.status.pack(fill=X, side=BOTTOM)

    # ------------------------------------------------------------------
    # Crawl Controls
    # ------------------------------------------------------------------
    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")

    def start_crawl(self):
        seed_url = self.url_entry.get().strip()
        if not seed_url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        # Reset state for a fresh crawl
        self.visited.clear()
        self.queue = deque([seed_url])
        self.running = True
        self.paused = False

        self.progress_label.config(text="Crawled Pages: 0")
        self.status.config(text="Crawling started")
        self.url_list.delete(*self.url_list.get_children())
        self.log_text.delete("1.0", "end")

        self.start_button.config(state=DISABLED)
        self.pause_button.config(state=NORMAL)
        self.stop_button.config(state=NORMAL)
        self.progress_bar.start(10)

        # Run the BFS crawl on a background thread so the GUI never freezes
        threading.Thread(target=self.bfs_crawl, daemon=True).start()

    def stop_crawl(self):
        self.running = False
        self.status.config(text="Crawling stopped")
        self.pause_button.config(state=DISABLED)
        self.stop_button.config(state=DISABLED)
        self.start_button.config(state=NORMAL)
        self.progress_bar.stop()

    # ------------------------------------------------------------------
    # BFS Crawl Engine
    # ------------------------------------------------------------------
    def bfs_crawl(self):
        """
        Core Breadth-First Search loop.

        Uses a FIFO deque (append + popleft) so links discovered on the
        current page are only visited *after* every URL already queued
        from earlier levels — this is what makes the traversal BFS rather
        than DFS.
        """
        crawled_count = 0

        while self.queue and self.running:
            if self.paused:
                time.sleep(0.5)
                continue

            current_url = self.queue.popleft()

            if current_url in self.visited:
                continue

            self.visited.add(current_url)
            crawled_count += 1

            # Push UI updates back onto the main thread via root.after()
            self.root.after(0, lambda url=current_url: self.url_list.insert("", "end", values=(url,)))
            self.root.after(0, lambda: self.progress_label.config(text=f"Crawled Pages: {crawled_count}"))
            self.root.after(0, lambda url=current_url: self.log_text.insert("end", f"Crawled: {url}\n"))

            if not self.is_allowed_by_robots(current_url):
                self.root.after(0, lambda url=current_url: self.log_text.insert(
                    "end", f"Skipped (robots.txt disallows): {url}\n"))
                continue

            try:
                response = requests.get(
                    current_url, timeout=5, headers={"User-Agent": "BFSWebCrawlerBot"}
                )

                if "text/html" not in response.headers.get("Content-Type", ""):
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                for tag in soup.find_all("a", href=True):
                    href = tag["href"]
                    full_url = urljoin(current_url, href)
                    norm_url = self.normalize_url(full_url)

                    if norm_url and norm_url not in self.visited:
                        self.queue.append(norm_url)

            except Exception as e:
                self.root.after(
                    0, lambda err=e, url=current_url: self.log_text.insert(
                        "end", f"Error crawling {url}: {err}\n"
                    )
                )
                continue

        self.root.after(0, self.done_message)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def normalize_url(self, url):
        """Validate scheme (http/https only) and strip trailing slashes for consistency."""
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return None
        return parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip("/")

    def is_allowed_by_robots(self, url):
        """Check the target domain's robots.txt before fetching a page."""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            rp = RobotFileParser()
            rp.set_url(base_url)
            rp.read()
            return rp.can_fetch("*", url)
        except Exception:
            # If robots.txt can't be read, default to allowing the crawl
            return True

    def done_message(self):
        self.progress_bar.stop()
        self.status.config(text="Crawling finished.")
        messagebox.showinfo("Done", "Crawling finished or stopped.")
        self.start_button.config(state=NORMAL)
        self.pause_button.config(state=DISABLED)
        self.stop_button.config(state=DISABLED)

    def handle_click(self, event):
        """Open the clicked URL in the system's default web browser."""
        item = self.url_list.identify_row(event.y)
        if item:
            url = self.url_list.item(item, "values")[0]
            webbrowser.open(url)

    def update_hover(self, event):
        """Show a live preview of the URL under the mouse cursor."""
        item = self.url_list.identify_row(event.y)
        if item:
            url = self.url_list.item(item, "values")[0]
            self.hover_url.set(f"🔗 {url}")
        else:
            self.hover_url.set("")

    def save_to_file(self):
        """Export all indexed URLs to crawled_urls.txt in the current directory."""
        urls = [self.url_list.item(i, "values")[0] for i in self.url_list.get_children()]
        if not urls:
            messagebox.showinfo("Info", "No URLs to save.")
            return

        with open("crawled_urls.txt", "w") as f:
            f.writelines(url + "\n" for url in urls)

        self.status.config(text="URLs saved to crawled_urls.txt")
        messagebox.showinfo("Saved", "URLs saved to crawled_urls.txt")


def main():
    """Entry point used both by `python web_crawler_gui.py` and the packaged console script."""
    root = tb.Window(themename="flatly")
    app = WebCrawlerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
