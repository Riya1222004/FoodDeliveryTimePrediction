import streamlit as st
import pandas as pd
import folium as fl
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from bs4 import BeautifulSoup
from weather import *
from distance import *
from givedata import *
import xgboost as xgb
import cv2

def get_pos(lat, lng):
    return lat, lng

df = pd.read_csv('restaurant.csv')

st.title("Food Delivery Time Prediction")
st.divider()

html_code = """
<script>
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            var locationResult = lat + " " + lon;
            document.getElementById("location-result").innerHTML = locationResult;
        });
    } else {
        document.getElementById("location-result").innerHTML = "Geolocation is not available in this browser.";
    }
</script>
<p id="location-result"></p>
"""

soup = BeautifulSoup(html_code, 'html.parser')
st.components.v1.html(html_code)
data = soup.find(id="location-result")
data = [23.12844355089839, 72.54451307841649]
d1=data
st.write("Your location: ",data[0],data[1])
st.write("Select location:")
mumbai_coords = [19.0760, 72.8777]
m = fl.Map(location=mumbai_coords,zoom_start=12)
m.add_child(fl.LatLngPopup())
map = st_folium(m, height=350, width=700)
if map.get("last_clicked"):
    data = get_pos(map['last_clicked']['lat'], map['last_clicked']['lng'])

if data is not None:
    st.write("Your selected location:", data[0], data[1])
else:
    data=d1

select_rest = st.selectbox('From where you want to order food?', df[' name'].values)
x="Razzberry Rhinoceros"
# if st.button('Select'):
# if select_rest==x:
st.write("Your selected restaurant is ", select_rest)
selected_restaurant = df[df[" name"] == select_rest]
restaurant_lat = selected_restaurant[" latitude"].iloc[0]
restaurant_lng = selected_restaurant[" longitude"].iloc[0]
restaurant_address = selected_restaurant[" address"].iloc[0]
st.write("You will get your food shortly :)")
st.write("Restaurant Location:")

restaurant_map = fl.Map(location=mumbai_coords, zoom_start=10)
fl.Marker([restaurant_lat, restaurant_lng], popup=restaurant_address).add_to(restaurant_map)
fl.Marker([data[0], data[1]]).add_to(restaurant_map)

folium_static(restaurant_map)

st.write("Restaurant Address:", restaurant_address)
st.write("Distance : ",haversine_distance(restaurant_lat,restaurant_lng,data[0],data[1]),"Km")
distance=haversine_distance(restaurant_lat,restaurant_lng,data[0],data[1])
if distance>=30.0:
    st.write("No delivery available now..")
else:
    wheather=get_weather(data[0],data[1])
    rating,veh_con,traffic_int,veh_int=result()
    model=xgb.XGBRegressor()
    model.load_model("xgb_boost.json")
    print("Delivery time: ",model.predict([[rating,veh_con,wheather,distance,traffic_int,veh_int]]),'min')
    st.write("Delivery time: ",model.predict([[rating,veh_con,wheather,distance,traffic_int,veh_int]])[0],'min')

img = cv2.imread('1.png')
st.image(img, caption='Mean Squared Error in various ML Algorithms', use_column_width=True)

img = cv2.imread('2.png')
st.image(img, caption='Mean Absolute Error in various ML Algorithms', use_column_width=True)

img = cv2.imread('3.png')
st.image(img, caption='Feature Importance', use_column_width=True)

img = cv2.imread('4.png')
st.image(img, caption='Actual vs. Predicted Plot', use_column_width=True)

img = cv2.imread('5.png')
st.image(img, caption='Residual Plot', use_column_width=True)


img = cv2.imread('6.png')
st.image(img, caption='Learning Curve Plot', use_column_width=True)

img = cv2.imread('7.png')
st.image(img, caption='Model Complexity Plot', use_column_width=True)