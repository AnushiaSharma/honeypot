# 🛡️ Matrix Honeypot System

A multi-layer **Honeypot System** designed to simulate vulnerable services and capture unauthorized access attempts.  
This project helps in understanding attacker behavior, logging intrusion attempts, and visualizing them through a secure admin dashboard.

---

## 🚀 Features

- 🖥️ **SSH Honeypot**
  - Fake SSH server to capture login attempts
  - Logs username, password, and IP

- 🌐 **Web Honeypot**
  - Fake login page to trap attackers
  - Captures credentials and stores them securely

- 📊 **Admin Dashboard**
  - Matrix-style hacker UI 😈
  - Displays:
    - IP Address
    - Username & Password
    - Country & City (IP tracking)
    - Timestamp

- 🔐 **Admin Authentication**
  - Secure login system for dashboard access
  - Session-based authentication

- 🌍 **IP Geolocation Tracking**
  - Detects attacker’s country & city using IP API

- 🧾 **Logging System**
  - Stores attack data in SQLite database
  - Logs connection attempts

---

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **SQLite**
- **HTML, CSS (Matrix UI)**
- **Socket Programming**
- **Requests (for IP tracking)**

---

## 📂 Project Structure
honeypot/
│── app.py
│── ssh_honeypot.py
│── web_honeypot.py
│── database.py
│── logger.py
│── templates/
│ ├── login.html
│ ├── admin_login.html
│ └── dashboard.html
│── .gitignore
│── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/honeypot.git
cd honeypot

2️⃣ Create virtual environment
python -m venv honeypot_env

3️⃣ Activate environment
# Windows
honeypot_env\Scripts\activate
4️⃣ Install dependencies
pip install flask requests
5️⃣ Run the application
python app.py
🌐 Access
Login Page (Honeypot):
http://localhost:8080
Admin Panel:
http://localhost:8080/admin
🔐 Security Note

Sensitive files such as:

attack.log
database.db

are excluded using .gitignore to prevent exposure of captured data.

⚠️ Disclaimer

This project is created for educational and research purposes only.
Do NOT deploy it publicly without proper security measures.

🎯 Expected Outcome
Capture unauthorized login attempts
Analyze attacker behavior
Visualize attack data via dashboard
Demonstrate real-world cybersecurity concepts
👩‍💻 Author

Anushia Sharma

💡 Future Improvements
🗺️ Live attacker map visualization
📊 Attack analytics (graphs & stats)
🔔 Real-time alerts
🌍 Public deployment using ngrok
⭐ If you like this project

Give it a star ⭐ on GitHub!