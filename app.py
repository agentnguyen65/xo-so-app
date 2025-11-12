import streamlit as st
import datetime
from typing import Dict, Any

# ... (API Logic giữ nguyên) ... 
# ... (Hàm fetch_lottery_result và check_ticket giữ nguyên) ...

# --- GIAO DIỆN STREAMLIT MỚI ---

st.set_page_config(page_title="Dò Vé Số Tự Động", layout="centered")
st.title("🎰 Dò Vé Số Tự Động")
st.markdown("---")

# **DANH SÁCH TỈNH MIỀN NAM ĐÃ CẬP NHẬT (THAY ĐỔI Ở ĐÂY)**
# Danh sách này bao gồm các tỉnh thường quay và luân phiên
province_options = [
    "TP.HCM", "Đồng Nai", "Cần Thơ", "Sóc Trăng", "Tiền Giang", "Kiên Giang",
    "Đà Lạt", "Bạc Liêu", "Bến Tre", "Vũng Tàu", "Đồng Tháp", "Cà Mau", 
    "Tây Ninh", "An Giang", "Bình Thuận", "Long An", "Bình Phước", "Hậu Giang",
    "Trà Vinh", "Vĩnh Long", "Bình Dương", "Ninh Thuận", "Phú Yên"
]

# Cột nhập liệu
col1, col2 = st.columns(2)

with col1:
    # INPUT 1: Ngày/Tháng/Năm
    lottery_date = st.date_input(
        "Ngày Xổ Số", 
        datetime.date.today(),
        max_value=datetime.date.today(),
        help="Chọn ngày đã in trên vé số của bạn."
    )
    
with col2:
    # INPUT 2: Tỉnh
    # SỬ DỤNG DANH SÁCH MỚI
    province = st.selectbox(
        "Tỉnh/Thành Phố",
        province_options,
        help="Chọn tỉnh đã in trên vé số của bạn."
    )

# INPUT 3: Số vé
ticket_number = st.text_input(
    "Số Vé (6 chữ số)",
    max_chars=6,
    placeholder="Nhập 6 số in trên vé...",
    help="Chỉ chấp nhận số có 6 chữ số."
)

st.markdown("---")

# Nút "Tạo kết quả"
if st.button("🔍 Dò Kết Quả Vé Số", type="primary", use_container_width=True):
    # ... (Logic xử lý nút bấm giữ nguyên) ...
    # Chuẩn hóa dữ liệu đầu vào
    date_str = lottery_date.strftime("%d/%m/%Y")
    
    if len(ticket_number) != 6 or not ticket_number.isdigit():
        st.error("Vui lòng nhập **đúng 6 chữ số** của vé số.")
    else:
        # Kiểm tra Giờ Xổ (Theo logic Bước 2)
        draw_time = datetime.time(16, 30, 0)
        now_time = datetime.datetime.now().time()
        
        # Chỉ kiểm tra giờ nếu ngày hôm nay
        if lottery_date == datetime.date.today() and now_time < draw_time:
            st.warning(f"⚠️ **Chưa tới giờ xổ!** Kết quả sẽ được công bố sau **16:30** hôm nay ({province}).")
        elif lottery_date > datetime.date.today():
             st.warning("⚠️ **Ngày dò vé là ngày trong tương lai.** Vui lòng chờ đến ngày đó.")
        else:
            # Khung hiển thị kết quả
            with st.spinner('Đang đối chiếu kết quả...'):
                input_data = {
                    "Ngày/Tháng/Năm": date_str,
                    "Tỉnh": province,
                    "Số vé": ticket_number
                }
                
                # Gọi API Logic
                results = fetch_lottery_result(date_str, province)
                final_result = check_ticket(ticket_number, results)
                
                st.success("✅ **Hoàn tất đối chiếu!**")
                st.balloons()
                st.subheader(f"Kết quả dò vé {ticket_number}:")
                st.info(final_result)
