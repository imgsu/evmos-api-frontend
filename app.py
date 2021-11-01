import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
import os
import urllib

st.title("Evmos API Frontend")

action_df = pd.read_csv("action_list.csv", header=0)
#st.write(action_df)
evmos_url = "https://evm.evmos.org/api"

col1, col2 = st.columns(2)
select_action = col1.selectbox("Choose an action", action_df["action"])
action_index = action_df[action_df["action"] == select_action].index[0]
query = action_df.at[action_index, "query"]
description = action_df.at[action_index, "description"]
params = action_df.at[action_index, "params"]
st.code(query, language="")
st.info(description)
#st.write(params)

if "addressHash2, addressHash3" in params:
    multiAddressHash = st.text_input("Enter multiple address hashes here separated by commas", "0x98217A5BDba4AD22bDFcf5129f39748036e56f4D,0x1549d29D1d51A694Cd5bbC89bF2c5F86ea5cE151")
    query = query.replace("{addressHash1,addressHash2,addressHash3}", multiAddressHash)
elif "addressHash" in params:
    addressHash = st.text_input("Enter address hash here", "0x98217A5BDba4AD22bDFcf5129f39748036e56f4D")
    query = query.replace("{addressHash}", addressHash)

if "transactionHash" in params:
    transactionHash = st.text_input("Enter transaction hash here", "0xfd8b6fc7b592994115a68f7b3028e2df4073192419603d481d5e571011dc7b59")
    query = query.replace("{transactionHash}", transactionHash)

if "contractAddressHash" in params:
    contractAddressHash = st.text_input("Enter contract address hash here", "0xbc83B501aE7937f6E923790130f71A1868D7B055")
    query = query.replace("{contractAddressHash}", contractAddressHash)

if "date" in params:
    date = st.date_input("Enter query date")
    query = query.replace("{date}", str(date))

query_url = evmos_url + query
st.write("Query URL:", query_url)
query = requests.get(query_url)

if query.ok:
    result = query.json()
else:
    query.raise_for_status()

result_df = pd.json_normalize(result)
st.subheader("Result")
st.dataframe(result_df)

st.download_button(
    label="Download data as JSON",
    data=result_df.to_json(),
    file_name='result.json',
    mime='text/json',
)
