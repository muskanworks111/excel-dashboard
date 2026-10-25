import pandas as pd
import plotly.express as px
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Excel Data Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Interactive Excel Data Dashboard")
st.markdown("Upload your Excel file below to generate instant charts!")

# File Uploader
uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])

@st.cache_data
def load_data(file):
  return pd.read_excel(file)


if uploaded_file is not None:
  # Read Data
  df = load_data(uploaded_file)

  # Detect numeric and text columns automatically
  numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
  categorical_cols = df.select_dtypes(
      include=["object", "category"]
  ).columns.tolist()

  # 1. Key Metrics Section
  st.subheader("📌 Key Metrics")
  m1, m2, m3 = st.columns(3)
  m1.metric("Total Records", len(df))
  m2.metric("Total Columns", len(df.columns))
  if numeric_cols:
    m3.metric(
        f"Total {numeric_cols[0]}", f"{df[numeric_cols[0]].sum():,.2f}"
    )

  st.divider()

  # 2. Interactive Charts Section
  st.subheader("📈 Visualizations")
  if categorical_cols and numeric_cols:
    col1, col2 = st.columns(2)

    with col1:
      cat_col = st.selectbox("Select X-Axis Category", categorical_cols)
      num_col = st.selectbox("Select Y-Axis Value", numeric_cols)
      fig_bar = px.bar(
          df,
          x=cat_col,
          y=num_col,
          title=f"{num_col} by {cat_col}",
          template="plotly_white",
      )
      st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
      fig_pie = px.pie(
          df,
          names=cat_col,
          values=num_col,
          title=f"Distribution of {num_col}",
          template="plotly_white",
      )
      st.plotly_chart(fig_pie, use_container_width=True)
  else:
    st.info("Uploaded dataset needs both text and numeric columns for charts.")

  st.divider()

  # 3. Data Table Preview
  st.subheader("📋 Raw Data Preview")
  st.dataframe(df, use_container_width=True)

else:
  st.info("👆 Please upload an `.xlsx` file using the button above to begin.")