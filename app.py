import streamlit as st
import pandas as pd
import math
from datetime import date

# Page Configuration
st.set_page_config(page_title="TECHPETAL PRIVATE LIMITED", page_icon="🏢", layout="wide")

# Custom CSS for Professional Corporate Look
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #4CAF50; margin-bottom: 0px; }
    .sub-title { font-size: 14px; color: #888; margin-bottom: 20px; }
    .card { background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# Data Persistence Setup
if 'employees' not in st.session_state:
    st.session_state['employees'] = []
if 'attendance_logs' not in st.session_state:
    st.session_state['attendance_logs'] = []
if 'maker_entries' not in st.session_state:
    st.session_state['maker_entries'] = []
if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

# Header
st.markdown('<div class="main-title">🏢 TECHPETAL PRIVATE LIMITED (TPPL)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enterprise Work Tracking & Geofenced Attendance System (Code: TPPL)</div>', unsafe_allow_html=True)

# Registered Offices
OFFICES = {
    "Hajipur Office": {"lat": 25.692200, "lon": 85.210600, "code": "321"},
    "Madhubani Data Center": {"lat": 26.334528, "lon": 86.073917, "code": "401"},
    "Madhubani Office": {"lat": 26.344750, "lon": 86.071417, "code": "402"}
}

def get_distance_meters(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lam = math.radians(lon2 - lon1)
    a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lam/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# Top Menu Navigation
mode = st.radio("Select Interface Mode:", ["📱 Operator Portal (Employees)", "🔒 Admin Master Panel (Management)"], horizontal=True)

# -------------------------------------------------------------
# 1. OPERATOR MOBILE PORTAL (FOR ALL EMPLOYEES)
# -------------------------------------------------------------
if mode == "📱 Operator Portal (Employees)":
    tab1, tab2, tab3 = st.tabs(["📝 Employee Registration", "📍 Mark Attendance (30m Geofence)", "📊 Daily Work Entry"])

    with tab1:
        st.subheader("Employee Onboarding Registration")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            mobile = st.text_input("Mobile Number")
            aadhar = st.text_input("Aadhar Card Number (12 Digits)")
        with c2:
            address = st.text_area("Address")
            assigned_off = st.selectbox("Assigned Workplace Location", list(OFFICES.keys()))
            password = st.text_input("Set Password (Optional)", type="password")

        if st.button("Submit Registration & Get Employee ID"):
            if name and mobile and len(aadhar) == 12:
                off_code = OFFICES[assigned_off]["code"]
                seq_num = len(st.session_state['employees']) + 1
                emp_id = f"TPPL/{off_code}/{seq_num:02d}"

                st.session_state['employees'].append({
                    "Employee ID": emp_id, "Name": name, "Mobile": mobile, 
                    "Aadhar": aadhar, "Address": address, "Office": assigned_off,
                    "Password": password if password else "TPPL@123"
                })
                st.success(f"✅ Registration Successful! Your Permanent Employee ID is: **{emp_id}**")
            else:
                st.error("Kripya Naam, Mobile, aur 12-digit Aadhar Number sahi se bharein.")

    with tab2:
        st.subheader("Daily Geofenced Attendance")
        st.caption("🔒 Date Lock Active: Current Date attendance only.")
        c1, c2 = st.columns(2)
        with c1:
            emp_id_in = st.text_input("Enter Employee ID (e.g. TPPL/321/01)")
            status_in = st.selectbox("Attendance Type", ["Present", "Absent"])
            loc_in = st.selectbox("Current Location", list(OFFICES.keys()))
        with c2:
            u_lat = st.number_input("GPS Latitude", value=25.692200, format="%.6f")
            u_lon = st.number_input("GPS Longitude", value=85.210600, format="%.6f")

        if st.button("Submit Attendance Log"):
            today_str = str(date.today())
            if status_in == "Absent":
                st.session_state['attendance_logs'].append({
                    "Date": today_str, "Employee ID": emp_id_in, "Status": "ABSENT", 
                    "Location": loc_in, "Distance": "N/A"
                })
                st.warning(f"Attendance logged as ABSENT for {today_str}")
            else:
                target = OFFICES[loc_in]
                dist = get_distance_meters(u_lat, u_lon, target["lat"], target["lon"])
                if dist <= 30.0:
                    st.session_state['attendance_logs'].append({
                        "Date": today_str, "Employee ID": emp_id_in, "Status": "PRESENT", 
                        "Location": loc_in, "Distance": f"{round(dist, 1)}m"
                    })
                    st.success(f"✅ PRESENT Verified! Distance from {loc_in}: {round(dist, 1)}m (Within 30m Zone)")
                else:
                    st.error(f"❌ DENIED! Distance is {round(dist, 1)}m. You must be within 30m of {loc_in}.")

    with tab3:
        st.subheader("Daily Work Submission (Maker Report Entry)")
        w_emp = st.text_input("Employee ID", key="w_emp")
        sro = st.text_input("SRO / Registration Office Name")
        c1, c2, c3 = st.columns(3)
        with c1:
            v_year = st.text_input("Volume Year")
        with c2:
            v_no = st.text_input("Volume No")
        with c3:
            deeds = st.number_input("Deeds / Metadata Created Today", min_value=1, step=1)

        if st.button("Submit Daily Work"):
            if w_emp and sro and v_year and v_no:
                st.session_state['maker_entries'].append({
                    "Date": str(date.today()), "Employee ID": w_emp, "SRO": sro,
                    "Volume Year": str(v_year).strip(), "Volume No": str(v_no).strip(),
                    "Created Deeds": deeds
                })
                st.success("✅ Work details submitted to Admin Dashboard successfully!")
            else:
                st.error("Kripya saare fields ache se fill karein.")

# -------------------------------------------------------------
# 2. ADMIN MASTER PANEL (MANAGEMENT - PASSWORD PROTECTED)
# -------------------------------------------------------------
else:
    st.subheader("🔒 Secure Admin Login")
    
    if not st.session_state['admin_logged_in']:
        c1, c2 = st.columns(2)
        with c1:
            admin_user = st.text_input("Admin Username")
            admin_pass = st.text_input("Admin Password", type="password")
            if st.button("Login to Admin Panel"):
                if admin_user == "admin" and admin_pass == "tppl@2026":
                    st.session_state['admin_logged_in'] = True
                    st.rerun()
                else:
                    st.error("Invalid Admin Username or Password!")
    else:
        st.success("✅ Admin Authenticated - FULL ACCESS GRANTED")
        if st.button("Logout Admin"):
            st.session_state['admin_logged_in'] = False
            st.rerun()

        adm1, adm2, adm3 = st.tabs(["📊 Missing Volume Reconciliation", "👥 Registered Employees List", "📍 Attendance Audit Logs"])

        with adm1:
            st.subheader("Volume Reconciliation & Missing Report Engine")
            c1, c2, c3 = st.columns(3)
            with c1:
                y_file = st.file_uploader("1. Yesterday Volume Report", type=["xlsx"])
            with c2:
                t_file = st.file_uploader("2. Today Volume Report", type=["xlsx"])
            with c3:
                m_file = st.file_uploader("3. Today One-Day Maker Report", type=["xlsx"])

            if y_file and t_file and m_file:
                yest_df = pd.read_excel(y_file, header=1)
                today_df = pd.read_excel(t_file, header=1)
                maker_df = pd.read_excel(m_file, header=1)

                for df in [yest_df, today_df, maker_df]:
                    df.columns = df.columns.str.strip()

                def std_col(df):
                    for col in df.columns:
                        if 'office' in col.lower() or 'sro' in col.lower():
                            df.rename(columns={col: 'Registration Office'}, inplace=True)
                        if 'volume' in col.lower() and ('no' in col.lower() or 'num' in col.lower()):
                            df.rename(columns={col: 'Volume No.'}, inplace=True)
                    return df

                yest_df, today_df, maker_df = std_col(yest_df), std_col(today_df), std_col(maker_df)

                for df in [yest_df, today_df, maker_df]:
                    if 'Volume Year' in df.columns:
                        df['Volume Year'] = df['Volume Year'].astype(str).str.strip().str.replace('.0', '', regex=False)
                    if 'Volume No.' in df.columns:
                        df['Volume No.'] = df['Volume No.'].astype(str).str.strip().str.replace('.0', '', regex=False)
                    if 'Registration Office' in df.columns:
                        df['Registration Office'] = df['Registration Office'].astype(str).str.strip()

                yest_df['KEY'] = yest_df['Registration Office'] + "_" + yest_df['Volume Year'] + "_" + yest_df['Volume No.']
                today_df['KEY'] = today_df['Registration Office'] + "_" + today_df['Volume Year'] + "_" + today_df['Volume No.']
                maker_df['KEY'] = maker_df['Volume Year'] + "_" + maker_df['Volume No.']

                today_keys = set(today_df['KEY'])
                missing_df = yest_df[~yest_df['KEY'].isin(today_keys)].copy()

                def check_rec(row):
                    mk_key = row['Volume Year'] + "_" + row['Volume No.']
                    m_match = maker_df[maker_df['KEY'] == mk_key]
                    if not m_match.empty:
                        ops = ", ".join(m_match['Name'].dropna().astype(str).unique()) if 'Name' in m_match.columns else "Operator"
                        return f"Submitted Today by {ops} (Volume Complete)"
                    return "Missing / Unaccounted"

                missing_df['Status'] = missing_df.apply(check_rec, axis=1)
                st.write("### 🔴 Missing Volume Comparison Result")
                st.dataframe(missing_df[['Registration Office', 'Volume Year', 'Volume No.', 'Deed Count', 'Status']], use_container_width=True)

        with adm2:
            st.subheader("Employee Master Database")
            if st.session_state['employees']:
                st.dataframe(pd.DataFrame(st.session_state['employees']), use_container_width=True)
            else:
                st.info("No registered employees found in system memory.")

        with adm3:
            st.subheader("Live Attendance Logs")
            if st.session_state['attendance_logs']:
                st.dataframe(pd.DataFrame(st.session_state['attendance_logs']), use_container_width=True)
            else:
                st.info("No attendance logs recorded today.")