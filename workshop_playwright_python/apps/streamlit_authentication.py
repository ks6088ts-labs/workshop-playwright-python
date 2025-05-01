import streamlit as st
import yaml
from streamlit_authenticator import Authenticate, LoginError
from yaml.loader import SafeLoader

# Loading config file
with open(".streamlit/config.yaml", encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    cookie_key=config["cookie"]["key"],
    cookie_expiry_days=config["cookie"]["expiry_days"],
)

# Creating a login widget
try:
    result = authenticator.login()
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    st.write(f"Welcome *{st.session_state['name']}*")
    st.title("Some content")
    authenticator.logout("Logout", "main")
