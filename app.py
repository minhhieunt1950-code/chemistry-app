import streamlit as st
from mendeleev import element
from chempy import balance_stoichiometry
import re

# 1. Cấu hình trang - Chế độ hiển thị rộng
st.set_page_config(page_title="Hóa Học Pro", page_icon="🧪", layout="wide")

st.title("🧪 Trợ Lý Hóa Học Thông Minh")

# Tạo các Tab để giao diện gọn gàng
tab1, tab2, tab3 = st.tabs(["🔍 Tra cứu nguyên tố", "⚖️ Cân bằng & Tính toán", "📚 Kiến thức"])

# --- TAB 1: TRA CỨU ---
with tab1:
    st.header("🔍 Tra cứu nguyên tố")
    # Sử dụng Session State để tránh lỗi hiển thị bảng đỏ sai thời điểm
    symbol_input = st.text_input("Nhập ký hiệu (Ví dụ: Fe, Al, Cu):", "Fe").strip()

    if symbol_input:
        el_data = None
        try:
            el_data = element(symbol_input)
        except:
            el_data = None

        if el_data:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tên nguyên tố", el_data.name)
                st.write(f"**Số hiệu nguyên tử:** {el_data.atomic_number}")
                st.write(f"**Nguyên tử khối:** {el_data.atomic_weight:.2f}")
            with col2:
                st.write("**Cấu hình electron:**")
                try:
                    # Lấy chuỗi thô (VD: 1s2 2s2 2p6...)
                    raw_conf = str(el_data.ec)

                    # SỬA LỖI TẠI ĐÂY:
                    # Dùng Regex tìm các số đứng sau chữ cái s, p, d, f và thêm dấu mũ ^
                    # Ví dụ: s2 sẽ thành s^{2}
                    fixed_conf = re.sub(r'([spdf])(\d+)', r'\1^{\2}', raw_conf)

                    # Hiển thị bằng LaTeX chuẩn
                    st.latex(fixed_conf)
                except:
                    st.write("Đang tải dữ liệu...")
        else:
            # Thông báo lỗi chỉ hiện khi không tìm thấy nguyên tố
            st.error("⚠️ Không tìm thấy nguyên tố. Vui lòng nhập đúng ký hiệu (VD: Mg, O, Ag).")

# --- TAB 2: CÂN BẰNG & TÍNH TOÁN ---
with tab2:
    st.subheader("🛠️ Cân bằng phương trình")
    pt = st.text_input("Nhập PT (Ví dụ: H2 + O2 -> H2O):", "KMnO4 + HCl -> KCl + MnCl2 + Cl2 + H2O")
    if pt and "->" in pt:
        try:
            left, right = pt.split("->")
            reac, prod = balance_stoichiometry(set(left.replace(" ", "").split("+")),
                                               set(right.replace(" ", "").split("+")))


            # Hàm format để hiển thị hệ số (số 1 sẽ ẩn đi cho đẹp)
            def f(d):
                return " + ".join([(f"{v}" if v > 1 else "") + k for k, v in d.items()])


            st.success(f"✅ Kết quả: {f(reac)} → {f(prod)}")
        except:
            st.warning("Hãy kiểm tra lại công thức các chất trong phương trình!")

    st.divider()
    st.subheader("⚖️ Tính số mol")
    st.write(r"Công thức: $n = \frac{m}{M}$")
    c_m, c_M = st.columns(2)
    m_v = c_m.number_input("Khối lượng m (gam):", min_value=0.0, value=5.6)
    M_v = c_M.number_input("M lớn (g/mol):", min_value=0.1, value=56.0)
    st.info(f"Số mol $n$ = **{m_v / M_v:.4f} mol**")

# --- TAB 3: KIẾN THỨC ---
with tab3:
    # Hình ảnh cấu tạo nguyên tử đã được fix link ổn định
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Stylised_Lithium_Atom.png/300px-Stylised_Lithium_Atom.png",
        width=250)
    st.write("**Ghi nhớ:**")
    st.markdown("- **Proton (p):** Trong hạt nhân, mang điện dương (+).")
    st.markdown("- **Neutron (n):** Trong hạt nhân, không mang điện.")
    st.markdown("- **Electron (e):** Ở lớp vỏ, mang điện âm (-).")