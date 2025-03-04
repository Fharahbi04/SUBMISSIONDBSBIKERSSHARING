import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df_hari = pd.read_csv("df_hari.csv")
df_jam = pd.read_csv("df_jam.csv")

kelompok_Musim={
    1: "Sangat sedikit pengguna",
    2: "banyak pengguna",
    3: "sangat banyak pengguna",
    4: "sedikit pengguna",
}
df_hari["Kategori"]= df_hari["season"].map(kelompok_Musim)

jumlah_bins = [0, 2000, 4000, df_hari["cnt"].max()]
jumlah_labels = ["Rendah","Menengah","Tinggi"]
df_hari["jumlah_kategori"] = pd.cut(df_hari["cnt"], bins=jumlah_bins, labels=jumlah_labels)

suhu_bins=[0, 0.3, 0.6, df_hari["temp"].max()]
suhu_labels = ["Dingin","Sedang","Panas"]
df_hari["suhu_kategori"] = pd.cut(df_hari["temp"], bins=suhu_bins, labels=suhu_labels)

with st.sidebar:
        st.image("bike.png",width=300)
        st.title("DBS BIKERS-SHARING")
        
        option = st.selectbox(
        "DATA YANG INGIN DI TAMPILKAN",
        ("Clustering",
        "Perbandingan Peminjam",
        "Pola pengguaan sepeda", 
        "Pengaruh cuaca dan musim(perhari)", 
        "Pengaruh musim dan hubungannya dengan cuaca (perhari)",
    ),
        ) 

if option == "Clustering":
    selected_season = st.sidebar.selectbox("Pilih Kategori Peminjam Sepeda ", df_hari["Kategori"].unique())
    selected_temp = st.sidebar.selectbox("Pilih kategori suhu luar", df_hari["suhu_kategori"].unique())

    filtered_data = df_hari[(df_hari["Kategori"]== selected_season)& (df_hari["suhu_kategori"]==selected_temp)]
    st.subheader("Tren Peminjaman Sepeda Harian")
    st.line_chart(df_hari.set_index("dteday")["cnt"])
    st.subheader("Data Peminjam sepeda")
    st.write(filtered_data[["dteday", "Kategori", "suhu_kategori", "jumlah_kategori", "cnt"]])


    st.subheader("Distibusi Jumlah Peminjaman Sepeda")
    plt.figure(figsize=(8, 5))
    sns.countplot(x=df_hari["jumlah_kategori"], palette="coolwarm")
    plt.title("Kategori Total Peminjaman")
    plt.xlabel("Kategori Peminjaman")
    plt.ylabel("Jumlah Hari")
    st.pyplot(plt)

    st.subheader("Pengaruh Suhu")
    plt.figure(figsize=(8, 5))
    sns.countplot(x=df_hari["suhu_kategori"], palette="coolwarm")
    plt.title("Kategori Total Peminjaman")
    plt.xlabel("Kategori Suhu")
    plt.ylabel("Jumlah Hari")
    st.pyplot(plt)




elif option == "Perbandingan Peminjam":
    st.subheader (" Perbandingan Peminjam Registered dan Casual")
    pengguna_jumlah=df_hari[['casual','registered']].sum()
    pengguna_rerata=df_hari[['casual','registered']].mean()

    fig,axes = plt.subplots(1,2,figsize=(14,5))
    
    sns.barplot(x=pengguna_jumlah.index,y=pengguna_jumlah, palette='viridis',ax=axes[0])
    axes[0].set_title('Jumlah Pengguna Sepeda(hari) Berdasarkan Tipe', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Tipe Pengguna')
    axes[0].set_ylabel('Jumlah Pengguna')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    sns.barplot(x=pengguna_rerata.index,y=pengguna_rerata, palette='viridis',ax=axes[1])
    axes[1].set_title('Rata-rata Pengguna Sepeda(hari) Berdasarkan Tipe', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Tipe Pengguna')
    axes[1].set_ylabel('Rata-rata Pengguna')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)



elif option == "Pola pengguaan sepeda":
    st.subheader (" Pola Pengguna Sepeda(Perjam)")
    pengguna_jumlah=df_jam[['holiday','weekday','workingday',]].value_counts().reset_index()
    pengguna_jumlah.columns=['holiday','weekday','workingday','count']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='weekday', y='count', hue='workingday', data=pengguna_jumlah, palette='viridis')

    plt.title("Holiday,weekday,workingday",fontsize=13,fontweight="bold")
    plt.xlabel("Weekday/Hari biasa(0 = minggu,6 = sabtu)",fontsize=13,fontweight="bold")
    plt.ylabel("jumlah",fontsize=13,fontweight="bold")
    plt.legend(title="workingday",fontsize=13)
    st.pyplot(plt)

    st.subheader ("Pola Pengguna Sepeda(Perhari)")
    pengguna_jumlah=df_hari[['holiday','weekday','workingday',]].value_counts().reset_index()
    pengguna_jumlah.columns=['holiday','weekday','workingday','count']
    plt.figure(figsize=(10, 6))
    sns.barplot(x='weekday', y='count', hue='workingday', data=pengguna_jumlah, palette='viridis')

    plt.title("Holiday,weekday,workingday",fontsize=13,fontweight="bold")
    plt.xlabel("Weekday/Hari biasa(0 = minggu,6 = sabtu)",fontsize=13,fontweight="bold")
    plt.ylabel("jumlah",fontsize=13,fontweight="bold")
    plt.legend(title="workingday",fontsize=13)
    st.pyplot(plt)
    st.text("Working day: 1 = Hari bukan akhir pekan atau hari libur,0 = Akhir Pekan atau Hari Libur")




elif option == "Pengaruh cuaca dan musim(perhari)":
    st.subheader ("Pengaruh Cuaca Dengan Pemakaian Sepeda(Perhari)")
    df_Cuace = df_hari.groupby('cuaca').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': ['sum','mean']
    }).reset_index()
    df_Cuace.columns = ['cuaca', 'casual', 'registered', 'cnt_sum', 'cnt_mean']
    plt.figure(figsize=(9, 9))
    plt.pie(df_Cuace['cnt_mean'], labels=df_Cuace['cuaca'], autopct='%1.1f%%', colors=sns.color_palette("viridis",len(df_Cuace)))
    plt.title("Rata-rata Pengguna Sepeda Berdasarkan Cuaca",fontsize=13,fontweight="bold")
    st.pyplot(plt)



elif option == "Pengaruh musim dan hubungannya dengan cuaca (perhari)":
    st.subheader ("Pengaruh Cuaca dan Musim Dengan Pemakaian Sepeda(Perhari)")
    df_musim = df_hari.groupby('Musim').agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': ['sum','mean']
    }).reset_index()
    df_musim.columns = ['Musim', 'casual', 'registered', 'cnt_sum', 'cnt_mean']
    plt.figure(figsize=(9, 9))
    plt.pie(df_musim['cnt_sum'], labels=df_musim['Musim'], autopct='%1.1f%%', colors=sns.color_palette("viridis",len(df_musim)))
    plt.title("Rata-rata Pengguna Sepeda Berdasarkan Musim",fontsize=13,fontweight="bold")
    st.pyplot(plt)

    st.subheader ("Hubungan Cuaca dan Musim Pada Peminjam Sepeda(Perhari)")
    df_pengaruh=df_hari.groupby(by=["Musim", "cuaca"]).agg({
     'casual': 'sum',
    'registered': 'sum',
    'cnt': ['sum','mean']
    }).reset_index()
    df_pengaruh.columns = ['Musim', 'cuaca', 'casual', 'registered', 'cnt_sum', 'cnt_mean']
    df_pivot = df_pengaruh.pivot(index='Musim', columns='cuaca', values='cnt_sum')
    plt.figure(figsize=(9, 9))
    sns.heatmap(df_pivot, annot=True, cmap='coolwarm', fmt='.0f')
    plt.title("Hubungan jumlah Pengguna Sepeda Berdasarkan Musim dan Cuaca",fontsize=13,fontweight="bold")
    st.pyplot(plt)
    st.text("Semakin Merah maka semakin banyak pengguna,sebaliknya semakin biru maka semakin sedikit")

st.caption('Copyright (c) MC179D5Y0226-Muhammad Fharahbi Fachri')