# 🛠️ Project Setup Guide

Welcome to the Junction2024 project! This guide will help you set up the development environment quickly.

## 📋 Prerequisites

1. **Python**: Make sure you have Python 3.7 or newer installed.
2. **Virtual Environment**: It’s recommended to use a virtual environment to manage dependencies.

## 🚀 Quick Start

### Step 1: Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/nilsson-v/junction2024.git
cd junction2024
```

### Step 2: Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies

Install the required Python packages using requirements.txt:

```bash
pip install -r requirements.txt
```

### Step 4: Get the Firebase Service Account Key

Request the serviceAccountKey.json file from the project maintainer.
Place the file in the firebase/ folder within the project directory:

```bash
junction2024/firebase/serviceAccountKey.json
```

### Step 5: Initialize Firebase

Run the initialization script to set up Firebase:

```bash
python firebase/firebase_init.py
```

If everything is set up correctly, you should see:

```bash
Firebase initialized successfully!
```

## 📝 Important Notes

Do not commit the serviceAccountKey.json file to the repository. This file contains sensitive credentials and is already listed in .gitignore.

If you encounter FileNotFoundError, make sure the serviceAccountKey.json file is in the correct location (firebase/serviceAccountKey.json).

## 🐛 Troubleshooting

Firebase Not Initialized: Ensure the path to serviceAccountKey.json is correct in firebase_init.py.
Dependencies Issues: If you face issues installing dependencies, try updating pip:

```bash
pip install --upgrade pip
```
