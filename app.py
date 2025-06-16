import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Set the URL of the government website (Example: U.S. Bureau of Economic Analysis or The Conference Board)
URL = "https://www.conference-board.org/data/consumerconfidence.cfm"

# Function to scrape consumer confidence data
def scrape_consumer_confidence():
    response = requests.get(URL)
    if response.status_code != 200:
        st.error("Failed to retrieve data.")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # This part depends on the actual structure of the website
    # The following is a placeholder example, you'll need to inspect the page to find the correct tags/classes
    try:
        table = soup.find("table")
        headers = [th.text.strip() for th in table.find_all("th")]
        rows = []
        for tr in table.find_all("tr")[1:]:
            cells = [td.text.strip() for td in tr.find_all("td")]
            if cells:
                rows.append(cells)

        df = pd.DataFrame(rows, columns=headers)
        return df
    except Exception as e:
        st.error(f"Error parsing data: {e}")
        return None

# Streamlit app
st.title("U.S. Consumer Confidence Index Dashboard")

st.write("This app scrapes and displays the latest U.S. Consumer Confidence data from The Conference Board.")

data = scrape_consumer_confidence()
if data is not None:
    st.dataframe(data)
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='consumer_confidence.csv',
        mime='text/csv',
    )
