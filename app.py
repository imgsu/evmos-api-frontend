import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
import os
import urllib

st.set_page_config(
    page_title="Evmos EVM API Frontend",
    page_icon=":microscope:",
    layout="centered",
    initial_sidebar_state="auto",
)
st.title("Evmos EVM API Frontend")
st.markdown("img#1916 | evmos1afcdd60zqyntzl96kfwg3n2d0sms0yg0ure2lv")

page = st.radio("", ["API Frontend", "Top Token Holders"])
action_df = pd.read_csv("action_list.csv", header=0)
token_df = pd.read_csv("token_list.csv", header=0)
evmos_url = "https://evm.evmos.org/api"

if page == "API Frontend":
    st.info("Frontend for Evmos EVM API built using [Streamlit](https://streamlit.io). Taken from Evmos API reference documentation found [here](https://evm.evmos.org/api-docs).")

    col1, col2 = st.columns([1,2])
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
        addresscol1, addresscol2 = st.columns([2, 1])
        addressHash = addresscol1.text_input("Enter address hash here", "0x98217A5BDba4AD22bDFcf5129f39748036e56f4D")
        query = query.replace("{addressHash}", addressHash)

    if "transactionHash" in params:
        transactionHash = st.text_input("Enter transaction hash here", "0xfd8b6fc7b592994115a68f7b3028e2df4073192419603d481d5e571011dc7b59")
        query = query.replace("{transactionHash}", transactionHash)

    if "contractAddressHash" in params:
        contractAddressHash = st.text_input("Enter contract address hash here", "0xbc83B501aE7937f6E923790130f71A1868D7B055")
        query = query.replace("{contractAddressHash}", contractAddressHash)

    if "date" in params:
        datecol1, datecol2 = st.columns([1,4])
        date = datecol1.date_input("Enter query date")
        query = query.replace("{date}", str(date))

    if "fromBlockNumber, toBlockNumber" in params:
        fromblock, toblock = st.columns([1,1])
        fromBlockNumber = fromblock.number_input("Enter from block number", min_value=0, value=2165403)
        toBlockNumber = toblock.number_input("Enter to block number", min_value=1, value=2165404)
        query = query.replace("{fromBlockNumber}", str(fromBlockNumber))
        query = query.replace("{toBlockNumber}", str(toBlockNumber))
    elif "blockNumber" in params:
        blockcol1, blockcol2 = st.columns([1,2])
        blockNumber = blockcol1.number_input("Enter block number", min_value=0, value=2165403)
        query = query.replace("{blockNumber}", str(blockNumber))

    if "blockTimestamp" in params:
        stampcol1, stampcol2 = st.columns([2,1])
        blockTimestamp = stampcol1.number_input("Enter block timestamp", min_value=0)
        search = stampcol2.select_slider("Search before/after timestamp", options=["before", "after"])
        query = query.replace("{blockTimestamp}", str(blockTimestamp))
        query = query.replace("{before/after}", str(search))

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

elif page == "Top Token Holders":
    st.info("Displays top token holders for a given contract address.")
    select_token = st.selectbox("Choose a token or enter a custom contract below", token_df["name"])
    token_index = token_df[token_df["name"] == select_token].index[0]
    custom_contract = st.text_input("Enter custom contract address (optional)", "")
    token_query = token_df.at[token_index, "query"]
    if custom_contract:
        token_query = "?module=token&action=getTokenHolders&contractaddress=" + str(custom_contract)
        select_token = custom_contract

    query_url = evmos_url + token_query
    st.write("Query URL:", query_url)
    query = requests.get(query_url)

    if query.ok:
        result = query.json()
    else:
        query.raise_for_status()

    result_df = pd.json_normalize(result, record_path=['result'])

    st.subheader(str(select_token))
    st.dataframe(result_df)

    st.download_button(
        label="Download data as JSON",
        data=result_df.to_json(),
        file_name='result.json',
        mime='text/json',
    )