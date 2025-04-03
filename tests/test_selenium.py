import time
import uuid
import os
import pytest
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

BASE_URL = "http://localhost:3000"


@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if os.getenv("GITHUB_ACTIONS") == "true":
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        driver = webdriver.Chrome(options=chrome_options)
        print("Running in GitHub Actions")
    else:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver = webdriver.Chrome()  # 本地测试时使用默认配置
    driver.maximize_window()
    yield driver
    driver.quit()

def wait_for_element(driver, by, value, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def test_signup_and_login_flow(driver):
    driver.get(BASE_URL + "/login")
    wait_for_element(driver, By.XPATH, "//*[contains(text(), 'Welcome back')]")

    signup_link = driver.find_element(By.LINK_TEXT, "Sign up")
    signup_link.click()
    wait_for_element(driver, By.ID, "email")

    import uuid
    unique_email = f"{uuid.uuid4()}@example.com"  
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    username_input = driver.find_element(By.ID, "username")

    email_input.clear()
    email_input.send_keys(unique_email)
    password_input.clear()
    password_input.send_keys(unique_email)  
    username_input.clear()
    username_input.send_keys(unique_email)  

    signup_button = driver.find_element(By.XPATH, "//button[contains(text(),'Sign up')]")
    signup_button.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    assert "Sign Up Successful!" in alert_text, f"The registration prompt is abnormal, and a prompt is received:{alert_text}"
    alert.accept()

    WebDriverWait(driver, 10).until(EC.url_contains("/login"))
    assert "/login" in driver.current_url

    email_input = wait_for_element(driver, By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    email_input.clear()
    email_input.send_keys(unique_email)
    password_input.clear()
    password_input.send_keys(unique_email)

    login_button = driver.find_element(By.XPATH, "//button[text()='Log in']")
    login_button.click()

    WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
    assert "/profile" in driver.current_url
    
def test_full_flow(driver):
    driver.get(BASE_URL + "/profile")
    time.sleep(2)

    edit_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Edit']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
    time.sleep(1)
    edit_btn.click()
    time.sleep(2)

    weight_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "weight"))
    )
    height_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "height"))
    )

    driver.execute_script("arguments[0].removeAttribute('readonly');", weight_input)
    driver.execute_script("arguments[0].removeAttribute('disabled');", weight_input)
    driver.execute_script("arguments[0].removeAttribute('readonly');", height_input)
    driver.execute_script("arguments[0].removeAttribute('disabled');", height_input)
    
    driver.execute_script("arguments[0].scrollIntoView(true);", weight_input)
    time.sleep(1)
    
    weight_input.clear()
    weight_input.send_keys("50")
    height_input.clear()
    height_input.send_keys("1.655")
    
    save_profile_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))
    )
    save_profile_btn.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)
    
    assert weight_input.get_attribute("disabled") is not None, "Weight input not ban"
    assert height_input.get_attribute("disabled") is not None, "Height input not ban"

    preferences_btn = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Preferences')]")
    preferences_btn.click()
    time.sleep(2)

    what_i_like_container = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(., 'What I like?')]"))
    )

    edit_button = what_i_like_container.find_element(By.XPATH, ".//button[text()='Edit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", edit_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", edit_button)
    time.sleep(1)
    tag_input = WebDriverWait(what_i_like_container, 20).until(
        EC.visibility_of_element_located((By.XPATH, ".//input[@placeholder='add your tag :)']"))
    )
    tag_input.clear()
    tag_input.send_keys("meat" + Keys.ENTER)
    time.sleep(1)

    save_button = WebDriverWait(what_i_like_container, 20).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[contains(text(),'Save')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", save_button)
    time.sleep(2)

def test_fridge_add_food(driver):
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    
    try:
        fridge_option = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "nav a[href='/fridge']"))
        )
        fridge_option.click()
        time.sleep(2)
    except Exception as e:
        print("【Fridge】 Failed to click the 'FRIDGE' link in Navbar. Page source code:")
        print(driver.page_source)
        raise e

    try:
        add_food_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '+ Add Food')]"))
        )
        add_food_btn.click()
        time.sleep(2)
    except Exception as e:
        print("Fridge failed to click the '+ Add Food' button. Page source code:")
        print(driver.page_source)
        raise e

    try:
        food_name_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Food Name']"))
        )
        food_name_input.clear()
        food_name_input.send_keys("beef")
    except Exception as e:
        print("Fridge could not locate the 'Food Name' input box. Page source code:")
        print(driver.page_source)
        raise e

    try:
        category_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select.border.px-3.py-2.w-full"))
        )

        driver.execute_script("arguments[0].click();", category_select)
        time.sleep(1)
        select_obj = Select(category_select)
        select_obj.select_by_visible_text("meat")
        time.sleep(1)
    except Exception as e:
        print("Fridge failed to select category 'meat'. Page source code:")
        print(driver.page_source)
        raise e
    
    try:
        add_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", add_button)
        time.sleep(2)
    except Exception as e:
        print("Fridge failed to select category 'meat'. Page source code:")
        print(driver.page_source)
        raise e



def test_recipe_drag_spicy_and_start_cook(driver):
    try:
        recipe_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "nav a[href='/recipe_gen']"))
        )
        recipe_link.click()
        time.sleep(2)
    except Exception as e:
        print("【Recipe】 Failed to click the 'RECIPE' link in Navbar. Page source code:")
        print(driver.page_source)
        raise e

    try:
        sweet_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='inline-block bg-gray-800 text-white rounded px-2 py-1 cursor-move' and text()='sweet']"))
        )
    except Exception as e:
        print("【Recipe】 Failed to locate the 'sweet' tag. Page source code:")
        print(driver.page_source)
        raise e
    
    try:
        beef_label = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='beef']"))
        )
        print("find food tag:", beef_label.text)
    except Exception as e:
        print("cannot find 'beef' Tag. Page source code:")
        print(driver.page_source)
        raise e

    try:
        pot_area = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//section[contains(@class,'relative flex flex-col items-center justify-center') and .//button[contains(text(),'start cook')]]"))
        )
    except Exception as e:
        print("【Recipe】 Failed to position pot area. Page source code:")
        print(driver.page_source)
        raise e

    try:
        action = ActionChains(driver)
        action.drag_and_drop(sweet_tag, pot_area).perform()
        time.sleep(1)
    except Exception as e:
        print("【Recipe】 Dragging 'sweet' TAB to pot area fails. Page source code:")
        print(driver.page_source)
        raise e
    
    try:
        action = ActionChains(driver)
        action.drag_and_drop(beef_label, pot_area).perform()
        time.sleep(1)
    except Exception as e:
        print("【Recipe】 Dragging 'sweet' TAB to pot area fails. Page source code:")
        print(driver.page_source)
        raise e

    try:
        start_cook_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                "//section[contains(@class,'flex flex-col items-center justify-center')]//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'start cook')]"
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", start_cook_button)
        time.sleep(1)
        start_cook_button.click()
        time.sleep(2)
    except Exception as e:
        print("[Recipe] The 'start cook' button in the pot area could not be clicked. Page source code:")
        print(driver.page_source)
        raise e


    try:
        pop_out_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'pop-out-animation')]"))
        )
        pop_out_button.click()
        time.sleep(2)
    except Exception as e:
        print("【Recipe: Failed to click the round button (pop-out animation). Page source code:")
        print(driver.page_source)
        raise e