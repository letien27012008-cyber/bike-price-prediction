# Ứng dụng dự đoán giá xe đạp

## Chạy trên máy tính
1. Cài Python 3.10 trở lên.
2. Đặt `app.py`, `requirements.txt` và `bikes.xlsx` trong cùng một thư mục.
3. Mở Terminal/CMD tại thư mục đó và chạy:

```bash
pip install -r requirements.txt
streamlit run app.py
```

4. Trình duyệt sẽ mở ứng dụng Streamlit.

## Triển khai Streamlit Community Cloud
Đưa cả 3 file (`app.py`, `requirements.txt`, `bikes.xlsx`) lên cùng một GitHub repository, sau đó tạo ứng dụng mới trên Streamlit Community Cloud và chọn `app.py` làm Main file path.

## Lưu ý
Dữ liệu gồm 97 mẫu, các trường đầu vào là `model`, `category1`, `category2`, `frame`; biến mục tiêu là `price`. Giá dự đoán giữ nguyên đơn vị như cột `price` trong dữ liệu. Bộ dữ liệu nhỏ nên kết quả chỉ mang tính tham khảo.
