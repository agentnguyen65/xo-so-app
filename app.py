import streamlit as st
import datetime
from typing import Dict, Any

# =================================================================
#           PHẦN 1: LOGIC API (Đang bị thiếu trong file của bạn)
# =================================================================

def fetch_lottery_result(date_str: str, province: str) -> Dict[str, str]:
    """
    Hàm mô phỏng việc gọi dữ liệu kết quả xổ số (thay thế cho API thực tế).
    
    LƯU Ý: Đang sử dụng dữ liệu MÔ PHỎNG. Khi triển khai thực tế, 
    bạn cần thay thế bằng API truy vấn kết quả xổ số trực tiếp.
    """
    # Dữ liệu mô phỏng cố định cho mục đích demo UI (ví dụ cho 12/11/2025 tại TP.HCM)
    if date_str == "12/11/2025" and province == "TP.HCM":
        return {
            "DB": "886655", # Đặc biệt
            "G1": "123456",
            "G2": "778899",
            "G3_1": "010101",
            "G3_2": "020202",
            "G8": "55"
        }
    return {} # Không có kết quả

def check_ticket(ticket_number: str, results: Dict[str, str]) -> str:
    """
    Thực hiện Đối chiếu số vé với kết quả (Logic SPG lõi).
    """
    if not results:
        return "Không tìm thấy dữ liệu kết quả xổ số để đối chiếu."
    
    ticket_number = ticket_number.strip()

    # 1. Giải Đặc Biệt (6 số)
    if ticket_number == results.get("DB"):
        return f"🎉 **Chúc mừng!** Vé số **{ticket_number}** đã trúng **Giải ĐẶC BIỆT** (2 Tỷ VNĐ)!"

    # 2. Giải Phụ Đặc Biệt (Trùng 5 số cuối, sai 1 số đầu)
    db_last_5 = results.get("DB")[-5:]
    ticket_last_5 = ticket_number[-5:]
    
    if ticket_last_5 == db_last_5 and ticket_number[0] != results.get("DB")[0]:
        return f"✨ **Chúc mừng!** Vé số **{ticket_number}** đã trúng **Giải PHỤ ĐẶC BIỆT** (50 Triệu VNĐ)!"

    # 3. Giải Khuyến Khích
    if ticket_number[0] == results.get("DB")[0] and ticket_number != results.get("DB"):
        return f"💡 **Chúc mừng!** Vé số **{ticket_number}** đã trúng **Giải KHUYẾN KHÍCH** (6 Triệu VNĐ)!"

    # Thêm logic dò các giải khác nếu cần
    
    return "💔 **Rất tiếc.** Chúc bạn may mắn lần sau."

# =================================================================
#           PHẦN 2: GIAO DIỆN STREAMLIT (Phần bạn đã cung cấp)
# =================================================================

st.set_page_config(page_title="Dò Vé Số Tự Động", layout="centered")
st.title("🎰 Dò Vé Số Tự Động")
st.markdown("---")

# **DANH SÁCH TỈNH MIỀN NAM ĐÃ CẬP NHẬT**
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
                
                # Gọi API Logic (LƯU Ý: Hàm đã được định nghĩa ở PHẦN 1)
                results = fetch_lottery_result(date_str, province)
                final_result = check_ticket(ticket_number, results)
                
                st.success("✅ **Hoàn tất đối chiếu!**")
                st.balloons()
                st.subheader(f"Kết quả dò vé {ticket_number}:")
                st.info(final_result)

