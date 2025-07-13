#!/usr/bin/env python3
"""
Setup script for GitHub Trophy Booster
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="github-trophy-booster",
    version="1.0.0",
    author="Amritpal Singh",
    author_email="your.email@example.com",
    description="A comprehensive toolkit to boost your GitHub profile and earn more trophies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Amritpals01/github-trophy-booster",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "github-analyzer=github_analyzer:main",
            "trophy-tracker=trophy_tracker:main",
        ],
    },
    keywords="github, trophy, profile, analyzer, developer-tools",
    project_urls={
        "Bug Reports": "https://github.com/Amritpals01/github-trophy-booster/issues",
        "Source": "https://github.com/Amritpals01/github-trophy-booster",
        "Documentation": "https://github.com/Amritpals01/github-trophy-booster/blob/master/README.md",
    },
)
