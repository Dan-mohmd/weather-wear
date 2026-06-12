# app.py

import streamlit as st
import pandas as pd
import requests
import urllib3
import base64
import requests
import os
from pathlib import Path
from datetime import datetime
from requests.exceptions import RequestException
from urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.write("Available secrets:", list(st.secrets.keys()))
# -----------------------------
# App Config
# -----------------------------
st.set_page_config(
    page_title="Weather Wear",
    page_icon="☀️",
    layout="wide"
)


# -----------------------------
# Navbar / Header
# -----------------------------
st.markdown(
    """
    <style>
    .brand-bar {
        background-color: #1f2937;
        color: #ffffff;
        border-radius: 10px;
        display: flex;
        align-items: center;
        gap: 18px;
        width: 100%;
    }

    .brand-icon-slot {
        width: 62px;
        height: 62px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        flex-shrink: 0;
    }

    .brand-icon-slot img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .brand-title {
        font-size: 38px;
        font-weight: 700;
        white-space: nowrap;
    }

    .chat-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 65px;
        height: 65px;
        border-radius: 50%;
        background-color: #25D366;
        color: white;
        font-size: 30px;
        border: none;
        cursor: pointer;
        z-index: 9999;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    .chat-box {
        position: fixed;
        bottom: 100px;
        right: 20px;
        width: 350px;
        height: 450px;
        background: white;
        border-radius: 15px;
        padding: 10px;
        z-index: 9999;
        border: 1px solid #ddd;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Nav-bar
# -----------------------------

nav_left, nav_right = st.columns([5, 1])

def get_base64_image(image_path):
    image_bytes = Path(image_path).read_bytes()
    return base64.b64encode(image_bytes).decode()

logo_base64 = get_base64_image("ww_logo.png")

nav_left, nav_right = st.columns([5, 1])

with nav_left:
    st.markdown(
        f"""
        <div class="brand-bar">
            <div class="brand-icon-slot">
                <img src="data:image/png;base64,{logo_base64}" alt="Weather Wear Logo">
            </div>
            <div class="brand-title">Weather Wear</div>
        </div>
        """,
        unsafe_allow_html=True
    )
# --------------------------
# OPEN BUTTON
# --------------------------

col1, col2 = st.columns([10, 1])

with nav_right:
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    if st.button("💬 Chat Assistant"):
        st.session_state.chat_open = not st.session_state.chat_open

# -----------------------------
# Weather Code Mapping
# -----------------------------
WEATHER_CODES = {
    0: "Sunny",
    1: "Mostly Sunny",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Foggy",
    48: "Foggy",
    51: "Light Rain",
    53: "Rainy",
    55: "Rainy",
    61: "Light Rain",
    63: "Rainy",
    65: "Heavy Rain",
    71: "Snowy",
    73: "Snowy",
    75: "Heavy Snow",
    80: "Rainy",
    81: "Rainy",
    82: "Heavy Rain",
    95: "Stormy",
    96: "Stormy",
    99: "Stormy"
}


# -----------------------------
# API Transformer Class
# -----------------------------
class WeatherTransformer:
    def __init__(self):
        self.api_key = "1a36b2d05745ab30a90785c8657896d7"

        if not self.api_key:
            self.api_key = st.text_input(
                "Enter OpenWeather API Key",
                type="password"
            )

        if not self.api_key:
            st.warning("Please enter an OpenWeather API key.")
            st.stop()
            
    def get_coordinates(self, location):
        geo_url = "https://api.openweathermap.org/geo/1.0/direct"

        params = {
            "q": location,
            "limit": 1,
            "appid": self.api_key
        }

        try:
            response = requests.get(geo_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if not data:
                return None

            result = data[0]

            return {
                "name": result.get("name", location),
                "country": result.get("country", ""),
                "latitude": result["lat"],
                "longitude": result["lon"]
            }

        except RequestException as error:
            st.error("Could not fetch location data.")
            st.caption(f"Technical details: {error}")
            return None

    def fetch_weather(self, latitude, longitude):
        weather_url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(weather_url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()

        except RequestException as error:
            st.error("Could not fetch weather data.")
            st.caption(f"Technical details: {error}")
            return None

    def transform_weather_data(self, location_info, weather_data):
        weather_main = weather_data["weather"][0]["main"]
        weather_description = weather_data["weather"][0]["description"]
        main = weather_data["main"]
        wind = weather_data.get("wind", {})

        df = pd.DataFrame([{
            "location": location_info["name"],
            "country": location_info["country"],
            "latitude": location_info["latitude"],
            "longitude": location_info["longitude"],
            "temperature": main["temp"],
            "feels_like": main["feels_like"],
            "humidity": main["humidity"],
            "weather_condition": normalize_weather(weather_main).title(),
            "weather_description": weather_description.title(),
            "wind_speed": wind.get("speed", 0),
            "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        return df

    def get_weather_dataframe(self, location):
        location_info = self.get_coordinates(location)

        if location_info is None:
            return None

        weather_data = self.fetch_weather(
            location_info["latitude"],
            location_info["longitude"]
        )

        if weather_data is None:
            return None

        weather_df = self.transform_weather_data(location_info, weather_data)
        weather_df.to_csv("weather_data.csv", index=False)

        return weather_df
# -----------------------------
# Helper Functions
# -----------------------------
def normalize_weather(condition):
    condition = str(condition).lower()

    if "thunderstorm" in condition or "storm" in condition:
        return "stormy"
    if "rain" in condition or "drizzle" in condition:
        return "rainy"
    if "clear" in condition or "sun" in condition:
        return "sunny"
    if "cloud" in condition:
        return "cloudy"
    if "snow" in condition:
        return "snowy"
    if "mist" in condition or "fog" in condition or "haze" in condition:
        return "foggy"

    return condition


def load_outfit_dataset(file_path):
    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df


def recommend_outfit(outfit_df, weather_condition, style):
    weather_key = normalize_weather(weather_condition)

    df = outfit_df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    required_columns = [
        "weather_condition",
        "style",
        "top",
        "bottom",
        "footwear",
        "accessory",
        "outerwear",
        "notes"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"Missing columns in dataset: {missing_columns}")
        return pd.DataFrame()

    df["weather_condition"] = df["weather_condition"].astype(str).str.lower()
    df["style"] = df["style"].astype(str).str.lower()

    filtered = df[
        (df["weather_condition"].str.contains(weather_key, na=False)) &
        (df["style"] == style.lower())
    ]

    return filtered

# -----------------------------
# Main App
# -----------------------------

# Weather consoles

input_col, style_col = st.columns([1, 1])

with input_col:
    location = st.text_input("Enter Location", value="Delhi")

with style_col:
    style = st.selectbox(
        "Choose Outfit Style",
        ["Casual", "Formal", "Sporty", "Party", "Traditional"]
    )

left_space, button_col, right_space = st.columns([2, 1, 2])

with button_col:
    search_button = st.button("Fetch Weather", use_container_width=True)


st.subheader("Weather Based Outfit Recommender")

outfit_file = "outfit_recommendations.csv"

try:
    outfit_df = load_outfit_dataset(outfit_file)
except FileNotFoundError:
    st.error("Could not find outfit_recommendations.csv. Place it in the same folder as app.py.")
    st.stop()


if search_button:
    st.session_state.weather_loaded = True
    st.session_state["weather_api_failed"] = False

    transformer = WeatherTransformer()

    with st.spinner("Fetching weather data..."):
        weather_df = transformer.get_weather_dataframe(location)

    if weather_df is None:
        if st.session_state.get("weather_api_failed"):
            st.stop()

        st.error("Location not found. Please enter a valid city or place name.")
        st.stop()

    weather = weather_df.iloc[0]
    if "weather_data" not in st.session_state:
        st.session_state.weather_data = None

    if "weather_loaded" not in st.session_state:
        st.session_state.weather_loaded = False
    
    st.session_state.weather_data = weather.to_dict()
    st.session_state.weather_loaded = True
    st.session_state["style"] = style

    current_temperature = float(weather["temperature"])
    

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Location", f"{weather['location']}, {weather['country']}")
    col2.metric("Weather", weather["weather_condition"])
    col3.metric("Temperature", f"{current_temperature} °C")
    col4.metric("Humidity", f"{weather['humidity']}%")

    temp_chart_df = pd.DataFrame({
        "Weather Info": ["Current Temperature"],
        "Temperature °C": [current_temperature]
    })

    # Create recommendations before trying to display them
    recommendations = recommend_outfit(
    outfit_df=outfit_df,
    weather_condition=weather["weather_condition"],
    style=style
    )
    

    st.write("### Outfit Suggestions")

    

    if recommendations.empty:
        st.warning("No exact outfit match found for this weather, temperature, and style.")
    else:
        for _, row in recommendations.head(1).iterrows():
            st.session_state["recommended_outfit"] = {
            "top": row["top"],
            "bottom": row["bottom"],
            "footwear": row["footwear"],
            "accessory": row["accessory"],
            "outerwear": row["outerwear"],
            "notes": row["notes"]
            }
            st.success("Recommended Outfit")

            st.write(f"**Top:** {row['top']}")
            st.write(f"**Bottom:** {row['bottom']}")
            st.write(f"**Footwear:** {row['footwear']}")
            st.write(f"**Accessory:** {row['accessory']}")
            st.write(f"**Outerwear:** {row['outerwear']}")
            st.write(f"**Notes:** {row['notes']}")

            st.divider()

else:
    st.info("Enter a location, choose your style, and click Get Recommendation.")
if st.session_state.get("weather_loaded", False):

    weather = st.session_state.weather_data

if "weather" not in st.session_state:
    st.session_state.weather = None

weather = st.session_state.weather

if st.session_state.weather:
    st.write(st.session_state.weather)

    # show metrics
# ------------------

# ------------------
# AI Chat-bot
# ------------------

import streamlit as st
import requests
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
from google import genai

# --------------------------
# SESSION STATES
# --------------------------

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "provider" not in st.session_state:
    st.session_state.provider = "Ollama"

# --------------------------
# AI FUNCTIONS
# --------------------------

st.markdown("""
<style>
/* Mobile-style floating chat window */
.st-key-mobile_chat_box {
    position: fixed;
    right: 24px;
    bottom: 24px;
    width: 390px;
    height: 640px;
    z-index: 9999;
    background: #0e1117;
    border: 1px solid #30363d;
    border-radius: 18px;
    padding: 16px;
    overflow-y: auto;
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.45);
}

/* Make it fit small screens */
@media (max-width: 520px) {
    .st-key-mobile_chat_box {
        right: 10px;
        left: 10px;
        bottom: 10px;
        width: auto;
        height: 85vh;
    }
}

/* Reduce spacing inside the chat box */
.st-key-mobile_chat_box h3 {
    margin-top: 0;
}

.st-key-mobile_chat_box [data-testid="stChatInput"] {
    margin-bottom: 0;
}
</style>
""", unsafe_allow_html=True)

# ------------------------

def ask_ollama(prompt, model):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )

        return r.json()["response"]

    except Exception as e:
        return str(e)


def ask_openai(prompt, api_key):
    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return str(e)


def ask_gemini(prompt, api_key):
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# --------------------------
# CHAT POPUP
# --------------------------

if st.session_state.chat_open:

    with st.container(border=True, key="mobile_chat_box"):

        top1, top2 = st.columns([8, 1])

        with top1:
            st.markdown("### AI Assistant")

        with top2:
            if st.button("✕"):
                st.session_state.chat_open = False
                st.rerun()

        provider = st.selectbox(
            "Provider",
            ["Ollama", "Gemini", "OpenAI"],
            key="provider"
        )

        if provider == "Ollama":

            model = st.text_input(
                "Model",
                "llama3",
                key="ollama_model"
            )

        elif provider == "Gemini":
            st.text_input(
                "Gemini Key",
                type="password",
                key="api_key"
            )

        else:

            st.text_input(
                "OpenAI Key",
                type="password",
                key="api_key"
            )

        st.divider()

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input(
            "Ask anything..."
        )

        if prompt:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.chat_message("user"):
                st.write(prompt)

            with st.spinner("Thinking..."):

                if provider == "Ollama":

                    answer = ask_ollama(
                        prompt,
                        st.session_state.ollama_model
                    )
                
                elif provider == "Gemini":

                    answer = ask_gemini(
                        prompt,
                        st.session_state.api_key
                    )

                else:

                    answer = ask_openai(
                        prompt,
                        st.session_state.api_key
                    )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()
