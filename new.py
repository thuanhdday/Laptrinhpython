import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

try:
    from tabulate import tabulate
    from colorama import init, Fore, Style
    # Khởi tạo colorama
    init()
    HAS_FORMATTING = True
except ImportError:
    HAS_FORMATTING = False
    print("Thông báo: Để có giao diện đẹp hơn, hãy cài đặt thêm thư viện:")
    print("pip install tabulate colorama")

def print_colored(text, color=None, is_bold=False):
    """In văn bản có màu nếu có thư viện colorama"""
    if HAS_FORMATTING:
        if is_bold:
            text = Style.BRIGHT + text
        if color:
            text = color + text + Style.RESET_ALL
    print(text)

def print_separator():
    """In đường phân cách"""
    print_colored("="*80, Fore.CYAN if HAS_FORMATTING else None)

try:
    # Đọc dữ liệu
    print_colored("Đang đọc dữ liệu...", Fore.GREEN if HAS_FORMATTING else None)
    df = pd.read_csv('data.csv', low_memory=False)
    
    # Kiểm tra và làm sạch dữ liệu
    if 'reviews.text' not in df.columns:
        raise ValueError("Không tìm thấy cột 'reviews.text' trong dữ liệu")
    
    # Loại bỏ các dòng không có đánh giá
    df.dropna(subset=['reviews.text'], inplace=True)
    
    if len(df) == 0:
        raise ValueError("Không có dữ liệu đánh giá sau khi làm sạch")

    # Hàm phân tích cảm xúc sử dụng TextBlob
    def analyze_sentiment(text):
        try:
            analysis = TextBlob(str(text))
            if analysis.sentiment.polarity > 0.1:
                return 'Tích cực'
            elif analysis.sentiment.polarity < -0.1:
                return 'Tiêu cực'
            else:
                return 'Trung lập'
        except:
            return 'Trung lập'

    print_colored("Đang phân tích cảm xúc...", Fore.GREEN if HAS_FORMATTING else None)
    # Áp dụng phân tích cảm xúc vào dữ liệu
    df['Cảm xúc'] = df['reviews.text'].apply(analyze_sentiment)

    # ------- Biểu đồ 1: Phân phối cảm xúc -------
    print_colored("\nBIỂU ĐỒ PHÂN PHỐI CẢM XÚC", Fore.GREEN if HAS_FORMATTING else None)
    try:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='Cảm xúc', order=['Tích cực', 'Trung lập', 'Tiêu cực'],
                    palette={'Tích cực': 'green', 'Trung lập': 'gray', 'Tiêu cực': 'red'})
        plt.title('Phân phối cảm xúc trong đánh giá sản phẩm', pad=20, fontsize=14, fontweight='bold')
        plt.xlabel('Loại cảm xúc', fontsize=12)
        plt.ylabel('Số lượng đánh giá', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        plt.close()
    except Exception as e:
        print_colored(f"Lỗi khi tạo biểu đồ phân phối cảm xúc: {str(e)}", Fore.RED if HAS_FORMATTING else None)

    # ------- Biểu đồ 2 & 3: Phân tích đánh giá sao -------
    if 'reviews.rating' in df.columns:
        print_colored("\nPHÂN TÍCH ĐÁNH GIÁ SAO", Fore.GREEN if HAS_FORMATTING else None)
        try:
            # Biểu đồ phân phối điểm đánh giá
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x='reviews.rating', palette='viridis')
            plt.title('Phân phối điểm đánh giá (1-5 sao)', pad=20, fontsize=14, fontweight='bold')
            plt.xlabel('Số sao', fontsize=12)
            plt.ylabel('Số lượng đánh giá', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
            plt.close()

            # Biểu đồ tương quan giữa điểm và cảm xúc
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=df, x='Cảm xúc', y='reviews.rating',
                      order=['Tích cực', 'Trung lập', 'Tiêu cực'],
                      palette={'Tích cực': 'green', 'Trung lập': 'gray', 'Tiêu cực': 'red'})
            plt.title('Tương quan giữa điểm đánh giá và cảm xúc', pad=20, fontsize=14, fontweight='bold')
            plt.xlabel('Loại cảm xúc', fontsize=12)
            plt.ylabel('Điểm đánh giá (sao)', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
            plt.close()
        except Exception as e:
            print_colored(f"Lỗi khi tạo biểu đồ đánh giá sao: {str(e)}", Fore.RED if HAS_FORMATTING else None)

    # ------- Biểu đồ 4: Top sản phẩm và phân tích cảm xúc -------
    print_colored("\nPHÂN TÍCH TOP SẢN PHẨM", Fore.GREEN if HAS_FORMATTING else None)
    try:
        # Đếm số lượng cảm xúc theo sản phẩm
        sentiment_counts = df.groupby(['name', 'Cảm xúc']).size().unstack(fill_value=0).reset_index()

        # Lấy top 10 sản phẩm có nhiều đánh giá nhất
        top_products = df['name'].value_counts().head(10).index
        sentiment_top = sentiment_counts[sentiment_counts['name'].isin(top_products)]

        # Đảm bảo các cột cảm xúc luôn tồn tại
        for col in ['Tích cực', 'Tiêu cực']:
            if col not in sentiment_top.columns:
                sentiment_top[col] = 0

        # Vẽ biểu đồ
        plt.figure(figsize=(15, 8))
        sentiment_top.plot(
            x='name',
            y=['Tích cực', 'Tiêu cực'],
            kind='bar',
            stacked=True,
            color=['green', 'red']
        )
        plt.title('Số lượng bình luận tích cực và tiêu cực theo sản phẩm (Top 10)', 
                 pad=20, fontsize=14, fontweight='bold')
        plt.xlabel('Tên sản phẩm', fontsize=12)
        plt.ylabel('Số lượng bình luận', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Loại cảm xúc', title_fontsize=12)
        plt.tight_layout()
        plt.show()
        plt.close()
    except Exception as e:
        print_colored(f"Lỗi khi tạo biểu đồ top sản phẩm: {str(e)}", Fore.RED if HAS_FORMATTING else None)

    # ------- WordCloud tổng quan -------
    print_colored("\nPHÂN TÍCH TỪ KHÓA TỔNG QUAN", Fore.GREEN if HAS_FORMATTING else None)
    try:
        # Tách văn bản theo cảm xúc
        positive_reviews = ' '.join(df[df['Cảm xúc'] == 'Tích cực']['reviews.text'].astype(str))
        negative_reviews = ' '.join(df[df['Cảm xúc'] == 'Tiêu cực']['reviews.text'].astype(str))

        # Cấu hình chung cho WordCloud
        wordcloud_config = {
            'width': 1000,
            'height': 500,
            'background_color': 'white',
            'colormap': 'RdYlBu',
            'collocations': False,
            'min_word_length': 3,
            'max_words': 100,
            'prefer_horizontal': 0.7
        }

        # Tạo WordCloud cho đánh giá tích cực
        if len(positive_reviews.strip()) > 0:
            wordcloud_pos = WordCloud(**wordcloud_config).generate(positive_reviews)
            plt.figure(figsize=(12, 6))
            plt.imshow(wordcloud_pos, interpolation='bilinear')
            plt.title('Từ khóa phổ biến trong đánh giá tích cực', 
                     pad=20, fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            plt.show()
            plt.close()

        # Tạo WordCloud cho đánh giá tiêu cực
        if len(negative_reviews.strip()) > 0:
            wordcloud_neg = WordCloud(**wordcloud_config).generate(negative_reviews)
            plt.figure(figsize=(12, 6))
            plt.imshow(wordcloud_neg, interpolation='bilinear')
            plt.title('Từ khóa phổ biến trong đánh giá tiêu cực', 
                     pad=20, fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            plt.show()
            plt.close()
    except Exception as e:
        print_colored(f"Lỗi khi tạo WordCloud tổng quan: {str(e)}", Fore.RED if HAS_FORMATTING else None)

    # ------- Phân tích chi tiết sản phẩm có đánh giá tiêu cực -------
    print_separator()
    print_colored("PHÂN TÍCH CHI TIẾT ĐÁNH GIÁ TIÊU CỰC", Fore.YELLOW if HAS_FORMATTING else None)
    print_separator()

    # Tính tỷ lệ đánh giá tiêu cực cho mỗi sản phẩm
    product_sentiment = df.groupby('name').agg({
        'Cảm xúc': lambda x: (x == 'Tiêu cực').mean(),
        'reviews.text': 'count'
    }).reset_index()

    # Đổi tên cột
    product_sentiment.columns = ['Tên sản phẩm', 'Tỷ lệ tiêu cực', 'Tổng số đánh giá']

    # Lọc sản phẩm có ít nhất 5 đánh giá và sắp xếp theo tỷ lệ tiêu cực
    min_reviews = 5
    negative_products = product_sentiment[product_sentiment['Tổng số đánh giá'] >= min_reviews].sort_values(
        'Tỷ lệ tiêu cực', ascending=False
    )

    if len(negative_products) == 0:
        raise ValueError(f"Không có sản phẩm nào có ít nhất {min_reviews} đánh giá")

    # Format tỷ lệ tiêu cực thành phần trăm
    negative_products['Tỷ lệ tiêu cực'] = negative_products['Tỷ lệ tiêu cực'].apply(lambda x: f"{x*100:.1f}%")

    # In ra top 10 sản phẩm có tỷ lệ đánh giá tiêu cực cao nhất
    print_colored("\nTOP 10 SẢN PHẨM CÓ TỶ LỆ ĐÁNH GIÁ TIÊU CỰC CAO NHẤT", Fore.GREEN if HAS_FORMATTING else None)
    print_colored(f"(Chỉ tính các sản phẩm có ít nhất {min_reviews} đánh giá)\n", Fore.YELLOW if HAS_FORMATTING else None)

    if HAS_FORMATTING:
        print(tabulate(
            negative_products.head(10), 
            headers=['Tên sản phẩm', 'Tỷ lệ tiêu cực', 'Tổng số đánh giá'],
            tablefmt='grid',
            showindex=True,
            numalign='right'
        ))
    else:
        print(negative_products.head(10).to_string())

    # Phân tích từ khóa tiêu cực cho mỗi sản phẩm trong top 5
    print_colored("\nPHÂN TÍCH TỪ KHÓA TIÊU CỰC CHO TOP 5 SẢN PHẨM", Fore.GREEN if HAS_FORMATTING else None)
    top_5_products = negative_products.head()['Tên sản phẩm'].tolist()

    # Tùy chỉnh style cho WordCloud
    wordcloud_config = {
        'width': 1000,
        'height': 500,
        'background_color': 'white',
        'colormap': 'RdYlBu',
        'collocations': False,
        'min_word_length': 3,
        'max_words': 100,
        'prefer_horizontal': 0.7
    }

    for idx, product in enumerate(top_5_products, 1):
        try:
            # Lấy tất cả đánh giá tiêu cực của sản phẩm
            negative_reviews = df[(df['name'] == product) & (df['Cảm xúc'] == 'Tiêu cực')]['reviews.text']
            
            if len(negative_reviews) > 0:
                print_separator()
                print_colored(f"#{idx}: {product}", Fore.YELLOW if HAS_FORMATTING else None)
                print_colored(f"Số lượng đánh giá tiêu cực: {len(negative_reviews)}")
                print_separator()
                
                # Tạo và hiển thị wordcloud cho từng sản phẩm
                text = ' '.join(negative_reviews.astype(str))
                try:
                    wordcloud = WordCloud(**wordcloud_config).generate(text)
                    
                    plt.figure(figsize=(12, 6))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.title(f'Từ khóa tiêu cực - {product}', pad=20, fontsize=14, fontweight='bold')
                    plt.axis('off')
                    plt.tight_layout()
                    plt.show()
                    plt.close()
                except Exception as e:
                    print_colored(f"Lỗi khi tạo wordcloud cho {product}: {str(e)}", Fore.RED if HAS_FORMATTING else None)
        except Exception as e:
            print_colored(f"Lỗi khi xử lý sản phẩm {product}: {str(e)}", Fore.RED if HAS_FORMATTING else None)

    print_separator()
    print_colored("🎉 HOÀN THÀNH PHÂN TÍCH!", Fore.GREEN if HAS_FORMATTING else None)
    print_separator()

except FileNotFoundError:
    print_colored("Lỗi: Không tìm thấy file data.csv", Fore.RED if HAS_FORMATTING else None)
    print("Vui lòng đảm bảo file data.csv nằm trong cùng thư mục với script.")

except Exception as e:
    print_colored(f"Lỗi không mong đợi: {str(e)}", Fore.RED if HAS_FORMATTING else None)
    print("Vui lòng kiểm tra lại dữ liệu đầu vào và thử lại.")
