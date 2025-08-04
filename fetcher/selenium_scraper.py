def run_selenium_scraper(case_type, case_year, case_status):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    driver = webdriver.Chrome()
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
    time.sleep(2)

    state_dropdown = driver.find_element(By.NAME, "sess_state_code")
    Select(state_dropdown).select_by_value("14")
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", state_dropdown)
    time.sleep(1)

    district_dropdown = driver.find_element(By.NAME, "sees_dist_code")
    Select(district_dropdown).select_by_value("5")
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", district_dropdown)
    time.sleep(2)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
    court_dropdown = driver.find_element(By.ID, "court_complex_code")
    Select(court_dropdown).select_by_visible_text("District Court, Faridabad")
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", court_dropdown)
    time.sleep(3)

    try:
        driver.execute_script("closeModel({modal_id:'validateError'})")
    except:
        pass

    driver.execute_script("document.getElementById('casetype-tabMenu').click();")
    driver.execute_script("validateStateDistCourt('casetype-tabMenu');")
    time.sleep(3)

    try:
        driver.execute_script("closeModel({modal_id:'validateError'})")
    except:
        pass

    driver.find_element(By.NAME, "case_type_1").send_keys(case_type)
    driver.find_element(By.NAME, "search_year").send_keys(case_year)

    if case_status.lower() == "pending":
        driver.find_element(By.ID, "radPCT").click()
    elif case_status.lower() == "disposed":
        driver.find_element(By.ID, "radDCT").click()
    else:
        print("❌ Invalid status")
        driver.quit()
        return []

    captcha_element = driver.find_element(By.ID, "captcha_image")
    captcha_element.screenshot("captcha.png")
    print("CAPTCHA saved as captcha.png")
    captcha_code = input("Enter CAPTCHA: ")

    driver.find_element(By.ID, "ct_captcha_code").send_keys(captcha_code)
    driver.execute_script("submitCaseType();")
    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dispTable")))
    table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")

    results = []
    for row in table_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 4:
            results.append({
                "sr_no": cells[0].text.strip(),
                "case_info": cells[1].text.strip(),
                "parties": cells[2].text.strip().replace("\n", " "),
                "action": cells[3].text.strip()
            })
        elif len(cells) == 1:
            results.append({
                "court_name": cells[0].text.strip()
            })

    driver.quit()
    return results



# def run_selenium_scraper(case_type, case_year, case_status):
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support.ui import Select, WebDriverWait
#     from selenium.webdriver.support import expected_conditions as EC
#     import time
#     # from selenium.webdriver.chrome.options import Options  # ❌ Not needed unless using headless

#     # ✅ Use visible browser, so no options required
#     driver = webdriver.Chrome()
#     driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

#     # 1. Go to Case Status
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
#     time.sleep(2)

#     # 2. Select State
#     state_dropdown = driver.find_element(By.NAME, "sess_state_code")
#     Select(state_dropdown).select_by_value("14")  # Haryana
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", state_dropdown)
#     time.sleep(1)

#     # 3. Select District
#     district_dropdown = driver.find_element(By.NAME, "sees_dist_code")
#     Select(district_dropdown).select_by_value("5")  # Faridabad
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", district_dropdown)
#     time.sleep(2)

#     # 4. Select Court Complex
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#     court_dropdown = driver.find_element(By.ID, "court_complex_code")
#     Select(court_dropdown).select_by_visible_text("District Court, Faridabad")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", court_dropdown)
#     time.sleep(3)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#         print("✅ Closed error modal using JS.")
#     except:
#         print("⚠️ Could not close modal — maybe it wasn't open.")

#     # 5. Open Case Type tab
#     driver.execute_script("document.getElementById('casetype-tabMenu').click();")
#     driver.execute_script("validateStateDistCourt('casetype-tabMenu');")
#     time.sleep(3)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     # 6. Fill form inputs (use function arguments, not input())
#     driver.find_element(By.NAME, "case_type_1").send_keys(case_type)
#     driver.find_element(By.NAME, "search_year").send_keys(case_year)

#     if case_status.lower() == "pending":
#         driver.find_element(By.ID, "radPCT").click()
#     elif case_status.lower() == "disposed":
#         driver.find_element(By.ID, "radDCT").click()
#     else:
#         print("❌ Invalid status. Use 'pending' or 'disposed'.")
#         return

#     # 7. CAPTCHA (ask user manually)
#     captcha_element = driver.find_element(By.ID, "captcha_image")
#     captcha_element.screenshot("captcha.png")  # Save to local file
#     print("🧩 CAPTCHA saved as captcha.png — open and read it.")
#     captcha_code = input("Enter CAPTCHA: ")

#     driver.find_element(By.ID, "ct_captcha_code").send_keys(captcha_code)

#     # 8. Submit
#     driver.execute_script("submitCaseType();")
#     time.sleep(3)

#     # 9. Wait for results table
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dispTable")))
#     table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")

#     print("\n📋 Case Results:\n")
#     for row in table_rows:
#         cells = row.find_elements(By.TAG_NAME, "td")
#         if len(cells) == 4:
#             sr_no = cells[0].text.strip()
#             case_info = cells[1].text.strip()
#             parties = cells[2].text.strip().replace("\n", " ")
#             view_text = cells[3].text.strip()
#             print(f"{sr_no}. {case_info}")
#             print(f"    Parties: {parties}")
#             print(f"    Action: {view_text}")
#             print("-" * 50)
#         else:
#             print(cells[0].text.strip())
#             print("-" * 50)

#     input("\nPress Enter to close browser...")
#     driver.quit()












# def run_selenium_scraper(case_type, case_year, case_status):
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support.ui import Select, WebDriverWait
#     from selenium.webdriver.support import expected_conditions as EC
#     import time
#     from selenium.webdriver.chrome.options import Options

#     options = Options()
#     # options.add_argument('--headless')
#     # options.add_argument('--disable-gpu')
#     # options.add_argument('--no-sandbox')
#     # options.add_argument('--window-size=1920,1080')

#     driver = webdriver.Chrome(options=options)
#     driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

#     # 1. Go to Case Status
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
#     time.sleep(2)

#     # 2. Select State
#     state_dropdown = driver.find_element(By.NAME, "sess_state_code")
#     Select(state_dropdown).select_by_value("14")  # Haryana
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", state_dropdown)
#     time.sleep(1)

#     # 3. Select District
#     district_dropdown = driver.find_element(By.NAME, "sees_dist_code")
#     Select(district_dropdown).select_by_value("5")  # Faridabad
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", district_dropdown)
#     time.sleep(2)

#     # 4. Select Court Complex
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#     court_dropdown = driver.find_element(By.ID, "court_complex_code")
#     Select(court_dropdown).select_by_visible_text("District Court, Faridabad")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", court_dropdown)
#     time.sleep(3)
#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#         print("✅ Closed error modal using JS.")
#     except:
#         print("⚠️ Could not close modal — maybe it wasn't open.")
#     # 5. Now safely validate to open Case Type tab
#     # 1. Trigger the tab click like Bootstrap expects
#     driver.execute_script("document.getElementById('casetype-tabMenu').click();")

#     # 2. Manually trigger the validation function too (just in case)
#     driver.execute_script("validateStateDistCourt('casetype-tabMenu');")

#     time.sleep(3)

#     # 👇 Close the modal if it reappears
#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#         print("✅ Closed popup after Case Type tab.")
#     except:
#         print("⚠️ Modal not found after tab click.")
#     # 4. Ask user for case details
#     case_type = input("Enter Case Type (e.g., CA): ")

#     driver.find_element(By.NAME, "case_type_1").send_keys(case_type)

#     case_year = input("Enter Case Year (e.g., 2022): ")

#     driver.find_element(By.NAME, "search_year").send_keys(case_year)

#     status = input("Enter Case Status (Pending / Disposed): ").strip().lower()

#     if status == "pending":
#         driver.find_element(By.ID, "radPCT").click()
#     elif status == "disposed":
#         driver.find_element(By.ID, "radDCT").click()
#     else:
#         print("❌ Invalid status entered. Please enter 'Pending' or 'Disposed'.")

#     captcha_element = driver.find_element(By.ID, "captcha_image")

#     # Save screenshot of that element only
#     captcha_element.screenshot("captcha.png")

#     print("✅ CAPTCHA image saved as 'captcha.png'. Please open it and type the code.")
#     captcha_code = input("Enter CAPTCHA: ")

#     # Fill the CAPTCHA field
#     driver.find_element(By.ID, "ct_captcha_code").send_keys(captcha_code)

#     driver.execute_script("submitCaseType();")
#     time.sleep(3)

#     # ✅ Wait until table appears
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "dispTable"))
#     )

#     # ✅ Get all rows from tbody (excluding header row)
#     table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")

#     print("\n📋 Case Results:\n")
#     for row in table_rows:
#         cells = row.find_elements(By.TAG_NAME, "td")
#         if len(cells) == 4:
#             sr_no = cells[0].text.strip()
#             case_info = cells[1].text.strip()
#             parties = cells[2].text.strip().replace("\n", " ")
#             view_text = cells[3].text.strip()  # usually "View" link
#             print(f"{sr_no}. {case_info}")
#             print(f"    Parties: {parties}")
#             print(f"    Action: {view_text}")
#             print("-" * 50)
#         else:
#             # Optional: Print merged rows (like court name row with colspan)
#             print(cells[0].text.strip())
#             print("-" * 50)
#     input("\nPress Enter to close browser...")