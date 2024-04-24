import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page


page = st.sidebar.selectbox("Khám phá hoặc Dự đoán", ("Dự đoán", "Khám phá dữ liệu"))

if page == "Dự đoán":
    show_predict_page()
else:
    show_explore_page()

