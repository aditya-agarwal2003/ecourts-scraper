# def run_selenium_scraper(case_type, case_year, case_status):
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support.ui import Select, WebDriverWait
#     from selenium.webdriver.support import expected_conditions as EC
#     import time

#     driver = webdriver.Chrome()
#     driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

#     # Click "Case Status"
#     WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()

#     # Select State, District, Court with automated change events
#     def select_and_trigger(by_locator, value, select_by_text=False):
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located(by_locator))
#         el = Select(driver.find_element(*by_locator))
#         if select_by_text:
#             el.select_by_visible_text(value)
#         else:
#             el.select_by_value(value)
#         driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(*by_locator))

#     select_and_trigger((By.NAME, "sess_state_code"), "14")
#     select_and_trigger((By.NAME, "sees_dist_code"), "5")
#     select_and_trigger((By.ID, "court_complex_code"), "District Court, Faridabad", select_by_text=True)

#     time.sleep(1)
#     driver.execute_script("closeModel({modal_id:'validateError'})")

#     # Open and validate Case Type tab
#     driver.execute_script("document.getElementById('casetype-tabMenu').click();")
#     driver.execute_script("validateStateDistCourt('casetype-tabMenu');")
#     time.sleep(1)
#     driver.execute_script("closeModel({modal_id:'validateError'})")

#     # Now wait until case_type field is visible
#     WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "case_type_1")))
#     driver.find_element(By.NAME, "case_type_1").send_keys(case_type)
#     driver.find_element(By.NAME, "search_year").send_keys(case_year)

#     # Status radio
#     if case_status.lower() == "pending":
#         driver.find_element(By.ID, "radPCT").click()
#     else:
#         driver.find_element(By.ID, "radDCT").click()

#     # If CAPTCHA is pending
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))
#     driver.find_element(By.ID, "captcha_image").screenshot("captcha.png")
#     print("🧩 CAPTCHA saved as captcha.png")
#     input("Enter CAPTCHA and hit Enter...")

#     driver.find_element(By.NAME, "ct_captcha_code").send_keys(input("Enter CAPTCHA value: "))
#     driver.execute_script("submitCaseType();")

#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dispTable")))
#     rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")

#     results = []
#     for tr in rows:
#         cols = tr.find_elements(By.TAG_NAME, "td")
#         if len(cols) == 4:
#             results.append({
#                 "sr_no": cols[0].text.strip(),
#                 "case_info": cols[1].text.strip(),
#                 "parties": cols[2].text.strip().replace("\n", " "),
#                 "action": cols[3].text.strip()
#             })
#         elif len(cols) == 1:
#             results.append({"court_name": cols[0].text.strip()})

#     driver.quit()
#     return results


# def run_selenium_scraper(case_type, case_year, case_status):
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support.ui import Select, WebDriverWait
#     from selenium.webdriver.support import expected_conditions as EC
#     import time
#     from selenium.webdriver.chrome.options import Options

#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--window-size=1920,1080')

#     driver = webdriver.Chrome(options=options)
#     driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
#     time.sleep(2)

#     state_dropdown = driver.find_element(By.NAME, "sess_state_code")
#     Select(state_dropdown).select_by_value("14")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", state_dropdown)
#     time.sleep(1)

#     district_dropdown = driver.find_element(By.NAME, "sees_dist_code")
#     Select(district_dropdown).select_by_value("5")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", district_dropdown)
#     time.sleep(2)

#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#     court_dropdown = driver.find_element(By.ID, "court_complex_code")
#     Select(court_dropdown).select_by_visible_text("District Court, Faridabad")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", court_dropdown)
#     time.sleep(3)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     driver.execute_script("document.getElementById('casetype-tabMenu').click();")
#     driver.execute_script("validateStateDistCourt('casetype-tabMenu');")
#     time.sleep(3)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     driver.find_element(By.NAME, "case_type_1").send_keys(case_type)
#     driver.find_element(By.NAME, "search_year").send_keys(case_year)

#     if case_status.lower() == "pending":
#         driver.find_element(By.ID, "radPCT").click()
#     elif case_status.lower() == "disposed":
#         driver.find_element(By.ID, "radDCT").click()
#     else:
#         print("❌ Invalid status")
#         driver.quit()
#         return []

#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))

#     captcha_element = driver.find_element(By.ID, "captcha_image")
#     captcha_element.screenshot("captcha.png")
#     print("CAPTCHA saved as captcha.png")
#     captcha_code = input("Enter CAPTCHA: ")

#     driver.find_element(By.ID, "ct_captcha_code").send_keys(captcha_code)
#     driver.execute_script("submitCaseType();")
#     time.sleep(3)

#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dispTable")))
#     table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")

#     results = []
#     for row in table_rows:
#         cells = row.find_elements(By.TAG_NAME, "td")
#         if len(cells) == 4:
#             results.append({
#                 "sr_no": cells[0].text.strip(),
#                 "case_info": cells[1].text.strip(),
#                 "parties": cells[2].text.strip().replace("\n", " "),
#                 "action": cells[3].text.strip()
#             })
#         elif len(cells) == 1:
#             results.append({
#                 "court_name": cells[0].text.strip()
#             })

#     driver.quit()
#     return results



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

#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
#     time.sleep(2)

#     state_dropdown = driver.find_element(By.NAME, "sess_state_code")
#     Select(state_dropdown).select_by_value("14")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", state_dropdown)
#     time.sleep(1)

#     district_dropdown = driver.find_element(By.NAME, "sees_dist_code")
#     Select(district_dropdown).select_by_value("5")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", district_dropdown)
#     time.sleep(1)

#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#     court_dropdown = driver.find_element(By.ID, "court_complex_code")
#     Select(court_dropdown).select_by_visible_text("District Court, Faridabad")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", court_dropdown)
#     time.sleep(1)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
#     time.sleep(2)  # Optional, you can also wait explicitly if needed

#     # Close any modal if it appears
#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     # Wait and select case_type
# # Wait until the case type dropdown is present and has at least one real <option>
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "case_type"))
#     )

#     # Wait for options to be available (not just the placeholder)
#     def case_type_loaded(driver):
#         select_elem = driver.find_element(By.NAME, "case_type")
#         options = select_elem.find_elements(By.TAG_NAME, "option")
#         return len(options) > 1  # i.e., not just "Select Case Type"

#     WebDriverWait(driver, 10).until(case_type_loaded)

#     # Now select the mapped case type
#     case_type_map = {
#         "CA": "1^3",
#         "CS": "4^3",
#         "BA": "25^3",
#         "MACP": "43^3",
#         "NDPS": "27^3",
#         # Add more if needed
#     }

#     value = case_type_map.get(case_type)
#     if not value:
#         print(f"❌ Unknown case type: {case_type}")
#         driver.quit()
#         return []

#     Select(driver.find_element(By.NAME, "case_type")).select_by_value(value)













    # driver.find_element(By.NAME, "search_year").send_keys(case_year)

    # if case_status.lower() == "pending":
    #     driver.find_element(By.ID, "radPCT").click()
    # elif case_status.lower() == "disposed":
    #     driver.find_element(By.ID, "radDCT").click()
    # else:
    #     print("❌ Invalid status")
    #     driver.quit()
    #     return []

    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))

    # captcha_element = driver.find_element(By.ID, "captcha_image")
    # captcha_element.screenshot("captcha.png")
    # print("CAPTCHA saved as captcha.png")
    # captcha_code = input("Enter CAPTCHA: ")

    # driver.find_element(By.ID, "ct_captcha_code").send_keys(captcha_code)
    # driver.execute_script("submitCaseType();")
    # time.sleep(3)

    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dispTable")))
    # table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")

    # results = []
    # for row in table_rows:
    #     cells = row.find_elements(By.TAG_NAME, "td")
    #     if len(cells) == 4:
    #         results.append({
    #             "sr_no": cells[0].text.strip(),
    #             "case_info": cells[1].text.strip(),
    #             "parties": cells[2].text.strip().replace("\n", " "),
    #             "action": cells[3].text.strip()
    #         })
    #     elif len(cells) == 1:
    #         results.append({
    #             "court_name": cells[0].text.strip()
    #         })

    # driver.quit()
    # return results

from ocr_utils import solve_captcha

def run_selenium_scraper(case_type, case_no, case_year, case_status):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    from selenium.webdriver.chrome.options import Options
      # 🧠 Make sure this is at the top of your file

    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
    time.sleep(2)

    Select(driver.find_element(By.NAME, "sess_state_code")).select_by_value("14")  # Haryana
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sess_state_code"))
    time.sleep(1)

    Select(driver.find_element(By.NAME, "sees_dist_code")).select_by_value("5")  # Faridabad
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sees_dist_code"))
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
    Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text("District Court, Faridabad")
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.ID, "court_complex_code"))
    time.sleep(1)

    try:
        driver.execute_script("closeModel({modal_id:'validateError'})")
    except:
        pass

    # ✅ Switch to Case Number tab
    driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
    time.sleep(2)

    try:
        driver.execute_script("closeModel({modal_id:'validateError'})")
    except:
        pass

    # ✅ Select case type
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))
    Select(driver.find_element(By.NAME, "case_type")).select_by_value(case_type)

    # ✅ Fill case number and year
    driver.find_element(By.NAME, "search_case_no").send_keys(case_no)
    driver.find_element(By.NAME, "rgyear").send_keys(case_year)

    # ✅ CAPTCHA
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "case_captcha_code")))
    # captcha_element = driver.find_element(By.ID, "case_captcha_code")
    # captcha_element.screenshot("captcha.png")
    # captcha_code = input("Enter CAPTCHA: ")
    # driver.find_element(By.ID, "case_captcha_code").send_keys(captcha_code)
   
   
   
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))
    captcha_element = driver.find_element(By.ID, "captcha_image")

    captcha_path = "captcha.png"
    captcha_element.screenshot(captcha_path)

    captcha_code = solve_captcha(captcha_path)
    print(f"✅ CAPTCHA solved as: {captcha_code}")

    driver.find_element(By.ID, "case_captcha_code").send_keys(captcha_code)



    driver.execute_script("submitCaseNo();")  # ⬅️ Make sure you use correct function (not CaseType!)
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
                "view_text": cells[3].text.strip()
            })
        elif len(cells) == 1:
            results.append({
                "court_name": cells[0].text.strip()
            })

    driver.quit()
    return results
