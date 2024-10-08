# mengimport semua modul yang dbutuhkan
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

def create_weather_workingday_df(df, isWorkingdaybyInt):
    weather_workingday_df = df[df["workingday"] == isWorkingdaybyInt].groupby(["weathersit"])["cnt"].sum().sort_values(ascending=False).reset_index()
    if not (weather_workingday_df["weathersit"] == 4).any():
        new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
        weather_workingday_df = pd.concat([weather_workingday_df, new_row], ignore_index=True)

    weather_workingday_df.rename(columns={"weathersit": "index_cuaca", "cnt": "jumlah_pengguna"}, inplace=True)

    return weather_workingday_df

# membuat kategori waktu agar tidak terlalu banyak bar chartnya
def create_byHourGroup_df(df):
    df["hr_group"] = df.hr.apply(lambda x: "Pagi Hari" if x >= 5 and x < 11
                                  else ("Siang Hari" if x >= 11 and x < 15
                                        else "Sore Hari" if x >= 15 and x < 20
                                        else "Malam Hari"))

    byHourGroup_df = df.groupby(by="hr_group")["cnt"].sum().reset_index()
    byHourGroup_df.rename(columns={"hr_group": "categories", "cnt": "jumlah_pengguna"}, inplace=True)

    return byHourGroup_df

# membaca file csv day dan hour
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")


column = "dteday"
day_df.sort_values(by=column, inplace=True)
day_df.reset_index(drop=True, inplace=True)
hour_df.sort_values(by=column, inplace=True)
hour_df.reset_index(drop=True, inplace=True)

day_df[column] = pd.to_datetime(day_df[column])
hour_df[column] = pd.to_datetime(hour_df[column])


min_date = day_df[column].min()
max_date = day_df[column].max()

with st.sidebar:
    st.image("bike.jpg")#menambahkan logo rental sepeda

    start_date, end_date = st.date_input(label="Time", min_value=min_date.date(), max_value=max_date.date(), value=[min_date.date(), max_date.date()])


main_df = day_df[(day_df[column] >= pd.to_datetime(start_date)) & (day_df[column] <= pd.to_datetime(end_date))]
second_df = hour_df[(hour_df[column] >= pd.to_datetime(start_date)) & (hour_df[column] <= pd.to_datetime(end_date))]


weather_workingday_df = create_weather_workingday_df(main_df, 1)
byHourGroup_df = create_byHourGroup_df(second_df)


st.header("Bike Sharing Dashboard :globe_with_meridians: ")


st.subheader("Pengaruh Cuaca di Hari Kerja")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    labels_detail = [
        'Clear or Partly cloudy', 
        'Mist and/or Cloudy', 
        'Light Rain and/or Thunderstorm or Light Snow', 
        'Heavy Rain or Snow and Fog'
    ]
    size = weather_workingday_df["jumlah_pengguna"]
    pie = plt.pie(size, startangle=0)
    title = plt.title("Jumlah Pengguna Sepeda di Setiap Cuaca\nPada Hari Bekerja Tahun 2011-2012", fontsize=20)
    title.set_ha("center")
    plt.legend(
        pie[0], 
        labels_detail, 
        bbox_to_anchor=(0.65,-0.05), 
        loc="lower right", 
        bbox_transform=plt.gcf().transFigure
    )
    st.pyplot(fig)


st.subheader("Jumlah Pengguna Sepeda Berdasarkan Waktu")

fig = plt.figure(figsize=(10, 5))

sns.barplot(y="jumlah_pengguna", x="categories", hue="categories", data=byHourGroup_df.sort_values(by="jumlah_pengguna", ascending=False), dodge=False)
plt.title("Jumlah Pengguna di Setiap Kategori Waktu", loc="center", fontsize=17)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis="x", labelsize=12)
plt.legend(title="Kategori Waktu")
st.pyplot(fig)