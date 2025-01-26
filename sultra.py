from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Path ke ChromeDriver Anda
chrome_driver_path = r"C:\\Users\\andriawan\\Documents\\My Task\\Python\\MY PROJECT\\infokendari\\chromedriver.exe"
service = Service(chrome_driver_path)

# Inisialisasi driver
driver = webdriver.Chrome(service=service)

# Buka URL target
url = "https://sultra.tribunnews.com/bisnis"
driver.get(url)

# Fungsi untuk menyimpan data ke Excel
def save_to_excel(data, filename="scraped_data_bisnis.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data berhasil disimpan ke file {filename}")

# Simulasi scroll untuk memuat data
last_height = driver.execute_script("return document.body.scrollHeight")

data = []  # Variabel untuk menyimpan data
while True:
    try:
        # Scroll ke bawah halaman
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)  # Waktu tunggu untuk memuat konten baru

        # Ambil elemen berdasarkan class target
        posts = driver.find_elements(By.CSS_SELECTOR, "h3")
        links = driver.find_elements(By.CSS_SELECTOR, "h3 a")
        dates = driver.find_elements(By.CSS_SELECTOR, "time.timeago")

        # Pastikan setiap elemen diambil dengan handle jika elemen tidak ada
        for i in range(len(posts)):
            title = posts[i].text if i < len(posts) else None
            link = links[i].get_attribute('href') if i < len(links) else None
            date = dates[i].text if i < len(dates) else None
            data.append({"title": title, "link": link, "date": date})

        # Simpan data sementara ke Excel
        save_to_excel(data)

        # Cek apakah sudah mencapai akhir halaman
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    except Exception as e:
        print(f"Error: {e}")
        save_to_excel(data)  # Simpan data terakhir sebelum keluar
        break

# Simpan data akhir ke Excel
save_to_excel(data)

# Tutup driver
driver.quit()
