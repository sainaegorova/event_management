from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Путь к драйверу (например, для Chrome)
driver_path = 'C:/chromedriver'
driver = webdriver.Chrome()

try:
    # Открыть главную страницу
    driver.get("http://127.0.0.1:5000/")
    time.sleep(5)  # Подождать, чтобы страница загрузилась

    # Тестирование страницы входа
    driver.find_element(By.LINK_TEXT, "Login").click()  # Переход на страницу входа
    time.sleep(2)  # Дождаться загрузки страницы входа

    # Вводим данные для входа
    driver.find_element(By.NAME, "email").send_keys("test@example.com")  # Замените на тестовый email
    driver.find_element(By.NAME, "password").send_keys("password")  # Замените на тестовый пароль
    driver.find_element(By.TAG_NAME, "button").click()  # Нажимаем кнопку "Login"
    time.sleep(5)  # Подождать, чтобы загрузилась следующая страница после входа

    # Тестирование создания события (после успешного входа)
    # Убедитесь, что "Create Event" виден и доступен для клика
    create_event_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Create Event"))
    )
    create_event_link.click()  # Переход на страницу создания события
    time.sleep(2)  # Подождать, чтобы страница загрузилась

    # Вводим данные для создания события
    driver.find_element(By.NAME, "name").send_keys("Test Event")  # Название события
    driver.find_element(By.NAME, "date").send_keys("1132024")  # Дата события
    driver.find_element(By.NAME, "date").send_keys(Keys.RETURN)  # Отправляем форму
    time.sleep(5)  # Подождать, чтобы подтверждение создания события загрузилось

    # Тестирование регистрации на событие
    driver.find_element(By.LINK_TEXT, "Test Event (2024-03-11)").click()  # Переход на страницу события
    time.sleep(20)  # Подождать, чтобы страница загрузилась

    # Вводим данные для регистрации на событие
    driver.find_element(By.NAME, "name").send_keys("Participant Name")  # Имя участника
    driver.find_element(By.NAME, "email").send_keys("participant@example.com")  # Email участника
    driver.find_element(By.NAME, "email").send_keys(Keys.RETURN)  # Отправляем форму
    time.sleep(5)  # Подождать, чтобы подтверждение регистрации загрузилось


finally:
    # Закрыть браузер
    driver.quit()