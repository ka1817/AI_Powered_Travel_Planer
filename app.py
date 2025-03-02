import streamlit as st
import requests

# Streamlit UI
st.title("🌍 AI-Powered Travel Planner")

# User Inputs
destination = st.text_input("✈️ Destination")
dates = st.text_input("📅 Travel Dates (e.g., March 15 - March 20)")
budget = st.selectbox("💰 Budget", ["Low", "Medium", "High"])
preferences = st.text_area("🎭 Preferences (e.g., adventure, culture, food, nightlife)")
num_travelers = st.number_input("👨‍👩‍👧‍👦 Number of Travelers", min_value=1, value=2)
accommodation = st.selectbox("🏨 Accommodation Type", ["Hotel", "Airbnb", "Hostel"])

# Submit Button
if st.button("Generate Itinerary"):
    payload = {
        "destination": destination,
        "dates": dates,
        "budget": budget,
        "preferences": preferences,
        "num_travelers": num_travelers,
        "accommodation": accommodation
    }

    response = requests.post("http://localhost:8000/generate_itinerary/", json=payload)

    if response.status_code == 200:
        itinerary = response.json()["itinerary"]
        st.subheader("🗺️ Your AI-Powered Itinerary")
        st.write(itinerary)
    else:
        st.error("❌ Error generating itinerary!")
