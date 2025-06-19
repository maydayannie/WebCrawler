import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def send_line_push(user_id: str, message: str, token: str):
    print("LINE TOKEN:", os.getenv("LINE_CHANNEL_TOKEN"))

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    res = requests.post(url, headers=headers, json=payload)
    print(res.status_code, res.text)

def main():
    # Selenium headless config
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    service = Service(ChromeDriverManager().install())  # ✅ 建立 Service 物件
    driver = webdriver.Chrome(service=service, options=options)  # ✅ 使用正確方式建立 driver

    try:
        # driver.get("https://www.costco.com.tw/search?searchOption=tw-search-all&text=macbook%20air")
        driver.get("https://www.costco.com.tw/search?text=televisions&searchOption=tw-search-all")
        # WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "is-initialized"))
        # )
        WebDriverWait(driver, 30).until(
            # EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'MacBook Air')]"))
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'TV')]"))
        )
        driver.implicitly_wait(3)

        # elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'MacBook Air 搭配 Apple M4 晶片')]")
        elements = driver.find_elements(By.XPATH, "//span[contains(text(), '顯示器')]")

        # messages = "\n".join([e.text for e in elements]) if elements else "❌ 查無符合條件的商品"

        if elements:
            messages=''
            for i, element in enumerate(elements, start=1):
                messages+=f"{i}.{element.text}\n"
        else:
            messages=("❌ 查無符合條件的商品")

        send_line_push(
            user_id=os.getenv("LINE_USER_ID"),
            message=f"📦 Costco TV 今日查詢結果：\n{messages}",
            token=os.getenv("LINE_CHANNEL_TOKEN")
        )
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
