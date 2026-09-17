# 💧 Smart Water Irrigator

### 🌱 Production-Ready Smart Agriculture & Irrigation System

Smart Water Irrigator is a full-stack web application designed for **smart and efficient agriculture**. It calculates precise irrigation requirements using real-time weather data and recommends suitable crops based on climatic and environmental conditions.

The system helps farmers make data-driven irrigation decisions, reduce water wastage, and improve crop productivity.

---

## 🚀 Features

### 🔐 User Authentication
- Secure user registration and login
- Session management
- Role-based access for users and administrators

### 👨‍🌾 Farmer Dashboard
- Enter field and crop-related information
- Calculate irrigation requirements instantly
- View personalized agricultural insights

### 🌦️ Real-Time Weather Module
- Fetches real-time weather information
- Uses **OpenWeatherMap API**
- Weather-based irrigation calculations

### 🌾 Crop Recommendation Engine
- Recommends suitable crops based on climatic conditions
- Uses data analytics to provide dynamic suggestions
- Helps farmers select appropriate crops for their environment

### 📊 History & Analytics
- Store previous irrigation calculations
- Track irrigation history
- Visualize data using **Chart.js**
- Analyze water requirements over time

### 📄 PDF Report Export
- Generate professional irrigation reports
- Download reports in PDF format
- Useful for maintaining agricultural records

### 🛠️ Admin Panel
- Monitor overall application usage
- Manage crop information
- View system activity and user data

---

## 🏗️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, Flask |
| Database | MySQL |
| Frontend | HTML5, CSS3, JavaScript |
| UI Framework | Bootstrap 5 |
| Data Visualization | Chart.js |
| Weather API | OpenWeatherMap API |
| Reports | PDF Export |

---

## 📂 Project Structure

```text
Smart-Water-Irrigator/
│
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── .env.example
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md
