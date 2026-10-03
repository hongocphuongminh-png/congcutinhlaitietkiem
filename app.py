import streamlit as st
st.image("logo.jpg", width=180)
import pandas as pd

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 APP TÍNH LÃI TIỀN GỬI TIẾT KIỆM_CỦA HẤU")
st.write(
    "Tính tiền lãi theo **lãi đơn** hoặc **lãi kép** "
    "với nhiều hình thức nhận lãi."
)

st.divider()

# ==============================
# NHẬP THÔNG TIN
# ==============================

st.subheader("📌 Thông tin khoản tiền gửi")

so_tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_lai = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_nhan = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# ==============================
# NÚT TÍNH TOÁN
# ==============================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo năm -> dạng thập phân
    lai_suat_nam = lai_suat / 100

    # ==============================
    # XÁC ĐỊNH SỐ KỲ
    # ==============================

    if hinh_thuc_nhan == "Lãnh lãi theo tháng":
        so_ky = ky_han
        lai_suat_ky = lai_suat_nam / 12
        ten_ky = "Tháng"

    elif hinh_thuc_nhan == "Lãnh lãi theo quý":
        so_ky = ky_han // 3
        lai_suat_ky = lai_suat_nam / 4
        ten_ky = "Quý"

        if ky_han % 3 != 0:
            st.warning(
                "Kỳ hạn không chia hết cho 3. "
                "Phần tháng lẻ sẽ được tính theo số tháng thực tế."
            )

    else:
        so_ky = 1
        lai_suat_ky = lai_suat_nam * ky_han / 12
        ten_ky = "Cuối kỳ"

    # ==============================
    # TÍNH LÃI ĐƠN
    # ==============================

    if hinh_thuc_lai == "Lãi đơn":

        tong_lai = so_tien_gui * lai_suat_nam * ky_han / 12

        tong_tien = so_tien_gui + tong_lai

        # Lãi định kỳ
        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            tien_lai_dinh_ky = (
                so_tien_gui * lai_suat_nam / 12
            )

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            tien_lai_dinh_ky = (
                so_tien_gui * lai_suat_nam / 4
            )

        else:
            tien_lai_dinh_ky = tong_lai

        # ==============================
        # TẠO BẢNG CHI TIẾT
        # ==============================

        data = []

        if hinh_thuc_nhan == "Lãnh lãi theo tháng":

            lai_luy_ke = 0

            for i in range(1, ky_han + 1):

                lai_ky = so_tien_gui * lai_suat_nam / 12
                lai_luy_ke += lai_ky

                data.append({
                    "Kỳ": f"Tháng {i}",
                    "Tiền gốc": so_tien_gui,
                    "Tiền lãi kỳ này": lai_ky,
                    "Lãi lũy kế": lai_luy_ke,
                    "Tổng gốc + lãi": so_tien_gui + lai_luy_ke
                })

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":

            lai_luy_ke = 0
            so_quy = ky_han // 3

            for i in range(1, so_quy + 1):

                lai_ky = so_tien_gui * lai_suat_nam / 4
                lai_luy_ke += lai_ky

                data.append({
                    "Kỳ": f"Quý {i}",
                    "Tiền gốc": so_tien_gui,
                    "Tiền lãi kỳ này": lai_ky,
                    "Lãi lũy kế": lai_luy_ke,
                    "Tổng gốc + lãi": so_tien_gui + lai_luy_ke
                })

        else:

            data.append({
                "Kỳ": "Cuối kỳ",
                "Tiền gốc": so_tien_gui,
                "Tiền lãi kỳ này": tong_lai,
                "Lãi lũy kế": tong_lai,
                "Tổng gốc + lãi": tong_tien
            })

    # ==============================
    # TÍNH LÃI KÉP
    # ==============================

    else:

        # Lãi kép:
        # Tiền cuối kỳ = P * (1 + r)^n
        #
        # Với:
        # P = tiền gốc
        # r = lãi suất mỗi kỳ
        # n = số kỳ

        if hinh_thuc_nhan == "Lãnh lãi theo tháng":

            so_ky = ky_han
            lai_suat_ky = lai_suat_nam / 12

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":

            # Nếu kỳ hạn không chia hết cho 3,
            # tính phần thời gian theo tháng ở cuối.
            so_ky = ky_han // 3
            lai_suat_ky = lai_suat_nam / 4

        else:

            so_ky = 1
            lai_suat_ky = lai_suat_nam * ky_han / 12

        data = []

        if hinh_thuc_nhan == "Lãnh lãi theo tháng":

            tien_hien_tai = so_tien_gui

            for i in range(1, ky_han + 1):

                tien_lai = tien_hien_tai * lai_suat_ky
                tien_hien_tai += tien_lai

                data.append({
                    "Kỳ": f"Tháng {i}",
                    "Tiền gốc đầu kỳ": tien_hien_tai - tien_lai,
                    "Tiền lãi kỳ này": tien_lai,
                    "Lãi lũy kế": tien_hien_tai - so_tien_gui,
                    "Tổng gốc + lãi": tien_hien_tai
                })

            tong_tien = tien_hien_tai
            tong_lai = tong_tien - so_tien_gui
            tien_lai_dinh_ky = data[-1]["Tiền lãi kỳ này"]

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":

            tien_hien_tai = so_tien_gui

            so_quy = ky_han // 3

            for i in range(1, so_quy + 1):

                tien_lai = tien_hien_tai * lai_suat_ky
                tien_hien_tai += tien_lai

                data.append({
                    "Kỳ": f"Quý {i}",
                    "Tiền gốc đầu kỳ": tien_hien_tai - tien_lai,
                    "Tiền lãi kỳ này": tien_lai,
                    "Lãi lũy kế": tien_hien_tai - so_tien_gui,
                    "Tổng gốc + lãi": tien_hien_tai
                })

            # Tính phần tháng lẻ nếu có
            thang_le = ky_han % 3

            if thang_le > 0:

                lai_suat_thang = lai_suat_nam / 12
                tien_lai = tien_hien_tai * lai_suat_thang * thang_le
                tien_hien_tai += tien_lai

                data.append({
                    "Kỳ": f"{thang_le} tháng lẻ",
                    "Tiền gốc đầu kỳ": tien_hien_tai - tien_lai,
                    "Tiền lãi kỳ này": tien_lai,
                    "Lãi lũy kế": tien_hien_tai - so_tien_gui,
                    "Tổng gốc + lãi": tien_hien_tai
                })

            tong_tien = tien_hien_tai
            tong_lai = tong_tien - so_tien_gui

            tien_lai_dinh_ky = (
                data[-1]["Tiền lãi kỳ này"]
            )

        else:

            tong_tien = (
                so_tien_gui
                * (1 + lai_suat_nam) ** (ky_han / 12)
            )

            tong_lai = tong_tien - so_tien_gui
            tien_lai_dinh_ky = tong_lai

            data.append({
                "Kỳ": "Cuối kỳ",
                "Tiền gốc đầu kỳ": so_tien_gui,
                "Tiền lãi kỳ này": tong_lai,
                "Lãi lũy kế": tong_lai,
                "Tổng gốc + lãi": tong_tien
            })

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================

    st.success("✅ Tính toán hoàn tất!")

    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            f"{tien_lai_dinh_ky:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            f"{tong_lai:,.0f} VNĐ"
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            f"{tong_tien:,.0f} VNĐ"
        )

    st.divider()

    # ==============================
    # THÔNG TIN KHOẢN GỬI
    # ==============================

    st.subheader("📋 Thông tin khoản gửi")

    thong_tin = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Phương pháp tính",
            "Hình thức nhận lãi"
        ],
        "Giá trị": [
            f"{so_tien_gui:,.0f} VNĐ",
            f"{ky_han} tháng",
            f"{lai_suat:.2f}%/năm",
            hinh_thuc_lai,
            hinh_thuc_nhan
        ]
    })

    st.table(thong_tin)

    # ==============================
    # BẢNG CHI TIẾT
    # ==============================

    st.subheader("📑 Chi tiết tiền lãi")

    df = pd.DataFrame(data)

    # Định dạng số tiền
    cot_tien = [
        col for col in df.columns
        if col != "Kỳ"
    ]

    for col in cot_tien:
        df[col] = df[col].apply(
            lambda x: f"{x:,.0f} VNĐ"
        )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ==============================
    # CÔNG THỨC
    # ==============================

    with st.expander("📚 Xem công thức tính"):

        if hinh_thuc_lai == "Lãi đơn":

            st.markdown("""
            **Công thức lãi đơn:**

            **Tiền lãi = Tiền gốc × Lãi suất năm × Số tháng / 12**

            **Tổng tiền = Tiền gốc + Tiền lãi**
            """)

        else:

            st.markdown("""
            **Công thức lãi kép:**

            **A = P × (1 + r)ⁿ**

            Trong đó:

            - **A**: Tổng số tiền nhận được
            - **P**: Số tiền gốc
            - **r**: Lãi suất mỗi kỳ
            - **n**: Số kỳ tính lãi
            """)

# ==============================
# FOOTER
# ==============================

st.divider()

st.caption(
    "💡 Công cụ mang tính chất tham khảo, "
    "kết quả thực tế có thể khác tùy theo quy định "
    "của từng ngân hàng."
)
