from setuptools import setup

setup(
    name="bfs-web-crawler",
    version="1.0.0",
    description="An AI-powered web crawler with a real-time GUI, built on Breadth-First Search",
    author="Atharva Shevate",
    url="https://github.com/atharva1727/ai-web-crawler-bfs",
    py_modules=["web_crawler_gui"],
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "ttkbootstrap>=1.10.1",
    ],
    entry_points={
        "console_scripts": [
            "bfs-web-crawler=web_crawler_gui:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
