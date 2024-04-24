import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
regressor= data["model"]
le_diachi = data["le_diachi"]
le_loaihinhnha = data["le_loaihinhnha"]
le_quan = data["le_quan"]
le_phuong = data["le_phuong"]

def show_predict_page():
    st.title("Dự đoán giá nhà đất ở Hà Nội")

    st.write("""### Chúng ta cần thông tin để dự đoán""")

    cacdiachi = (
        "Đường Lạc Long Quân",      
       "Đường Lê Trọng Tấn",   
        "Đường Minh Khai",      
        "Đường Quan Nhân",     
        "Đường Đội Cấn",       
        "Đường Nguyễn Trãi",      
        "Đường Khương Trung",     
        "Đường Kim Giang",     
        "Đường Thái Hà",      
        "Đường Cầu Giấy",      
        "Đường Hoàng Văn Thái")
    
    cacphuong=("Phường Khương Trung", 
"Phường Ô Chợ Dừa", 
"Phường Minh Khai", 
"Phường Yên Hoà", 
"Phường Láng Hạ",  
"Phường Dương Nội" ,                               
"Phường Phú Đô",      
"Phường Cửa Đông",      
"Phường Đồng Xuân",     
"Phường Biên Giang",     )
    cacquan =(
  "Quận Đống Đa",   
"Quận Thanh Xuân",
"Quận Hà Đông", 
"Quận Cầu Giấy",
"Quận Hai Bà Trưng",
"Quận Hoàng Mai",
"Quận Ba Đình", 
"Quận Long Biên",  
"Quận Tây Hồ",   
"Quận Nam Từ Liêm",  
"Quận Bắc Từ Liêm",  
"Quận Hoàn Kiếm ",  )

    cacloaihinhnha= (
   "Nhà ngõ, hẻm",       
"Nhà mặt phố, mặt tiền",  
"Nhà phố liền kề",     
"Nhà biệt thự",      )
    
    diachi= st.selectbox("Đường",  cacdiachi)
    phuong= st.selectbox("Phường",  cacphuong)
    quan= st.selectbox("Quận",  cacquan)
    loaihinhnha= st.selectbox("Loại hình nhà",  cacloaihinhnha)
    sotang= st.slider("Số tầng ", 0, 50, 1)
    sophongngu= st.slider("Số phòng ngủ", 0, 10, 1)
    dientich = st.number_input("Diện tích(m²)", min_value=0.0, max_value=350.0, value=1.0)
    chieudai = st.number_input("Chiều dài ", min_value=0.0, max_value=8250.0, value=1.0)
    chieurong = st.number_input("Chiều rộng", min_value=0.0, max_value=4500.0, value=1.0)
    ok = st.button(" Dự đoán giá tiền nhà đất")
    if ok:
        X = np.array([[diachi, quan,phuong,loaihinhnha,sotang,sophongngu,dientich,chieudai, chieurong ]])
        X[:, 0] = le_diachi.transform(X[:, 0]).astype(float)
        X[:, 1] = le_quan.transform(X[:, 1]).astype(float)
        X[:, 2] = le_phuong.transform(X[:,2]).astype(float)
        X[:, 3] = le_loaihinhnha.transform(X[:, 3]).astype(float)
            # Chuyển đổi toàn bộ mảng thành kiểu dữ liệu float
        X = X.astype(float)

        salary = regressor.predict(X)
        formatted_salary = "{:,.2f}".format(salary[0])
        formatted_salary = formatted_salary.replace(",", ".")

        st.subheader(f"Giá tiền nhà đất là đ{formatted_salary}")

