import korvai_basic as kb
import korvai_specific as ks
import streamlit as st
import numpy as np
import random as r
import pandas as pd


st.title("Welcome to Geeta's Korvai Calculator!",)
talam = st.sidebar.selectbox(
    "Select the Talam:",
    ["adi", "adi2", "rupakam", "misra chaapu", "khanda chaapu", "jumpa"])
edam = st.sidebar.slider('What is the Edam?', -10, 20, 1)
st.subheader("Some korvais in the AAA BCBCB format include: ")
my_korvai1 = kb.korvai_basic(talam,edam)
df1=my_korvai1.final_korvai()
st.table(df1)
st.subheader("Some korvais with specific purvangam templates include: ")
my_korvai2 = ks.korvai_specific(talam,edam)
df2=my_korvai1.final_korvai()
st.table(df2)
st.balloons()

