import trafilatura
import os

def scrape_and_append(url):
    print(f"--- 🕸️ Đang bắt đầu cào dữ liệu từ: {url} ---")
    
    # 1. Tải và trích xuất nội dung
    downloaded = trafilatura.fetch_url(url)
    content = trafilatura.extract(downloaded)
    
    # 2. Danh sách các từ khóa báo hiệu cào lỗi (Junk detection)
    junk_keywords = [
        "javascript is disabled", 
        "enable javascript", 
        "browser extension",
        "access denied",
        "403 forbidden",
        "robot check"
    ]

    if content:
        # Kiểm tra xem nội dung có quá ngắn hoặc chứa từ khóa rác không
        is_junk = any(kw in content.lower() for kw in junk_keywords)
        
        if is_junk or len(content) < 100:
            print("⚠️ Cảnh báo: Nội dung cào về có vẻ là lỗi JavaScript hoặc quá ngắn.")
            print("--- Nội dung nhận được ---")
            print(content[:200] + "...")
            
            confirm = input("\nBạn có chắc chắn muốn lưu nội dung này không? (y/n): ")
            if confirm.lower() != 'y':
                print("❌ Đã hủy lưu dữ liệu rác.")
                return

        # 3. Ghi thêm vào file knowledge.txt nếu vượt qua kiểm tra
        with open("knowledge.txt", "a", encoding="utf-8") as f:
            f.write(f"\n\n--- Source: {url} ---\n")
            f.write(content)
            f.write("\n--- End of Source ---\n")
        
        print("✅ Thành công! Tri thức mới đã được nạp.")
    else:
        print("❌ Thất bại: Không thể lấy nội dung từ link này.")

if __name__ == "__main__":
    link = input("Dán link web bạn muốn Guru học vào đây: ")
    scrape_and_append(link)