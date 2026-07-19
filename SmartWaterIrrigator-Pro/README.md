# Smart Water Irrigator - Production Ready

A full-stack, production-ready web application designed for smart agriculture. It calculates precise irrigation requirements based on real-time weather data and recommends suitable crops using advanced data analytics.

## Features
- **User Authentication:** Secure registration, login, and session management.
- **Farmer Dashboard:** Input field data and receive instant insights.
- **Weather Module:** Real-time data from OpenWeatherMap.
- **Crop Recommendation Engine:** Dynamic suggestions based on climatic conditions.
- **History & Analytics:** Track past calculations and view Chart.js analytics.
- **PDF Export:** Download professional irrigation reports.
- **Admin Panel:** Monitor global usage and manage crops.

## Technology Stack
- **Backend:** Python Flask
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, JS, Bootstrap 5, Chart.js

## Local Setup

1. **Clone/Download the repository**
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup Database:**
   - Install MySQL Server on your machine.
   - Run `python database.py` to initialize the database and tables (this uses `schema.sql`).
4. **Configure Environment:**
   - Copy `.env.example` to `.env`.
   - Update your MySQL credentials and OpenWeatherMap API key in the `.env` file.
5. **Run Application:**
   ```bash
   python app.py
   ```
6. **Access:** Open `http://localhost:5000` in your browser.
## author 
 "Mayank Kushwaha "
 "Prajapati Sumit" 
