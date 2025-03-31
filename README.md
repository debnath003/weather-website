# Real-Time-Weather-Website

## Weather App

### Technologies Used

#### Frontend
- **[HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)**: Structuring the content of web pages.
- **[CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)**: Styling web pages for visual appeal.
- **[Bootstrap](https://getbootstrap.com/)**: A CSS framework for creating responsive and mobile-first web pages.
- **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)**: Adding interactivity to the web pages.

#### Backend
- **[Django (Python)](https://www.djangoproject.com/)**: A high-level Python web framework for building the backend.
- **[SQLite](https://www.sqlite.org/)**: A lightweight database for storing saved cities.
- **[OpenWeatherMap API](https://openweathermap.org/api)**: Fetching real-time weather data.

---

### How It Works
1. The website fetches weather data from the **OpenWeatherMap API**.
2. Users select a **city** and a **time** from the dropdown menus.
3. The website sends a request to the **OpenWeatherMap API** for the selected city.
4. The API returns the weather information for that city.
5. The website displays the weather information to the user.

---

### Unique Feature: Saving and Managing Cities
- Users can **save cities** with custom names.
- Users can **view a list** of their saved cities.
- Users can **delete cities** from their saved list.
- The saved cities are stored in the **SQLite database**.
- Users can **view weather details** of their saved cities.

---

### Access the Website
You can access the project here: [Weather App](https://pdebnath.pythonanywhere.com/)

---

### License
This project is open-source and available under the **[GPL 3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html)**.
