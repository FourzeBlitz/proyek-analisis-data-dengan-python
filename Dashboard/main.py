import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import numpy as np

sns.set_theme(style="dark")

# load dataset ori
all_df = pd.read_csv("Dashboard\hour.csv")

# convert to datetime format
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()


# sidebar
with st.sidebar:

    st.title(":moyai: Bike Sharing :bike:")

    start_date, end_date = st.date_input(
        label="Pick a date range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )


main_df = all_df.drop("instant", axis=1)
alltime_df = main_df
main_df = main_df[
    (main_df["dteday"] >= str(start_date)) & (main_df["dteday"] <= str(end_date))
]


st.title("The Bike Dataset")

filtered_data, raw_data = st.tabs(["Filtered Data", "Raw Data"])

with filtered_data:
    st.write(main_df)

with raw_data:
    st.write(all_df)


# line chart
st.header("Mean Penggunaan Sepeda")
byHour, byMonth, byYear = st.tabs(["hour", "month", "year"])

with byHour:
    with st.container():
        mean_user_df = main_df.groupby("hr")["cnt"].mean()
        st.line_chart(mean_user_df)
        st.markdown("x-axis: Jam")
        st.markdown("y-axis: Jumlah penggunaan sewa sepeda")
with byMonth:
    with st.container():
        mean_user_df = main_df.groupby("mnth")["cnt"].mean()
        st.line_chart(mean_user_df)
        st.markdown("x-axis: Bulan")
        st.markdown("y-axis: Jumlah penggunaan sewa sepeda")
with byYear:
    with st.container():
        mean_user_df = main_df.groupby("yr")["cnt"].mean()
        st.line_chart(mean_user_df)
        st.markdown("x-axis: Tahun")
        st.markdown("y-axis: Jumlah penggunaan sewa sepeda")


st.header("Customer Demographics")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        # Group by 'yr' column and calculate the sum of 'cnt' for each year
        total_pengguna_per_tahun = alltime_df.groupby("yr")["cnt"].sum().reset_index()

        # Replace the 'yr' values
        total_pengguna_per_tahun["yr"] = total_pengguna_per_tahun["yr"].replace(
            {0: 2011, 1: 2012}
        )

        # Mencari tahun dengan jumlah penggunaan sepeda terbanyak
        tahun_terbanyak = alltime_df.groupby("yr")["cnt"].sum().idxmax()
        jumlah_pengguna_terbanyak = alltime_df.groupby("yr")["cnt"].sum().max()

        tahun_tertinggi = 2011 if tahun_terbanyak == 0 else 2012
        st.subheader(":calendar: Tahun tertinggi: " + str(tahun_tertinggi))

    with col2:
        st.subheader("Penggunaan sewa sepeda pada tahun " + str(tahun_tertinggi))

col_sepeda_perTahun, col_sepeda_perBulan = st.columns(2)

with col_sepeda_perTahun:

    # Plot the bar chart
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.barplot(x="yr", y="cnt", data=total_pengguna_per_tahun, ax=ax)

    # Set title and labels
    ax.set_title("Jumlah Pengguna Sepeda per Tahun", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel("Tahun", fontsize=35)
    ax.tick_params(axis="x", labelsize=35)
    ax.tick_params(axis="y", labelsize=30)
    ax.ticklabel_format(style="plain", axis="y")

    # Display the plot using Streamlit
    st.pyplot(fig)
    with st.expander("See explanation"):
        st.markdown(
            """Ada peningkatan penggunaan sewa sepeda dari tahun 2011 ke 2012 sebesar :green[**64.88%**]
            """
        )

with col_sepeda_perBulan:

    best_month_of_aYear = alltime_df[alltime_df["yr"] == tahun_terbanyak]
    total_pengguna_per_bulan = (
        best_month_of_aYear.groupby("mnth")["cnt"].sum().reset_index()
    )

    fig, ax = plt.subplots(figsize=(20.3, 20))
    sns.histplot(
        x="mnth",
        weights="cnt",
        data=total_pengguna_per_bulan,
        ax=ax,
        kde=True,
        bins=12,
    )
    # sns.barplot(x="mnth", y="cnt", data=total_pengguna_per_bulan, ax=ax)

    # Set title and labels
    ax.set_title("Jumlah Pengguna Sepeda per Bulan", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel("Bulan", fontsize=35)
    ax.tick_params(axis="x", labelsize=35)
    ax.set_xticks(range(1, 13))
    ax.tick_params(axis="y", labelsize=30)
    ax.ticklabel_format(style="plain", axis="y")

    # Display the plot using Streamlit
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.markdown(
            """Penggunaan sewa sepeda mulai naik pada :blue[bulan 4] kemudian memuncak pada :blue[bulan 9] kemudian mengalami penurunan, namun jumlah penggunaan pada :blue[bulan 12] masih lebih tinggi dari bulan 1 dan 2. Bisa dilihat masih :blue[ada kenaikan dalam 1 tahun], untuk tahun kedepannya starting penggunaan sewa sepeda mungkin akan sama / lebih tinggi dari bulan 12.
            """
        )


# penggunaan sepeda di 4 musim
st.header("Jumlah Penggunaan sewa sepeda di berbagai macam musim")
col_pie_musim, col_bar_musim = st.tabs(["Pie Chart Musim", "Bar Chart Musim"])
df_meanUser_perSeason = alltime_df.groupby("season")["cnt"].mean()
df_sumUser_perSeason = alltime_df.groupby("season")["cnt"].sum()
with col_pie_musim:
    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(
        df_sumUser_perSeason.values,
        labels=df_sumUser_perSeason.index.map(
            {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
        ),
        autopct="%1.1f%%",
        startangle=90,
        explode=(0, 0, 0.1, 0),
    )
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
    st.pyplot(fig)

with col_bar_musim:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        df_sumUser_perSeason.index.map(
            {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
        ),
        df_sumUser_perSeason.values,
        color="skyblue",
    )

    # Add labels and formatting
    ax.set_title("Sum of Users per Season")
    ax.set_xlabel("Season")
    ax.set_ylabel("Sum of Users")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)


# penggunaan sepeda di 4 kondisi cuaca
st.header("Penggunaan sewa sepeda di berbagai macam kondisi cuaca")
col_pie_cuaca, col_bar_cuaca = st.tabs(["Pie Chart Cuaca", "Bar Chart Cuaca"])
df_meanUser_perWeather = alltime_df.groupby("weathersit")["cnt"].mean()
df_sumUser_perWeather = alltime_df.groupby("weathersit")["cnt"].sum()
labels = [
    "Clear, Few clouds",
    "Mist + Cloudy",
    "Light Snow, Light Rain",
    "Heavy Rain, Snow + Fog",
]
with col_pie_cuaca:
    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(
        df_meanUser_perWeather.values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        explode=(0.1, 0, 0, 0),
    )
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
    st.pyplot(fig)

with col_bar_cuaca:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, df_sumUser_perWeather.values, color="skyblue")

    # Add labels and formatting
    ax.set_title("Sum of Users per Weather Situation")
    ax.set_xlabel("Weather Situation")
    ax.set_ylabel("Sum of Users")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)


# rata-rata penggunaan sewa sepeda terhadap berbagai macam suhu
st.header("Rata-rata Penggunaan Sewa Sepeda terhadap Berbagai Macam Suhu")
temperatures = main_df.copy()
temperatures["temp"] = temperatures["temp"] * 41
bike_rental_usage = main_df["cnt"]

mean_user_perTemp = temperatures.groupby("temp")["cnt"].mean()

fig, ax = plt.subplots()
ax.plot(mean_user_perTemp.index, mean_user_perTemp.values)

# Set labels and title
ax.set_xlabel("Temperature")
ax.set_ylabel("Bike Rental Usage")

# Display the plot using Streamlit
st.pyplot(fig)
