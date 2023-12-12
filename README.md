# ZavieBot

ZavieBot is a Telegram bot designed to manage user sign-ups, permissions, and night stay information.

## Table of Contents

- [Introduction](#introduction)
- [Files](#files)
  - [1. Main.py](#1-Mainpy)
  - [2. Database.py](#2-databasepy)
  - [3. Makepdf.py](#3-makepdfpy)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

ZavieBot simplifies user management by allowing users to sign up, edit their information, check their details, and manage night stay permissions. The bot also provides commands to generate PDF reports of user data.

## Files

### 1. Main.py

The main code for ZavieBot. It handles user commands, interactions, and integrates with Telegram using the python-telegram-bot library.

### 2. Database.py

The database module manages user data. It provides functions to add users, retrieve information, and update user details in a SQLite database.

### 3. Makepdf.py

The Makepdf module handles PDF generation. It utilizes the FPDF library to create PDF reports containing user data.

## Usage

To use ZavieBot, follow these steps:

1. Clone the repository.
2. Install dependencies with `pip install -r requirements.txt`.
3. Replace 'YOUR_BOT_TOKEN' in `Main.py` with your actual bot token.
4. Run the bot with `python Main.py`.

## Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or provide feedback.

## License

This project is licensed under the [MIT License](LICENSE).
