
---

```markdown
# ☀️ Weather Wear: Weather-Based Outfit Recommender

Weather Wear is an interactive, multi-lingual Streamlit application that provides intelligent outfit recommendations tailored to local weather conditions and your personal style choice. It balances standard tabular suggestions loaded from a CSV dataset with an integrated AI Chat Assistant powered by Ollama, Gemini, or OpenAI to answer any additional styling queries.

🚀 **Live Demo:** [Deploy on Streamlit](https://l8zwapp7gqwdkbarjcwkken.streamlit.app/)

---

## ✨ Features

* **Real-time Weather Fetching:** Integrates with the OpenWeather API to extract precise meteorological data (temperature, humidity, wind speed) for any city.
* **Smart Outfit Matching:** References a local dataset (`outfit_recommendations.csv`) to provide immediate suggestions spanning Tops, Bottoms, Footwear, Outerwear, and Accessories.
* **Multi-lingual Localization (i18n):** Full UI translation support for **English**, **Hindi (हिन्दी)**, and **Malayalam (മലയാളം)**.
* **Hybrid AI Chat Assistant:** A floating, mobile-responsive chat widget allowing users to toggle between locally hosted models (**Ollama**) and cloud APIs (**OpenAI GPT-4**, **Gemini 2.5 Flash**).

---

## 🛠️ Tech Stack & Dependencies

* **Frontend Framework:** Streamlit
* **Data Processing:** Pandas
* **Networking/APIs:** Requests, Urllib3
* **LLM Integrations:** `google-genai`, `openai`

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/weather-wear.git](https://github.com/your-username/weather-wear.git)
cd weather-wear

```

### 2. Set Up a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

```

*(Ensure your `requirements.txt` contains `streamlit`, `pandas`, `requests`, `google-genai`, and `openai`)*

### 3. Add Necessary Local Files

Ensure the following files are located in your root directory alongside `app.py`:

* `ww_logo.png` (The branding application logo)
* `outfit_recommendations.csv` (The tabular dataset populated with styles)

The CSV should contain these columns at minimum:
`weather_condition`, `style`, `top`, `bottom`, `footwear`, `accessory`, `outerwear`, `notes`

### 4. Configure API Keys

Create a `.streamlit/secrets.toml` file to store your OpenWeather API credentials safely:

```toml
OPENWEATHER_API_KEY = "your_openweather_api_key_here"

```

### 5. Run the Application

```bash
streamlit run app.py

```

---

## 🤖 Using the AI Chat Assistant

The chatbot panel supports 3 execution providers:

1. **Ollama:** Expects an instance running locally on `http://localhost:11434` (defaults to `llama3`).
2. **Gemini:** Requires a valid Google GenAI API Key running `gemini-2.5-flash`.
3. **OpenAI:** Requires a valid OpenAI API Key running `gpt-4.1-mini`.

---

## 📝 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

```

---

### Key Adjustments Handled for You:
* **Live App Link Integration:** The link you requested is seamlessly wired up in the header badge/text format.
* **Clean Setup Documentation:** Separated steps for dataset population requirements, file assets, and API structure.

```