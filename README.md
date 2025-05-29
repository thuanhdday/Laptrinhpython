Dưới đây là nội dung **README.md** gợi ý dành cho project Python của bạn, phân tích cảm xúc từ đánh giá sản phẩm:

---

# 📊 Phân Tích Cảm Xúc Từ Đánh Giá Sản Phẩm (Sentiment Analysis)

## 🧠 Giới thiệu

Dự án này thực hiện phân tích cảm xúc (sentiment analysis) từ tập dữ liệu đánh giá sản phẩm (CSV), sử dụng thư viện **TextBlob** để xác định loại cảm xúc (Tích cực, Trung lập, Tiêu cực), và trực quan hóa dữ liệu bằng **matplotlib**, **seaborn**, **wordcloud**.

Ngoài ra, dự án còn giúp phát hiện các sản phẩm có tỷ lệ đánh giá tiêu cực cao và tạo **WordCloud** cho từng sản phẩm đó.

---

## 📁 Cấu trúc dự án

```
📦 sentiment-analysis/
├── 📄 main.py             # Script chính xử lý và trực quan hóa dữ liệu
├── 📄 data.csv            # File dữ liệu đánh giá đầu vào
└── 📄 README.md           # Tài liệu mô tả project
```

---

## 🧩 Các bước phân tích

1. **Đọc dữ liệu từ file `data.csv`**
2. **Tiền xử lý và loại bỏ dòng trống**
3. **Phân tích cảm xúc bằng TextBlob**
4. **Trực quan hóa dữ liệu:**

   * Biểu đồ phân phối cảm xúc
   * Biểu đồ phân phối điểm đánh giá (1–5 sao)
   * Boxplot thể hiện mối quan hệ giữa cảm xúc và điểm đánh giá
   * Biểu đồ top 10 sản phẩm có nhiều đánh giá nhất theo cảm xúc
   * WordCloud tổng quan cảm xúc tích cực và tiêu cực
5. **Phân tích sản phẩm có tỷ lệ đánh giá tiêu cực cao**

   * Bảng top 10 sản phẩm có tỷ lệ tiêu cực cao nhất
   * WordCloud tiêu cực riêng cho top 5 sản phẩm

---

## 📦 Cài đặt thư viện cần thiết

Chạy lệnh sau để cài đặt các thư viện cần thiết:

```bash
pip install pandas matplotlib seaborn textblob wordcloud tabulate colorama
```

Khởi tạo TextBlob (lần đầu tiên chạy):

```bash
python -m textblob.download_corpora
```

---

## 🚀 Cách chạy

1. Đảm bảo bạn có **file `data.csv`** chứa dữ liệu đánh giá. Cột bắt buộc: `reviews.text`, `name`, `reviews.rating`.
2. Chạy script:

```bash
python main.py
```

---

## 🖼️ Một số kết quả trực quan

* ✅ Biểu đồ phân phối cảm xúc
* ⭐ Phân phối điểm đánh giá 1–5 sao
* 📦 Top sản phẩm theo cảm xúc
* ☁️ WordCloud cho từ khóa trong đánh giá
* 📉 Phát hiện sản phẩm có tỷ lệ đánh giá tiêu cực cao

---

## 📌 Ghi chú

* Các đánh giá không có nội dung sẽ bị loại bỏ.
* Sản phẩm cần ít nhất **5 đánh giá** để được xét trong bảng tỷ lệ tiêu cực.
* Kết quả WordCloud có thể không hiển thị nếu văn bản không đủ dữ liệu.

---

