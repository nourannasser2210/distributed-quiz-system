# 🎓 Distributed Quiz System

<div align="center">

### 🚀 Real-Time Distributed Quiz Platform using TCP Sockets & CustomTkinter

A modern desktop-based distributed quiz application built with **Python**, leveraging **TCP Socket Programming** for reliable real-time communication and featuring a sleek **dark-themed GUI** powered by **CustomTkinter**.

---

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge\&logo=python)
![Sockets](https://img.shields.io/badge/TCP-Sockets-green?style=for-the-badge)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-purple?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Client--Server-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

</div>

---

# 📌 Overview

The **Distributed Quiz System** is a real-time client-server desktop application designed to simulate a distributed examination environment where multiple users can connect simultaneously to a centralized quiz server.

The application demonstrates key concepts in:

* Distributed Systems
* Socket Programming
* Multi-threading
* Client-Server Architecture
* Real-time Communication
* GUI Development

---

# ✨ Features

## 🖥️ Server Dashboard

### 📚 Dynamic Question Management

* Add Multiple Choice Questions (MCQs)
* Add True/False Questions
* Delete existing questions instantly
* Manage quizzes during runtime without restarting the server

### 📡 Live Client Monitoring

* Track connected users in real-time
* Monitor client states such as:

  * Waiting
  * Answering Question 1/5
  * Completed Quiz

### 📝 Centralized Event Logging

* Connection events
* Client activities
* Quiz lifecycle events
* Timestamped system logs

### 🏆 Automated Leaderboard

* Stores completed results
* Calculates percentages automatically
* Displays rankings instantly

---

## 👥 Client Application

### 🔐 User Authentication

* Simple username-based login
* Instant server registration

### 🎨 Interactive User Experience

* Dynamic question rendering
* Multiple choice radio buttons
* Smooth transitions between questions
* Progress indicators and counters

### ⚡ Instant Evaluation

* Immediate score calculation
* Performance badges based on results:

| Score      | Badge              |
| ---------- | ------------------ |
| 90% - 100% | 🏆 Excellent       |
| 75% - 89%  | 🌟 Very Good       |
| 50% - 74%  | 👍 Good Job        |
| Below 50%  | 📚 Keep Practicing |

---

# 🏗️ System Architecture

The project follows a **Distributed Client-Server Architecture**.

```text
                    ┌────────────────────┐
                    │    Quiz Server     │
                    │--------------------│
                    │ Question Database  │
                    │ Client Manager     │
                    │ Result Processor   │
                    │ Activity Logger    │
                    └─────────┬──────────┘
                              │ TCP Socket
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client 1  │      │   Client 2  │      │   Client N  │
│ Quiz GUI    │      │ Quiz GUI    │      │ Quiz GUI    │
└─────────────┘      └─────────────┘      └─────────────┘
```

---

# 🧩 Project Structure

```text
distributed-quiz-system/
│
├── server.py
├── client.py
│
├── core/
│   ├── QuizServerCore.py
│   ├── QuizClientCore.py
│
├── gui/
│   ├── QuizServerApp.py
│   ├── QuizClient.py
│
├── assets/
│   ├── screenshots/
│   └── icons/
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Technology Stack

| Category             | Technologies  |
| -------------------- | ------------- |
| Programming Language | Python        |
| Networking           | TCP Sockets   |
| GUI Framework        | CustomTkinter |
| Data Exchange        | JSON          |
| Concurrency          | Threading     |
| Architecture         | Client-Server |

---

# 🔄 Communication Workflow

```text
Client Connects
        ↓
Authentication Request
        ↓
Server Validation
        ↓
Questions Sent Sequentially
        ↓
Client Responses Submitted
        ↓
Score Calculation
        ↓
Result Delivered
        ↓
Leaderboard Updated
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/nourannasser2210/distributed-quiz-system.git
cd distributed-quiz-system
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

## Start Server

```bash
python server.py
```

## Launch Client

```bash
python client.py
```

You can open multiple client instances simultaneously to simulate a distributed environment.

---

# 📈 Future Enhancements

* Database integration using SQLite or MySQL
* Question categories and difficulty levels
* Timer-based quizzes
* User accounts and authentication
* Result export to PDF or Excel
* LAN discovery for automatic server detection

---

# 👩‍💻 Author

## Nouran Nasser

Computer Science Student | AI & Software Engineering Enthusiast

* 💼 Interested in Artificial Intelligence, NLP, Computer Vision, and Distributed Systems
* 🌍 Open to collaboration and freelance opportunities

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps the project reach more developers and motivates future improvements.

---

<div align="center">

### Built with ❤️ using Python and Socket Programming

</div>

