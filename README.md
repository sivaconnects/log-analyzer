# 📋 Log File Analyzer

A simple Python web application built with **Flask** that allows you to upload log files and analyze them — view error counts, warnings, top frequent messages, and all error lines in a clean dashboard.

> 🎯 Built for learning and practicing **Python app deployment on AWS EC2**.

---

## 🖥️ Demo

Upload any `.log` or `.txt` file and instantly get:

- ✅ Count of **ERROR / WARNING / INFO / DEBUG** entries
- ✅ **Top 10 most frequent** log messages
- ✅ All **error lines** with line numbers
- ✅ Clean, color-coded web dashboard

---

## 🛠️ Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| Language   | Python 3          |
| Framework  | Flask             |
| Frontend   | HTML + CSS (inline)|
| Server     | EC2 (Ubuntu)      |

---

## 📁 Project Structure

```
log-analyzer/
├── app.py            # Main Flask application
├── requirements.txt  # Python dependencies
├── sample.log        # Sample log file for testing
└── README.md
```

---

## 🚀 Deployment Guide — AWS EC2 (Step by Step)

This guide will walk you through deploying this app on an AWS EC2 instance from scratch.

---

### Step 1 — Launch an EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. Choose **Ubuntu Server 22.04 LTS** (Free tier eligible)
3. Select instance type: **t2.micro** (Free tier)
4. Create or select a **Key Pair** (`.pem` file) — save it safely
5. Under **Network Settings**, click Edit and add these **Inbound Rules**:

| Type        | Protocol | Port | Source    |
|-------------|----------|------|-----------|
| SSH         | TCP      | 22   | My IP     |
| Custom TCP  | TCP      | 5000 | 0.0.0.0/0 |

6. Click **Launch Instance**

---

### Step 2 — Connect to Your EC2 Instance

On your local machine, open a terminal:

```bash
# Give correct permission to your key file
chmod 400 your-key.pem

# SSH into the instance
ssh -i your-key.pem ubuntu@<your-ec2-public-ip>
```

> 💡 Find your public IP in EC2 Console → Instances → your instance → **Public IPv4 address**

---

### Step 3 — Install Dependencies on EC2

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip git -y

# Verify installation
python3 --version
pip3 --version
```

---

### Step 4 — Clone the Repository

```bash
# Clone this repo
git clone https://github.com/<your-username>/log-analyzer.git

# Navigate into the project folder
cd log-analyzer
```

---

### Step 5 — Install Python Requirements

```bash
pip3 install -r requirements.txt
```

---

### Step 6 — Run the Application

```bash
python3 app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

Now open your browser and visit:
```
http://<your-ec2-public-ip>:5000
```

🎉 Your app is live!

---

### Step 7 — Keep the App Running After Closing Terminal

By default the app stops when you close your SSH session. To keep it running, use one of the following options:

**Option A — Using `nohup` (Quick & Simple)**
```bash
nohup python3 app.py &
```

**Option B — Using `screen` (Recommended for practice)**
```bash
# Install screen
sudo apt install screen -y

# Start a screen session
screen -S loganalyzer

# Run the app
python3 app.py

# Detach from screen (app keeps running)
# Press Ctrl + A, then D

# To re-attach later
screen -r loganalyzer
```

---

## 🧪 Testing the App

A `sample.log` file is included in this repo. Use it to test the upload and see the dashboard in action.

You can also test with any real log files from:
- `/var/log/syslog`
- `/var/log/auth.log`
- Any application log file

---

## ⚙️ Run Locally (Without EC2)

If you want to run this on your local machine first:

```bash
# Clone the repo
git clone https://github.com/<your-username>/log-analyzer.git
cd log-analyzer

# Install dependencies
pip3 install -r requirements.txt

# Run the app
python3 app.py

# Visit
http://localhost:5000
```

---

## 🌟 Want to Go Further? (Bonus Practice)

Once the basic deployment works, try these to level up your DevOps skills:

- [ ] **Dockerize the app** — Write a `Dockerfile` and run it as a container
- [ ] **Add Nginx** — Set up Nginx as a reverse proxy on port 80
- [ ] **systemd service** — Auto-start the app when EC2 reboots
- [ ] **GitHub Actions CI/CD** — Auto-deploy on every `git push`
- [ ] **HTTPS with SSL** — Use Let's Encrypt + Certbot for a free SSL certificate

---

## 📌 Common Issues & Fixes

| Problem | Fix |
|--------|-----|
| Can't connect to `<ip>:5000` | Check EC2 Security Group — port 5000 must be open |
| `Permission denied` on `.pem` file | Run `chmod 400 your-key.pem` |
| `pip3: command not found` | Run `sudo apt install python3-pip -y` |
| App stops after closing SSH | Use `nohup` or `screen` as shown in Step 7 |
| `Address already in use` error | Run `sudo fuser -k 5000/tcp` then restart |

---

## 📄 License

This project is open source and free to use for learning purposes.

---

## 🙋 Author

Made for practicing Python app deployment on AWS EC2.  
Feel free to fork, modify, and use this project for your own learning! ⭐
