import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="مناقصات Al-Nabhan", layout="wide")
st.image("logo al nabhan.jpg", width=180)
st.title("📋 منصة المناقصات اليومية - Al-Nabhan")

# تحميل البيانات
def load_data():
    try:
        file_path = f"Tenders_Report_2025-05-25.xlsx"
        df = pd.read_excel(file_path)
        return df
    except:
        return pd.DataFrame()

data = load_data()

if data.empty:
    st.warning("لا توجد مناقصات متاحة حالياً.")
else:
    with st.sidebar:
        st.header("🔍 تصفية")
        countries = st.multiselect("الدولة:", options=sorted(data["الدولة"].unique()))
        sectors = st.multiselect("المجال:", options=sorted(data["المجال"].unique()))

    filtered = data.copy()
    if countries:
        filtered = filtered[filtered["الدولة"].isin(countries)]
    if sectors:
        filtered = filtered[filtered["المجال"].isin(sectors)]

    st.markdown(f"### عدد المناقصات المعروضة: {len(filtered)}")
    st.dataframe(filtered, use_container_width=True)

    st.download_button(
        label="📥 تحميل التقرير",
        data=filtered.to_excel(index=False, engine='openpyxl'),
        file_name=f"Filtered_Tenders_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
