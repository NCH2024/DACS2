import mysql.connector
from PIL import Image
from io import BytesIO
import os

# ==================== CONFIG ====================
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'dacs2'

}
# ================================================

def insert_image(thongbao_id, image_path):
    with open(image_path, "rb") as file:
        binary_data = file.read()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = "UPDATE thongbao SET HinhAnh = %s WHERE thongbao_id = %s"
    cursor.execute(sql, (binary_data, thongbao_id))
    conn.commit()
    print("✅ Đã thêm ảnh vào thông báo", thongbao_id)

    cursor.close()
    conn.close()

def show_image(thongbao_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = "SELECT HinhAnh FROM thongbao WHERE thongbao_id = %s"
    cursor.execute(sql, (thongbao_id,))
    result = cursor.fetchone()

    if result and result[0]:
        image_data = result[0]
        image = Image.open(BytesIO(image_data))
        image.show()  # Hoặc lưu ra file nếu muốn
    else:
        print("❌ Không tìm thấy ảnh!")

    cursor.close()
    conn.close()

# ==================== TEST ======================
if __name__ == "__main__":
    thongbao_id = 4  # ID của thông báo em muốn cập nhật

    # 💾 Chèn ảnh
    insert_image(thongbao_id, "C:/Users/babic/Downloads/Thongbao4.jpg")

    # 🖼 Hiển thị ảnh
    show_image(thongbao_id)
