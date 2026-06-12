
# ☀️Weather Wear

Weather Wear is a weather-based outfit recommendation web app that helps users decide what to wear according to the current weather condition of a selected location. The app fetches live weather data using a free weather API, displays weather details such as condition and temperature, and recommends suitable outfits from a CSV dataset based on the weather and selected style.

## Features

* **Live Weather Fetching:** Gets real-time weather data for a user-entered location using a free weather API.
* **Weather-Based Outfit Suggestions:** Recommends clothes according to weather conditions such as sunny, rainy, cloudy, snowy, foggy, or stormy.
* **Style Selection:** Allows users to choose outfit styles such as casual, formal, sporty, party, or traditional.
* **CSV-Based Dataset:** Uses an outfit recommendation dataset stored in CSV format.
* **Weather Data Storage:** Saves fetched weather data into a CSV file using pandas.
* **Interactive Dashboard:** Built with Streamlit for a simple and user-friendly interface.
* **Temperature Display:** Shows the current temperature and weather details to the user.

---

## Tech Stack

The project is built using the following technologies:

* **Python:** Core programming language used for the application logic.
* **Streamlit:** Used to build the interactive web application.
* **Pandas:** Used for reading the outfit dataset, transforming weather data, and saving weather API data into CSV format.
* **Requests:** Used to fetch data from the weather API.
* **Open-Meteo API:** A free weather API used to get live weather details without requiring an API key.

---

## Dataset Format

The outfit recommendation dataset should be named:

```bash
outfit_recommendations.csv
```

The CSV file should contain columns similar to:

```csv
temp_min_c,temp_max_c,weather_condition,style,top,bottom,footwear,accessory,outerwear,notes
20,35,sunny,Casual,T-shirt,Jeans,Sneakers,Sunglasses,None,Light clothes are suitable for sunny weather
15,28,rainy,Formal,Shirt,Trousers,Formal shoes,Umbrella,Waterproof blazer,Carry rain protection
18,30,cloudy,Casual,Hoodie,Jeans,Sneakers,Watch,Light jacket,Comfortable outfit for cloudy weather
```

Main required columns:

* `weather_condition`
* `style`
* `top`
* `bottom`
* `footwear`
* `accessory`
* `outerwear`
* `notes`

---

## Getting Started

### Prerequisites

Make sure Python 3.8 or above is installed on your system.

Check your Python version:

```bash
python --version
```

---

## Installation

1. **Clone the repository:**

```bash
git clone https://code.swecha.org/Dan/weather-wear.git
cd weather-wear
```

2. **Create a virtual environment:**

```bash
python -m venv venv
```

3. **Activate the virtual environment:**

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

4. **Install the required dependencies:**

```bash
pip install streamlit pandas requests
```

5. **Add the dataset:**

Place your dataset file in the project folder:

```bash
outfit_recommendations.csv
```

---

## Usage

Run the Streamlit app using:

```bash
streamlit run app.py
```

After running the command, open the local app URL in your browser:

```bash
http://localhost:8501
```

---

## How It Works

1. The user enters a location in the sidebar.
2. The app fetches the location coordinates using the Open-Meteo Geocoding API.
3. The app fetches current weather data using the Open-Meteo Weather API.
4. The weather data is transformed using pandas and saved into a CSV file.
5. The app reads the outfit recommendation dataset.
6. Based on the current weather condition and selected style, the app displays a suitable outfit suggestion.

---

## Example Outfit Recommendation

For a rainy day with casual style, the app may suggest:

```text
Top: Hoodie
Bottom: Jeans
Footwear: Waterproof shoes
Accessory: Umbrella
Outerwear: Raincoat
Notes: Suitable for rainy weather. Carry rain protection.
```

---

## Project Structure

```bash
weather-wear/
│
├── app.py
├── outfit_recommendations.csv
├── weather_data.csv
├── README.md
└── requirements.txt
```

---

## Requirements File

You can create a `requirements.txt` file with:

```txt
streamlit
pandas
requests
```

Then install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Roadmap

* [ ] Add more outfit styles.
* [ ] Add outfit images for better visual recommendations.
* [ ] Add support for multiple outfit suggestions.
* [ ] Improve weather condition matching.
* [ ] Add user profile-based preferences.
* [ ] Add seasonal recommendations.

---

## Contributing

Contributions are welcome.

1. Fork the project.
2. Create a new feature branch:

```bash
git checkout -b feature/new-feature
```

3. Commit your changes:

```bash
git commit -m "Add new feature"
```

4. Push to your branch:

```bash
git push origin feature/new-feature
```

5. Open a Merge Request.

---

## Author

* **Dan** - Initial work and development

---

## License

This project is licensed under the MIT License.

---

## Project Status

**Active** - The project is currently working and hosted in Hugging-face.
Hugging-face URL : https://huggingface.co/spaces/spark-stack/weather-wear

```