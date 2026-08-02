import streamlit as st
from PIL import Image
import pandas as pd
import cv2
import numpy as np
import os


# =========================
# IMPORT MODULES
# =========================

from Modules.predict_review import predict_review
from Modules.Product_Verifier import verify_product

from Modules.Admin import (
    add_product,
    get_all_products,
    register_admin,
    login_admin,
    get_audit_logs
)

from Modules.Customer import (
    register_customer,
    login_customer
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Product Trust System",
    page_icon="🛡",
    layout="wide"
)


# =========================
# SESSION STATE
# =========================

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

if "customer_login" not in st.session_state:
    st.session_state.customer_login = False


# =========================
# CSS
# =========================

st.markdown(
"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Outfit', sans-serif;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111b27 0%, #0d131a 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    width: 280px !important;
}

section[data-testid="stSidebar"] > div {
    width: 280px !important;
}

section[data-testid="stSidebar"] .stRadio > label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* Glassmorphism custom cards */
.card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 30px;
    height: 240px;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    color: #f8fafc;
}
.card:hover {
    transform: translateY(-8px);
    border-color: rgba(30, 136, 229, 0.4);
    box-shadow: 0 16px 40px 0 rgba(30, 136, 229, 0.2);
}
.card h2 {
    color: #1E88E5 !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    margin-bottom: 12px !important;
}
.card p {
    color: #94a3b8 !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}

/* Animated gradient main title */
.main-title {
    font-size: 46px;
    font-weight: 800;
    background: linear-gradient(45deg, #1e88e5, #00d2ff, #7928ca);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient_text 4s ease infinite;
    text-align: center;
    margin-bottom: 5px;
}
@keyframes gradient_text {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.subtitle {
    text-align: center;
    font-size: 18px;
    font-weight: 400;
    color: #64748b;
    margin-bottom: 25px;
}

/* Styled Alert Blocks for Results */
.result-banner {
    padding: 20px;
    border-radius: 16px;
    margin: 15px 0;
    text-align: center;
    font-weight: 600;
    font-size: 18px;
    backdrop-filter: blur(8px);
}
.result-genuine {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.1);
}
.result-fake {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #f87171;
    box-shadow: 0 0 15px rgba(239, 68, 68, 0.1);
}
.result-warning {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #fbbf24;
    box-shadow: 0 0 15px rgba(245, 158, 11, 0.1);
}

/* Explainability Reasons */
.reason-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 4px solid #1E88E5;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #cbd5e1;
    font-size: 14px;
}

/* KPI metric cards */
.kpi-container {
    display: flex;
    gap: 15px;
    margin-bottom: 25px;
}
.kpi-card {
    flex: 1;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.kpi-val {
    font-size: 28px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 5px;
}
.kpi-label {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""",
unsafe_allow_html=True
)


# =========================
# HEADER
# =========================

st.markdown(
"""
<div class="main-title">
Product Trust Verification System
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle">
AI Based Review Detection & Product Verification
</div>
""",
unsafe_allow_html=True
)

st.write("---")


# =========================
# SIDEBAR
# =========================

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔐 Admin Portal",
        "👤 Customer Portal",
        "ℹ️ About Project"
    ]
)


# =========================
# HOME
# =========================

if menu == "🏠 Home":

    st.markdown(
        """
        ## Welcome to Product Trust System

        This system solves:

        - Fake product reviews
        - Counterfeit products

        using Machine Learning and QR Authentication.
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="card">
            <h2>⭐ Review Detection</h2>
            <p>Detect fake and genuine reviews using ML.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="card">
            <h2>📦 Product Verification</h2>
            <p>Verify authenticity using QR scanning.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="card">
            <h2>📊 Trust Score</h2>
            <p>Combines review and product reliability.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================
# ADMIN
# =========================

elif menu == "🔐 Admin Portal":

    st.header("🔐 Admin Portal")


    if not st.session_state.admin_login:


        option = st.radio(
            "Choose Option",
            [
                "Register Admin",
                "Login Admin"
            ]
        )


        if option == "Register Admin":

            username = st.text_input("Username")

            email = st.text_input("Email")

            password = st.text_input(
                "Password",
                type="password"
            )

            key = st.text_input(
                "Admin Access Key",
                type="password"
            )


            if st.button("Register"):

                result = register_admin(
                    username,
                    email,
                    password,
                    key
                )

                if result == "Success":
                    st.success(
                        "Admin Registered Successfully"
                    )

                elif result == "Unauthorized":
                    st.error(
                        "Invalid Admin Access Key"
                    )

                else:
                    st.warning(
                        "Admin already exists"
                    )



        elif option == "Login Admin":

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button("Login"):

                if login_admin(
                    username,
                    password
                ):

                    st.session_state.admin_login = True
                    st.session_state.admin_username = username

                    st.rerun()

                else:

                    st.error(
                        "Invalid Credentials"
                    )



    else:

        st.success(
            f"Admin Dashboard (Welcome, {st.session_state.get('admin_username', 'Admin')})"
        )


        if st.button("Logout"):

            st.session_state.admin_login = False
            st.session_state.admin_username = None

            st.rerun()


        admin_menu = st.radio(
            "Admin Menu",
            [
                "➕ Add Product",
                "📋 View Products",
                "📜 Scan Audit Logs"
            ]
        )


        if admin_menu == "➕ Add Product":


            name = st.text_input(
                "Product Name"
            )

            manufacturer = st.text_input(
                "Manufacturer"
            )

            batch = st.text_input(
                "Batch Number"
            )

            mfg = st.date_input(
                "Manufacture Date"
            )

            exp = st.date_input(
                "Expiry Date"
            )


            if st.button("Add Product"):

                uid = add_product(
                    name,
                    manufacturer,
                    batch,
                    str(mfg),
                    str(exp)
                )

                st.success(
                    "Product Added"
                )

                st.info(
                    f"Product ID : {uid}"
                )


                qr_path = f"qr_codes/{uid}.png"


                st.image(
                    qr_path,
                    width=250
                )


                with open(qr_path, "rb") as file:

                    st.download_button(
                        "Download QR",
                        file,
                        file_name=f"{uid}.png"
                    )



        elif admin_menu == "📋 View Products":


            products = get_all_products()

            # Calculate KPI Metrics
            total_products = len(products)
            total_scans = sum(p[7] for p in products)
            duplicate_warnings = sum(1 for p in products if p[7] > 1)

            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-label">📦 Total Products</div>
                    <div class="kpi-val">{total_products}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">📷 Total Scans</div>
                    <div class="kpi-val">{total_scans}</div>
                </div>
                <div class="kpi-card" style="border-color: rgba(239, 68, 68, 0.2)">
                    <div class="kpi-label" style="color: #f87171">⚠️ Duplicate Alerts</div>
                    <div class="kpi-val" style="color: #ef4444">{duplicate_warnings}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if total_products > 0:
                st.subheader("📊 Scan Count Distribution")
                df_chart = pd.DataFrame({
                    "Product": [p[1] for p in products],
                    "Scans": [p[7] for p in products]
                })
                st.bar_chart(data=df_chart, x="Product", y="Scans", use_container_width=True)

            st.subheader("📋 Registered Product List")
            df = pd.DataFrame(
                products,
                columns=[
                    "ID",
                    "Product",
                    "Manufacturer",
                    "Batch",
                    "MFG",
                    "EXP",
                    "Verification",
                    "Scan Count",
                    "Status"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            st.markdown("---")
            st.subheader("📥 Retrieve & Download Product QR Code")

            product_options = [f"{p[1]} (ID: {p[0]})" for p in products]
            selected_option = st.selectbox(
                "Select a product to view and download its QR code",
                product_options,
                key="download_qr_select"
            )

            if selected_option:
                selected_id = selected_option.split(" (ID: ")[-1].replace(")", "").strip()
                qr_path = f"qr_codes/{selected_id}.png"

                # Regenerate if file was deleted
                if not os.path.exists(qr_path):
                    import qrcode
                    os.makedirs("qr_codes", exist_ok=True)
                    qr = qrcode.make(selected_id)
                    qr.save(qr_path)

                # Display QR code image
                st.image(
                    qr_path,
                    caption=f"QR Code for: {selected_option}",
                    width=200
                )

                # Provide download button
                with open(qr_path, "rb") as file:
                    st.download_button(
                        label="Download QR Image",
                        data=file,
                        file_name=f"QR_{selected_id}.png",
                        mime="image/png",
                        key=f"dl_btn_{selected_id}"
                    )



        elif admin_menu == "📜 Scan Audit Logs":

            st.subheader("📜 Product Verification Audit Logs")

            logs = get_audit_logs()

            if len(logs) == 0:
                st.info("No scan attempts recorded yet.")
            else:
                # Calculate logs stats
                auth_count = sum(1 for log in logs if log[5] == "Authentic")
                dup_count = sum(1 for log in logs if log[5] == "Duplicate")
                fake_count = sum(1 for log in logs if log[5] == "Counterfeit")

                st.markdown(f"""
                <div class="kpi-container">
                    <div class="kpi-card" style="border-color: rgba(16, 185, 129, 0.2)">
                        <div class="kpi-label" style="color: #34d399">✅ Authentic Scans</div>
                        <div class="kpi-val" style="color: #10b981">{auth_count}</div>
                    </div>
                    <div class="kpi-card" style="border-color: rgba(245, 158, 11, 0.2)">
                        <div class="kpi-label" style="color: #fbbf24">⚠️ Duplicate Scans</div>
                        <div class="kpi-val" style="color: #f59e0b">{dup_count}</div>
                    </div>
                    <div class="kpi-card" style="border-color: rgba(239, 68, 68, 0.2)">
                        <div class="kpi-label" style="color: #f87171">❌ Counterfeit Scans</div>
                        <div class="kpi-val" style="color: #ef4444">{fake_count}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Render audit log DataFrame
                df_logs = pd.DataFrame(
                    logs,
                    columns=["Log ID", "Timestamp", "User", "Product ID", "Product Name", "Status"]
                )
                df_logs = df_logs[["Timestamp", "User", "Product ID", "Product Name", "Status"]]
                st.dataframe(df_logs, use_container_width=True)



# =========================
# CUSTOMER
# =========================

elif menu == "👤 Customer Portal":


    st.header(
        "👤 Customer Portal"
    )


    if not st.session_state.customer_login:


        action = st.radio(
            "Choose",
            [
                "Register",
                "Login"
            ]
        )


        if action == "Register":


            username = st.text_input(
                "Username"
            )

            email = st.text_input(
                "Email"
            )

            password = st.text_input(
                "Password",
                type="password"
            )


            if st.button(
                "Register"
            ):

                if register_customer(
                    username,
                    email,
                    password
                ):

                    st.success(
                        "Customer Registered"
                    )

                else:

                    st.error(
                        "User already exists"
                    )



        else:


            username = st.text_input(
                "Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )


            if st.button(
                "Login"
            ):


                if login_customer(
                    username,
                    password
                ):

                    st.session_state.customer_login = True
                    st.session_state.customer_username = username

                    st.rerun()

                else:

                    st.error(
                        "Invalid Login"
                    )



    else:


        st.success(
            f"Customer Dashboard (Welcome, {st.session_state.get('customer_username', 'Customer')})"
        )


        if st.button(
            "Logout"
        ):

            st.session_state.customer_login = False
            st.session_state.customer_username = None

            st.rerun()


        service = st.radio(
            "Choose Service",
            [
                "⭐ Review Detection",
                "📷 Product Verification"
            ]
        )


        # REVIEW

        if service == "⭐ Review Detection":

            review = st.text_area(
                "Enter Product Review",
                placeholder="Type or paste your product review here..."
            )

            if st.button(
                "Analyze Review"
            ):

                if review:

                    result, confidence, explanation = predict_review(
                        review
                    )

                    if result == "Genuine Review":
                        st.markdown(f"""
                        <div class="result-banner result-genuine">
                            ✅ Genuine Review Verified ({confidence:.2f}% Confidence)
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-banner result-fake">
                            ⚠️ Flagged as Fake / Machine-Generated Review ({confidence:.2f}% Confidence)
                        </div>
                        """, unsafe_allow_html=True)

                    st.progress(float(confidence) / 100.0)

                    st.subheader(
                        "🔍 Explainable AI Reasoning"
                    )

                    for reason in explanation:
                        st.markdown(f"""
                        <div class="reason-card">
                            🔹 {reason}
                        </div>
                        """, unsafe_allow_html=True)


        # PRODUCT VERIFY

        elif service == "📷 Product Verification":

            camera = st.camera_input(
                "Scan Product QR"
            )

            if camera:

                image = Image.open(camera)
                image = np.array(image)

                detector = cv2.QRCodeDetector()

                data, bbox, _ = detector.detectAndDecode(
                    image
                )

                if data:

                    status, details = verify_product(
                        data,
                        username=st.session_state.get("customer_username", "Anonymous")
                    )

                    if status == "Authentic":
                        st.markdown("""
                        <div class="result-banner result-genuine">
                            ✅ Authentic Product Verified
                        </div>
                        """, unsafe_allow_html=True)

                    elif status == "Duplicate":
                        st.markdown("""
                        <div class="result-banner result-warning">
                            ⚠️ Warning: Duplicate Scan Detected (Potential Counterfeit Copy!)
                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        st.markdown("""
                        <div class="result-banner result-fake">
                            ❌ Counterfeit Product (QR Code Not Registered)
                        </div>
                        """, unsafe_allow_html=True)

                    if details:
                        st.subheader(
                            "📦 Product Details"
                        )
                        for key, val in details.items():
                            st.write(f"**{key}:** {val}")

                else:

                    st.error(
                        "QR Code not detected in camera frame. Please try aligning it closer to the center."
                    )



# =========================
# ABOUT
# =========================

elif menu == "ℹ️ About Project":

    st.write(
        """
        ## Product Trust Verification System

        - ML Fake Review Detection
        - Explainable AI Result
        - Product QR Authentication
        - Admin & Customer Access Control
        """
    )


    ## source myenv/bin/activate  

    ## streamlit run app.py  