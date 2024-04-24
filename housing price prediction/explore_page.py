import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

@st.cache
def load_data():
    df = pd.read_csv("VN_housing_dataset.csv")
    df['Diện tích'] = df['Diện tích'].str.rstrip('m²')

# Chuyển đổi cột 'Diện tích' thành dạng số và chuyển các giá trị không thể chuyển đổi thành NaN
    df['Diện tích'] = pd.to_numeric(df['Diện tích'], errors='coerce')

# Xóa các hàng mà có giá trị không phải số
    df = df.dropna(subset=['Diện tích'])
    df['Giá/m2'] = df['Giá/m2'].str.rstrip(' triệu/m²')

# Chuyển đổi cột 'Giá/m2' thành dạng số và chuyển các giá trị không thể chuyển đổi thành NaN
    df['Giá/m2'] = pd.to_numeric(df['Giá/m2'], errors='coerce')

# Xóa các hàng mà có giá trị không phải số
    df = df.dropna(subset=['Giá/m2'])

    df['Dài'] = df['Dài'].str.rstrip('m')
    df['Dài'] = pd.to_numeric(df['Dài'], errors='coerce')
    df['Rộng'] = df['Rộng'].str.rstrip('m')

# Chuyển đổi cột 'Rộng' thành dạng số và chuyển các giá trị không thể chuyển đổi thành NaN
    df['Rộng'] = pd.to_numeric(df['Rộng'], errors='coerce')
    df.rename(columns={'Diện tích': 'Diện tích(m²)'}, inplace=True)

# Thay đổi tên cột 'Giá/m2' thành 'Giá/m2(triệu/m²)'
    df.rename(columns={'Giá/m2': 'Giá/m2(triệu/m²)'}, inplace=True)

    df.rename(columns={'Rộng': 'Rộng(m)'}, inplace=True)
    df.rename(columns={'Dài': 'Dài(m)'}, inplace=True)
    df = df.dropna()
    df.isnull().sum()
    df['Tổng giá tiền(tỷ đồng)'] = df['Diện tích(m²)'] * df['Giá/m2(triệu/m²)']
    df['Số phòng ngủ'] = pd.to_numeric(df['Số phòng ngủ'].str.rstrip('phòng'), errors='coerce').astype('Int64')
    df = df.dropna(subset=['Số phòng ngủ'])

# Chuyển đổi cột 'Số tầng' thành dạng số nguyên và chuyển các giá trị không thể chuyển được thành NaN
    df['Số tầng'] = pd.to_numeric(df['Số tầng'], errors='coerce').astype('Int64')
    country_map = shorten_categories(df['Địa chỉ'].value_counts(), 20)
    df['Địa chỉ'] = df['Địa chỉ'].map(country_map)
    df['Địa chỉ'].value_counts()
    df.drop(df.index[df["Địa chỉ"] == "Other"], inplace=True)
    df = df[["Địa chỉ","Quận","Phường", "Loại hình nhà ở", "Số tầng", "Số phòng ngủ", "Diện tích(m²)","Dài(m)","Rộng(m)","Tổng giá tiền(tỷ đồng)"]]
    mask = ~df["Quận"].str.startswith("Huyện")

# Lọc DataFrame để chỉ chứa các hàng không thỏa mãn mask
    df = df[mask]
    return df

df = load_data()

def show_explore_page():
    st.title("Biểu đồ trung bình giá tiền căn nhà theo quận")

    # Groupby và tính trung bình giá tiền theo quận
    data = df.groupby(["Quận"])["Tổng giá tiền(tỷ đồng)"].mean().sort_values(ascending=True)

    # Tạo biểu đồ cột
    plt.figure(figsize=(10, 6))
    data.plot(kind='bar', color='skyblue')

    # Đặt nhãn cho trục x và trục y
    plt.xlabel('Quận')
    plt.ylabel('Trung bình giá tiền căn nhà từng quận')

    # Đặt tiêu đề cho biểu đồ
    plt.title('Tổng giá trị căn nhà từng quận')

    # Hiển thị biểu đồ trong Streamlit
    st.pyplot(plt)

    st.title("Biểu đồ Loại hình nhà ở vs Tổng giá tiền")

    # Vẽ biểu đồ đường
    plt.figure(figsize=(10, 6))
    for house_type in df['Loại hình nhà ở'].unique():
        df_house_type = df[df['Loại hình nhà ở'] == house_type]
        plt.plot(df_house_type['Tổng giá tiền(tỷ đồng)'], label=house_type)

    plt.xlabel('Index')
    plt.ylabel('Tổng giá tiền(tỷ đồng)')
    plt.title('Biểu đồ đường Loại hình nhà ở vs Tổng giá tiền')
    plt.legend()
    plt.grid(True)

    # Hiển thị biểu đồ trong ứng dụng Streamlit
    st.pyplot(plt)

    total_price_by_district = df.groupby('Quận')['Tổng giá tiền(tỷ đồng)'].sum()
     # Vẽ biểu đồ tròn
    st.title("Biểu đồ thể hiện số lượng nhu cầu bán nhà đất của các quận")
    plt.figure(figsize=(10, 6))
    plt.pie(total_price_by_district, labels=total_price_by_district.index, autopct='%1.1f%%', startangle=140)
    plt.title('Biểu đồ tròn thể hiện số lượng nhu cầu bán nhà đất của các quận')
    plt.axis('equal')  #  Đảm bảo biểu đồ tròn

    # Hiển thị biểu đồ trong ứng dụng Streamlit
    st.pyplot(plt)

        
    # Tạo đồ thị mật độ
    st.title("Biểu đồ Diện tích và Tổng giá tiền")
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='Diện tích(m²)', y='Tổng giá tiền(tỷ đồng)', cmap='viridis', fill=True)

    # Đặt nhãn cho trục x và trục y
    plt.xlabel('Diện tích(m²)')
    plt.ylabel('Tổng giá tiền(tỷ đồng)')

    # Đặt tiêu đề cho biểu đồ
    plt.title('Biểu đồ mật độ thể hiện mối quan hệ giữa Diện tích và Tổng giá tiền')

    # Hiển thị biểu đồ
    st.pyplot(plt)

