import streamlit as st
import pandas as pd
# import requests

df = pd.read_csv("resource.csv")

st.set_page_config(page_title="Eve Echoes Market", layout="wide", initial_sidebar_state="auto")


def main():
    # page_sidebar()
    page_body()

    return None


st.sidebar.header("Escolha o Recurso")
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
brocas = st.sidebar.selectbox("Brocas", [4, 5, 6, 7, 8, 9, 10])

choices = (area, region, resource, brocas)

df["Daily"] = df["Output"].apply(lambda x: (x * brocas) * 24)


def page_body():

    st.write(choices)

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

    st.markdown(f"*Melhor Planeta*: {best_planet} - {best_output} - {daily_farm:.2f}")

    st.write(f"Média de {choices[0]} = {media_output:.2f}")

    st.table(
        query[
            [
                "Region",
                "Constellation",
                "Planet Name",
                "Output",
                "Daily",
            ]
        ]
    )


if __name__ == "__main__":
    # page_sidebar()
    page_body()
