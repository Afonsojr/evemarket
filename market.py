import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import json
import requests
from datetime import datetime


df = pd.read_csv("resource.csv")
dfprice = pd.read_csv("price.csv")

st.set_page_config(page_title="Eve Echoes Market", layout="wide", initial_sidebar_state="auto")


def main():
    # page_sidebar()
    page_body()

    return None


st.sidebar.header("Choose Resource")

area = st.sidebar.selectbox("Area", sorted(["HighSec", "LowSec", "NullSec"]))
# region = st.sidebar.selectbox("Region", sorted(df["Region"].unique()))

if area == "HighSec":
    region = st.sidebar.selectbox(
        "Region", sorted(df.loc[df["Area"] == "HighSec"]["Region"].unique().tolist())
    )
elif area == "LowSec":
    region = st.sidebar.selectbox(
        "Region", sorted(df.loc[df["Area"] == "LowSec"]["Region"].unique().tolist())
    )
else:
    region = st.sidebar.selectbox(
        "Region", sorted(df.loc[df["Area"] == "NullSec"]["Region"].unique().tolist())
    )

resource = st.sidebar.selectbox("Resource", sorted(df["Resource"].unique()))
brocas = st.sidebar.selectbox("Brocas", [4, 5, 6, 7, 8, 9, 10, 12])

st.sidebar.markdown("[Buy a coffe](https://nubank.com.br/pagar/147uyr/qAoqlRsrgI)")

choices = (area, region, resource, brocas)


#
df["Daily"] = df["Output"].apply(lambda x: (x * brocas) * 24)

peso = dfprice[dfprice["name"] == choices[2]]["height"].item()

df["M3_Day"] = df["Daily"].apply(lambda x: x * peso).astype(float)
price = dfprice[dfprice["name"] == choices[2]]["sell"].item()
id = dfprice[dfprice["name"] == choices[2]]["item_id"].item()
df["Price_Day"] = df["M3_Day"].apply(lambda x: x * price).astype(float)


def page_body():

    query = (
        df.loc[
            (df["Area"] == choices[0])
            & (df["Region"] == choices[1])
            & (df["Resource"] == choices[2])
        ]
        .sort_values(by="Output", ascending=False)
        .head(11)
    )

    best_planet = query["Planet Name"].head(1).item()
    best_output = query["Output"].head(1).item()
    daily_farm = query["Daily"].head(1).item()

    # best_output = df.loc[df["Resource"] == choices[1]].max()
    media_output = df.loc[(df["Resource"] == choices[2]) & (df["Area"] == choices[0])][
        "Output"
    ].mean()

    st.markdown(
        f"_Best Planet_: **{best_planet}** - Output: **{best_output}** - Prod/day: **{daily_farm:.2f}**"
    )

    st.write(
        f"_Average_ **{choices[2]}** in **{choices[0]}**: **{media_output:.2f}** - Current value: **{price}**"
    )

    st.table(
        query[
            ["Region", "Constellation", "Planet Name", "Output", "M3_Day", "Daily", "Price_Day"]
        ].head(10)
    )
    #
    r = requests.get(f"https://api.eve-echoes-market.com/market-stats/{id}")
    temp = json.loads(r.text)
    dfTemp = pd.DataFrame(temp)
    dfTemp = dfTemp.dropna()
    dfTemp["time"] = dfTemp["time"].apply(lambda x: datetime.fromtimestamp(x))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dfTemp["time"], y=dfTemp["sell"], name="Sell", mode="lines"))
    fig.add_trace(go.Scatter(x=dfTemp["time"], y=dfTemp["buy"], name="Buy", mode="lines"))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    st.table(dfTemp.describe())


if __name__ == "__main__":
    # page_sidebar()
    page_body()
