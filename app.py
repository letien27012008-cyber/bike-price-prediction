import streamlit as st
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Dự đoán giá xe đạp", page_icon="🚲", layout="wide")
st.title("🚲 Ứng dụng dự đoán giá xe đạp")
st.caption("Mô hình Random Forest được huấn luyện từ bộ dữ liệu bikes.xlsx do người dùng cung cấp.")

@st.cache_data
def load_data():
    data = pd.read_excel("bikes.xlsx")
    required = ["bike.id", "model", "category1", "category2", "frame", "price"]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError(f"Thiếu cột bắt buộc: {', '.join(missing)}")
    data = data[required].dropna().copy()
    for c in ["model", "category1", "category2", "frame"]:
        data[c] = data[c].astype(str)
    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data = data.dropna(subset=["price"])
    return data

@st.cache_resource
def train_model(data):
    features = ["model", "category1", "category2", "frame"]
    X, y = data[features], data["price"]
    prep = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), features)
    ])
    model = Pipeline([
        ("preprocess", prep),
        ("regressor", RandomForestRegressor(
            n_estimators=300, random_state=42, min_samples_leaf=1
        ))
    ])
    model.fit(X, y)

    # Holdout evaluation: report as a diagnostic, not a guarantee.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    eval_model = Pipeline([
        ("preprocess", ColumnTransformer([
            ("categorical", OneHotEncoder(handle_unknown="ignore"), features)
        ])),
        ("regressor", RandomForestRegressor(
            n_estimators=300, random_state=42, min_samples_leaf=1
        ))
    ])
    eval_model.fit(X_train, y_train)
    pred = eval_model.predict(X_test)
    metrics = {
        "r2": r2_score(y_test, pred),
        "mae": mean_absolute_error(y_test, pred),
        "rmse": mean_squared_error(y_test, pred) ** 0.5
    }
    return model, metrics

try:
    data = load_data()
    model, metrics = train_model(data)
except Exception as exc:
    st.error(f"Không thể tải dữ liệu hoặc huấn luyện mô hình: {exc}")
    st.info("Hãy đặt file bikes.xlsx cùng thư mục với app.py.")
    st.stop()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Số mẫu dữ liệu", f"{len(data)}")
m2.metric("Giá thấp nhất", f"{data.price.min():,.0f}")
m3.metric("Giá cao nhất", f"{data.price.max():,.0f}")
m4.metric("Giá trung bình", f"{data.price.mean():,.2f}")

st.subheader("Nhập thông tin xe")
left, right = st.columns(2)
with left:
    model_choice = st.selectbox("Mẫu xe (model)", sorted(data["model"].unique()))
    category1 = st.selectbox("Loại xe (category1)", sorted(data["category1"].unique()))
with right:
    category2 = st.selectbox("Phân nhóm (category2)", sorted(data["category2"].unique()))
    frame = st.selectbox("Vật liệu khung (frame)", sorted(data["frame"].unique()))

if st.button("Dự đoán giá xe", type="primary", use_container_width=True):
    sample = pd.DataFrame([{
        "model": model_choice,
        "category1": category1,
        "category2": category2,
        "frame": frame
    }])
    estimate = float(model.predict(sample)[0])
    st.success(f"Giá xe dự đoán: **{estimate:,.2f}** (theo đơn vị giá trong dữ liệu)")
    st.caption("Đây là ước lượng từ mô hình, không phải giá bán được xác nhận.")

with st.expander("Xem dữ liệu và đánh giá mô hình"):
    st.write("**Dữ liệu gốc**")
    st.dataframe(data, use_container_width=True)
    st.write("**Đánh giá trên tập kiểm tra 20% (random_state=42)**")
    c1, c2, c3 = st.columns(3)
    c1.metric("R²", f"{metrics['r2']:.3f}")
    c2.metric("MAE", f"{metrics['mae']:,.2f}")
    c3.metric("RMSE", f"{metrics['rmse']:,.2f}")
    st.warning(
        "Bộ dữ liệu chỉ có 97 mẫu và mỗi tên model là duy nhất. "
        "Kết quả kiểm tra có thể biến động; dự đoán cho mẫu xe chưa xuất hiện "
        "trong dữ liệu có độ tin cậy hạn chế."
    )

st.caption("Các trường đầu vào sử dụng đúng các cột model, category1, category2 và frame trong bikes.xlsx.")
