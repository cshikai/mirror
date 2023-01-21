#importing dependencies
import streamlit as st
import yaml
from query import UI_Querier
from upload import Uploader

st.set_page_config(layout="wide")

st.header("Information Retrieval")

tab1, tab2,  = st.tabs(["Upload", "Query"])

with open('./configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

with tab1:
    st.header("Upload Jsonls")
    uploaded_csv_supply_full = st.file_uploader('upload', type=['jsonl'], accept_multiple_files=True, key="supply_csv", label_visibility = "hidden")
    if uploaded_csv_supply_full:
        if st.button("Upload to database", key="supply_button"):
            uploader = Uploader(config)
            uploader.upload_all(uploaded_csv_supply_full)
with tab2:
    st.header("Query")
    sparse_csv = st.slider('Threshold', min_value=0.0, max_value=1.0, step=0.1, value=1.0, disabled=True, key="sparse_csv", label_visibility = "hidden")
    search_query = st.text_input('Query Text', placeholder = 'Enter Query Here', key="csv_query", label_visibility = "hidden")
    if st.button("Search", key="csv_query_button"):
        querier = UI_Querier(config)
        results = querier.send_query({"query": search_query})
        if results=={}:
            st.warning("No Documents Found")
        else:
            for r in results['search_result']:
                st.subheader(f"Confidence Score: {r['confidence_score']}")
                data = querier.retrieve_data(r['id'])
                st.write(data[0].content)
                st.write(f"(Source :{data[0].meta['source']})")