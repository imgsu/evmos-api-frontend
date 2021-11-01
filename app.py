import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
import os
import urllib

st.title("Evmos API Frontend")
#st.image("evmos_logo.jpg")
evmos_url = "https://evm.evmos.org/api"

col1, col2 = st.columns(2)
select_module = col1.selectbox("Choose a module", ["account", "logs", "token", "stats", "block", "contract", "transaction"])

if select_module == "account":
    action_list = ["eth_get_balance", "balance", "balancemulti", "pendingtxlist", "txlist", "txlistinternal", "tokentx", "tokenbalance", "tokenlist", "getminedblocks", "listaccounts"]
else:
    action_list = []

select_action = col2.selectbox("Choose an action", action_list)
address_input = st.text_input("Enter address here", "0x98217A5BDba4AD22bDFcf5129f39748036e56f4D")
query_url = evmos_url + f"?module={select_module}&action={select_action}&address={address_input}"
st.write(query_url)
query = requests.get(query_url)

if query.ok:
    result = query.json()
else:
    query.raise_for_status()

result_df = pd.json_normalize(result)
st.write("Result")
st.dataframe(result_df)

st.download_button(
    label="Download data as JSON",
    data=result_df.to_json(),
    file_name='result.json',
    mime='text/json',
)
