# from ocr_utils import solve_captcha

# def run_selenium_scraper(case_type, case_no, case_year, case_status):
#     from selenium.common.exceptions import TimeoutException
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

#     Select(driver.find_element(By.NAME, "sess_state_code")).select_by_value("14")  # Haryana
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sess_state_code"))
#     time.sleep(1)

#     Select(driver.find_element(By.NAME, "sees_dist_code")).select_by_value("5")  # Faridabad
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sees_dist_code"))
#     time.sleep(1)

#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#     Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text("District Court, Faridabad")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.ID, "court_complex_code"))
#     time.sleep(1)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     # ✅ Switch to Case Number tab
#     driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
#     time.sleep(2)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     # Wait for the case type dropdown and ensure real options are loaded
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))

#     def case_type_options_loaded(driver):
#         dropdown = driver.find_element(By.NAME, "case_type")
#         options = dropdown.find_elements(By.TAG_NAME, "option")
#         return len(options) > 1  # >1 to ensure options are loaded (not just placeholder)

#     MAX_RETRIES = 3
#     for attempt in range(MAX_RETRIES):
#         try:
#             # Wait until case_type dropdown is present
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))

#             # Wait until case_type dropdown options are loaded (not just "Select Case Type")
#             def case_type_options_loaded(driver):
#                 select_elem = driver.find_element(By.NAME, "case_type")
#                 options = select_elem.find_elements(By.TAG_NAME, "option")
#                 return len(options) > 1  # real options loaded

#             WebDriverWait(driver, 15).until(case_type_options_loaded)

#             # Select your value now
#             Select(driver.find_element(By.NAME, "case_type")).select_by_value(case_type)
#             break  # ✅ done, exit the retry loop

#         except TimeoutException:
#             print(f"⚠️ Attempt {attempt+1}: Dropdown options didn't load. Retrying...")

#             # Try to click on the refresh link if it exists
#             try:
#                 refresh_link = driver.find_element(By.LINK_TEXT, "Click here to refresh again")
#                 refresh_link.click()
#                 time.sleep(3)
#             except:
#                 pass  # No refresh link found

#             # Start again from selecting state/district/court
#             try:
#                 Select(driver.find_element(By.NAME, "sess_state_code")).select_by_value("14")  # Haryana
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sess_state_code"))
#                 time.sleep(1)

#                 Select(driver.find_element(By.NAME, "sees_dist_code")).select_by_value("5")  # Faridabad
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sees_dist_code"))
#                 time.sleep(1)

#                 WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#                 Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text("District Court, Faridabad")
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.ID, "court_complex_code"))
#                 time.sleep(1)

#                 driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
#                 time.sleep(2)

#                 # close modal again
#                 try:
#                     driver.execute_script("closeModel({modal_id:'validateError'})")
#                 except:
#                     pass

#             except Exception as e:
#                 print(f"🔥 Error during retry state/district setup: {e}")
#                 break
#     else:
#         print("❌ Max retries reached. Exiting.")
#         driver.quit()
#         return []


#     # ✅ Fill case number and year
#     driver.find_element(By.NAME, "search_case_no").send_keys(case_no)
#     driver.find_element(By.NAME, "rgyear").send_keys(case_year)

#     # ✅ CAPTCH
#     for attempt in range(10):
#         print(f"🔁 Attempting CAPTCHA — Try #{attempt + 1}")

#         # Step 1: Wait and screenshot CAPTCHA image
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))
#         captcha_element = driver.find_element(By.ID, "captcha_image")
#         captcha_element.screenshot("captcha.png")

#         # Step 2: Solve CAPTCHA using Tesseract
#         captcha_text = solve_captcha("captcha.png")
#         print(f"🧠 Predicted CAPTCHA: {captcha_text}")

#         # Step 3: Fill the CAPTCHA input
#         input_box = driver.find_element(By.ID, "case_captcha_code")
#         input_box.clear()
#         input_box.send_keys(captcha_text)

#         # Step 4: Submit
#         driver.execute_script("submitCaseNo();")
#         time.sleep(3)

#         # Step 5: If results appear, break loop
#         try:
#             WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "dispTable")))
#             print("✅ CAPTCHA accepted — table loaded.")
#             break
#         except:
#             print("❌ CAPTCHA incorrect. Retrying...")

#             # Close error modal if it appears
#             try:
#                 driver.execute_script("closeModel({modal_id:'validateError'})")
#                 print("⚠️ Closed CAPTCHA error modal.")
#             except:
#                 pass

#             time.sleep(2)
#     else:
#         print("❌ Failed after 10 attempts.")
#         driver.quit()
#         return []
#     table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")
#     results = []
#     for row in table_rows:
#         cells = row.find_elements(By.TAG_NAME, "td")
#         if len(cells) == 4:
#             results.append({
#                 "sr_no": cells[0].text.strip(),
#                 "case_info": cells[1].text.strip(),
#                 "parties": cells[2].text.strip().replace("\n", " "),
#                 "view_text": cells[3].text.strip()
#             })
#         elif len(cells) == 1:
#             results.append({
#                 "court_name": cells[0].text.strip()
#             })
#     driver.quit()
#     return results



































from ocr_utils import solve_captcha
import html
import requests

def run_selenium_scraper(case_type, case_no, case_year, case_status):
    from selenium.common.exceptions import TimeoutException
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    from selenium.webdriver.chrome.options import Options
    import re
    import shlex


    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    BASE = "https://services.ecourts.gov.in/ecourtindia_v6/"
    driver.get(BASE)

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

    # Wait for the case type dropdown and ensure real options are loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))

    def case_type_options_loaded(driver):
        dropdown = driver.find_element(By.NAME, "case_type")
        options = dropdown.find_elements(By.TAG_NAME, "option")
        return len(options) > 1  # >1 to ensure options are loaded (not just placeholder)

    MAX_RETRIES = 3
    for attempt in range(MAX_RETRIES):
        try:
            # Wait until case_type dropdown is present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))

            # Wait until case_type dropdown options are loaded (not just "Select Case Type")
            def case_type_options_loaded(driver):
                select_elem = driver.find_element(By.NAME, "case_type")
                options = select_elem.find_elements(By.TAG_NAME, "option")
                return len(options) > 1  # real options loaded

            WebDriverWait(driver, 15).until(case_type_options_loaded)

            # Select your value now
            Select(driver.find_element(By.NAME, "case_type")).select_by_value(case_type)
            break  # ✅ done, exit the retry loop

        except TimeoutException:
            print(f"⚠️ Attempt {attempt+1}: Dropdown options didn't load. Retrying...")

            # Try to click on the refresh link if it exists
            try:
                refresh_link = driver.find_element(By.LINK_TEXT, "Click here to refresh again")
                refresh_link.click()
                time.sleep(3)
            except:
                pass  # No refresh link found

            # Start again from selecting state/district/court
            try:
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

                driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
                time.sleep(2)

                # close modal again
                try:
                    driver.execute_script("closeModel({modal_id:'validateError'})")
                except:
                    pass

            except Exception as e:
                print(f"🔥 Error during retry state/district setup: {e}")
                break
    else:
        print("❌ Max retries reached. Exiting.")
        driver.quit()
        return []


    # ✅ Fill case number and year
    driver.find_element(By.NAME, "search_case_no").send_keys(case_no)
    driver.find_element(By.NAME, "rgyear").send_keys(case_year)

    # ✅ CAPTCH
    for attempt in range(10):
        print(f"🔁 Attempting CAPTCHA — Try #{attempt + 1}")

        # Step 1: Wait and screenshot CAPTCHA image
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))
        captcha_element = driver.find_element(By.ID, "captcha_image")
        captcha_element.screenshot("captcha.png")

        # Step 2: Solve CAPTCHA using Tesseract
        captcha_text = solve_captcha("captcha.png")
        print(f"🧠 Predicted CAPTCHA: {captcha_text}")

        # Step 3: Fill the CAPTCHA input
        input_box = driver.find_element(By.ID, "case_captcha_code")
        input_box.clear()
        input_box.send_keys(captcha_text)

        # Step 4: Submit
        driver.execute_script("submitCaseNo();")
        time.sleep(3)

        # Step 5: If results appear, break loop
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "dispTable")))
            print("✅ CAPTCHA accepted — table loaded.")
            break
        except:
            print("❌ CAPTCHA incorrect. Retrying...")

            # Close error modal if it appears
            try:
                driver.execute_script("closeModel({modal_id:'validateError'})")
                print("⚠️ Closed CAPTCHA error modal.")
            except:
                pass

            time.sleep(2)
    else:
        print("❌ Failed after 10 attempts.")
        driver.quit()
        return []
    table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")
    results = {}
    for row in table_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 4:
            
            parties = cells[2].text.strip().replace("\n", " ")
            results['parties_name'] = parties

            try:
                # ⏩ Extract onclick from <a>
                view_button = cells[3].find_element(By.TAG_NAME, "a")
                onclick_attr = view_button.get_attribute("onclick")
                print(f"👉 onclick = {onclick_attr}")

                match = re.search(r"viewHistory\((.*?)\)", onclick_attr)
                if match:
                    raw_args = match.group(1)

                    lexer = shlex.shlex(raw_args, posix=True)
                    lexer.whitespace = ','
                    lexer.whitespace_split = True
                    lexer.quotes = "'"
                    args = list(lexer)
                    # print("409")
                    if len(args) == 9:
                        # ✅ Call viewHistory
                        driver.execute_script(f"viewHistory({','.join(repr(a) for a in args)})")
                        time.sleep(3)

                        label_elem = driver.find_element(By.XPATH, "//td/label[normalize-space()='Filing Date']")
                        # Get the following td (the date cell)
                        date_td = label_elem.find_element(By.XPATH, "./parent::td/following-sibling::td")
                        filing_date = date_td.text.strip()
                        results['filing_date'] = filing_date

                        hearing_date_elem = driver.find_element(
                            By.XPATH,
                            "//td/label[normalize-space()='Next Hearing Date']/parent::td/following-sibling::td"
                        )

                        next_hearing_date = hearing_date_elem.text.strip()
                        results['next_hearing_date'] = next_hearing_date

                       
                        # Find all <a> tags that have displayPdf in onclick
                        a_tags = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'displayPdf')]")
                        latest_pdf_tag = a_tags[-1]

                        driver.execute_script("arguments[0].click();", latest_pdf_tag)


                        # Wait for modal to load <object> or <iframe> containing PDF
                        obj = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//object[@data] | //iframe[@src]"))
                        )

                        url = obj.get_attribute("data") or obj.get_attribute("src")
                        print(url)
                        if url and not url.startswith("http"):
                            url = BASE + url
                        print(url)
                        results['latest_judgement_pdf_link'] = url
                        from ipdb import set_trace; set_trace()
                    else:
                        print(f"⚠️ Invalid viewHistory args: {len(args)}")
                        
                else:
                    print("❌ No viewHistory() match")
                    
            except Exception as e:
                print(f"❌ Failed view button extraction: {e}")


    driver.quit()
    print(results)
    return results














# from ocr_utils import solve_captcha

# def run_selenium_scraper(case_type, case_no, case_year, case_status):
#     from selenium.common.exceptions import TimeoutException
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support.ui import Select, WebDriverWait
#     from selenium.webdriver.support import expected_conditions as EC
#     import time
#     from selenium.webdriver.chrome.options import Options
#     import re
#     import shlex

#     options = Options()
#     # options.add_argument('--headless')
#     # options.add_argument('--disable-gpu')
#     # options.add_argument('--no-sandbox')
#     # options.add_argument('--window-size=1920,1080')
#     driver = webdriver.Chrome(options=options)
#     driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
#     time.sleep(2)

#     Select(driver.find_element(By.NAME, "sess_state_code")).select_by_value("14")  # Haryana
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sess_state_code"))
#     time.sleep(1)

#     Select(driver.find_element(By.NAME, "sees_dist_code")).select_by_value("5")  # Faridabad
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sees_dist_code"))
#     time.sleep(1)

#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#     Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text("District Court, Faridabad")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.ID, "court_complex_code"))
#     time.sleep(1)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     # ✅ Switch to Case Number tab
#     driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
#     time.sleep(2)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     # Wait for the case type dropdown and ensure real options are loaded
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))

#     def case_type_options_loaded(driver):
#         dropdown = driver.find_element(By.NAME, "case_type")
#         options = dropdown.find_elements(By.TAG_NAME, "option")
#         return len(options) > 1  # >1 to ensure options are loaded (not just placeholder)

#     MAX_RETRIES = 3
#     for attempt in range(MAX_RETRIES):
#         try:
#             # Wait until case_type dropdown is present
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))

#             # Wait until case_type dropdown options are loaded (not just "Select Case Type")
#             def case_type_options_loaded(driver):
#                 select_elem = driver.find_element(By.NAME, "case_type")
#                 options = select_elem.find_elements(By.TAG_NAME, "option")
#                 return len(options) > 1  # real options loaded

#             WebDriverWait(driver, 15).until(case_type_options_loaded)

#             # Select your value now
#             Select(driver.find_element(By.NAME, "case_type")).select_by_value(case_type)
#             break  # ✅ done, exit the retry loop

#         except TimeoutException:
#             print(f"⚠️ Attempt {attempt+1}: Dropdown options didn't load. Retrying...")

#             # Try to click on the refresh link if it exists
#             try:
#                 refresh_link = driver.find_element(By.LINK_TEXT, "Click here to refresh again")
#                 refresh_link.click()
#                 time.sleep(3)
#             except:
#                 pass  # No refresh link found

#             # Start again from selecting state/district/court
#             try:
#                 Select(driver.find_element(By.NAME, "sess_state_code")).select_by_value("14")  # Haryana
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sess_state_code"))
#                 time.sleep(1)

#                 Select(driver.find_element(By.NAME, "sees_dist_code")).select_by_value("5")  # Faridabad
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sees_dist_code"))
#                 time.sleep(1)

#                 WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#                 Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text("District Court, Faridabad")
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.ID, "court_complex_code"))
#                 time.sleep(1)

#                 driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
#                 time.sleep(2)

#                 # close modal again
#                 try:
#                     driver.execute_script("closeModel({modal_id:'validateError'})")
#                 except:
#                     pass

#             except Exception as e:
#                 print(f"🔥 Error during retry state/district setup: {e}")
#                 break
#     else:
#         print("❌ Max retries reached. Exiting.")
#         driver.quit()
#         return []


#     # ✅ Fill case number and year
#     driver.find_element(By.NAME, "search_case_no").send_keys(case_no)
#     driver.find_element(By.NAME, "rgyear").send_keys(case_year)

#     # ✅ CAPTCH
#     for attempt in range(10):
#         print(f"🔁 Attempting CAPTCHA — Try #{attempt + 1}")

#         # Step 1: Wait and screenshot CAPTCHA image
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))
#         captcha_element = driver.find_element(By.ID, "captcha_image")
#         captcha_element.screenshot("captcha.png")

#         # Step 2: Solve CAPTCHA using Tesseract
#         captcha_text = solve_captcha("captcha.png")
#         print(f"🧠 Predicted CAPTCHA: {captcha_text}")

#         # Step 3: Fill the CAPTCHA input
#         input_box = driver.find_element(By.ID, "case_captcha_code")
#         input_box.clear()
#         input_box.send_keys(captcha_text)

#         # Step 4: Submit
#         driver.execute_script("submitCaseNo();")
#         time.sleep(3)

#         # Step 5: If results appear, break loop
#         try:
#             WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "dispTable")))
#             print("✅ CAPTCHA accepted — table loaded.")
#             break
#         except:
#             print("❌ CAPTCHA incorrect. Retrying...")

#             # Close error modal if it appears
#             try:
#                 driver.execute_script("closeModel({modal_id:'validateError'})")
#                 print("⚠️ Closed CAPTCHA error modal.")
#             except:
#                 pass

#             time.sleep(2)
#         else:
#             print("❌ Failed after 10 attempts.")
#             driver.quit()
#             return []
#         table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")
#         results = []
#         for row in table_rows:
#             cells = row.find_elements(By.TAG_NAME, "td")
#             if len(cells) == 4:
#                 sr_no = cells[0].text.strip()
#                 case_info = cells[1].text.strip()
#                 parties = cells[2].text.strip().replace("\n", " ")

#                 try:
#                     # ⏩ Extract onclick from <a>
#                     view_button = cells[3].find_element(By.TAG_NAME, "a")
#                     onclick_attr = view_button.get_attribute("onclick")
#                     print(f"👉 onclick = {onclick_attr}")

#                     match = re.search(r"viewHistory\((.*?)\)", onclick_attr)
#                     if match:
#                         raw_args = match.group(1)

#                         lexer = shlex.shlex(raw_args, posix=True)
#                         lexer.whitespace = ','
#                         lexer.whitespace_split = True
#                         lexer.quotes = "'"
#                         args = list(lexer)

#                         if len(args) == 9:
#                             # ✅ Call viewHistory
#                             driver.execute_script(f"viewHistory({','.join(repr(a) for a in args)})")

#                             # ⏳ Wait for modal / case history details to load
#                             try:
#                                 WebDriverWait(driver, 10).until(
#                                     EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'modal') and contains(@style, 'display: block')]"))
#                                 )
#                                 print("✅ Modal opened.")
#                             except:
#                                 print("❌ Modal did not appear.")
                            
#                             # 📅 Filing Date extraction from modal table
#                             try:
#                                 # Wait until modal table appears
#                                 WebDriverWait(driver, 5).until(
#                                     EC.presence_of_element_located((By.CSS_SELECTOR, ".case_details_table"))
#                                 )

#                                 # Locate Filing Date cell in modal
#                                 filing_date_elem = driver.find_element(
#                                     By.XPATH,
#                                     "//div[contains(@class, 'modal') and contains(@style, 'display: block')]"
#                                     "//table[contains(@class, 'case_details_table')]"
#                                     "//label[contains(text(), 'Filing Date')]/parent::td/following-sibling::td"
#                                 )
#                                 filing_date = filing_date_elem.text.strip()
#                                 print(f"✅ Filing Date found: {filing_date}")

#                             except Exception as e:
#                                 print(f"❌ Couldn't get Filing Date: {e}")
#                                 filing_date = "N/A"

#                             # 📅 Next Hearing Date (optional for now)
#                             next_hearing = "N/A"

#                             # 📄 Most Recent PDF (optional for now)
#                             recent_pdf = "N/A"

#                         else:
#                             print(f"⚠️ Invalid viewHistory args: {len(args)}")
#                             filing_date = next_hearing = recent_pdf = "N/A"
#                     else:
#                         print("❌ No viewHistory() match")
#                         filing_date = next_hearing = recent_pdf = "N/A"

#                 except Exception as e:
#                     print(f"❌ Failed view button extraction: {e}")
#                     filing_date = next_hearing = recent_pdf = "N/A"


#                 results.append({
#                     "sr_no": sr_no,
#                     "case_info": case_info,
#                     "parties": parties,
#                     "filing_date": filing_date,
#                     "next_hearing_date": next_hearing,
#                     "recent_pdf": recent_pdf,
#                 })

#             elif len(cells) == 1:
#                 results.append({
#                     "court_name": cells[0].text.strip()
#                 })
#         driver.quit()
#         return results































# def run_selenium_scraper(case_type, case_no, case_year, case_status):
#     from selenium.common.exceptions import TimeoutException
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support.ui import Select, WebDriverWait
#     from selenium.webdriver.support import expected_conditions as EC
#     import time
#     from selenium.webdriver.chrome.options import Options
#     import shlex
#     import re

#     options = Options()
#     # options.add_argument('--headless')
#     # options.add_argument('--disable-gpu')
#     # options.add_argument('--no-sandbox')
#     # options.add_argument('--window-size=1920,1080')
#     driver = webdriver.Chrome(options=options)
#     driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
#     time.sleep(2)

#     Select(driver.find_element(By.NAME, "sess_state_code")).select_by_value("14")  # Haryana
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sess_state_code"))
#     time.sleep(1)

#     Select(driver.find_element(By.NAME, "sees_dist_code")).select_by_value("5")  # Faridabad
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sees_dist_code"))
#     time.sleep(1)

#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#     Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text("District Court, Faridabad")
#     driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.ID, "court_complex_code"))
#     time.sleep(1)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     # ✅ Switch to Case Number tab
#     driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
#     time.sleep(2)

#     try:
#         driver.execute_script("closeModel({modal_id:'validateError'})")
#     except:
#         pass

#     # Wait for the case type dropdown and ensure real options are loaded
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))

#     def case_type_options_loaded(driver):
#         dropdown = driver.find_element(By.NAME, "case_type")
#         options = dropdown.find_elements(By.TAG_NAME, "option")
#         return len(options) > 1  # >1 to ensure options are loaded (not just placeholder)

#     MAX_RETRIES = 3
#     for attempt in range(MAX_RETRIES):
#         try:
#             # Wait until case_type dropdown is present
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "case_type")))

#             # Wait until case_type dropdown options are loaded (not just "Select Case Type")
#             def case_type_options_loaded(driver):
#                 select_elem = driver.find_element(By.NAME, "case_type")
#                 options = select_elem.find_elements(By.TAG_NAME, "option")
#                 return len(options) > 1  # real options loaded

#             WebDriverWait(driver, 15).until(case_type_options_loaded)

#             # Select your value now
#             Select(driver.find_element(By.NAME, "case_type")).select_by_value(case_type)
#             break  # ✅ done, exit the retry loop

#         except TimeoutException:
#             print(f"⚠️ Attempt {attempt+1}: Dropdown options didn't load. Retrying...")

#             # Try to click on the refresh link if it exists
#             try:
#                 refresh_link = driver.find_element(By.LINK_TEXT, "Click here to refresh again")
#                 refresh_link.click()
#                 time.sleep(3)
#             except:
#                 pass  # No refresh link found

#             # Start again from selecting state/district/court
#             try:
#                 Select(driver.find_element(By.NAME, "sess_state_code")).select_by_value("14")  # Haryana
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sess_state_code"))
#                 time.sleep(1)

#                 Select(driver.find_element(By.NAME, "sees_dist_code")).select_by_value("5")  # Faridabad
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sees_dist_code"))
#                 time.sleep(1)

#                 WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
#                 Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text("District Court, Faridabad")
#                 driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.ID, "court_complex_code"))
#                 time.sleep(1)

#                 driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
#                 time.sleep(2)

#                 # close modal again
#                 try:
#                     driver.execute_script("closeModel({modal_id:'validateError'})")
#                 except:
#                     pass

#             except Exception as e:
#                 print(f"🔥 Error during retry state/district setup: {e}")
#                 break
#     else:
#         print("❌ Max retries reached. Exiting.")
#         driver.quit()
#         return []


#     # ✅ Fill case number and year
#     driver.find_element(By.NAME, "search_case_no").send_keys(case_no)
#     driver.find_element(By.NAME, "rgyear").send_keys(case_year)

#     # ✅ CAPTCH
#     for attempt in range(10):
#         print(f"🔁 Attempting CAPTCHA — Try #{attempt + 1}")

#         # Step 1: Wait and screenshot CAPTCHA image
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captcha_image")))
#         captcha_element = driver.find_element(By.ID, "captcha_image")
#         captcha_element.screenshot("captcha.png")

#         # Step 2: Solve CAPTCHA using Tesseract
#         captcha_text = solve_captcha("captcha.png")
#         print(f"🧠 Predicted CAPTCHA: {captcha_text}")

#         # Step 3: Fill the CAPTCHA input
#         input_box = driver.find_element(By.ID, "case_captcha_code")
#         input_box.clear()
#         input_box.send_keys(captcha_text)

#         # Step 4: Submit
#         driver.execute_script("submitCaseNo();")
#         time.sleep(3)

#         # Step 5: If results appear, break loop
#         try:
#             WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "dispTable")))
#             print("✅ CAPTCHA accepted — table loaded.")
#             break
#         except:
#             print("❌ CAPTCHA incorrect. Retrying...")

#             # Close error modal if it appears
#             try:
#                 driver.execute_script("closeModel({modal_id:'validateError'})")
#                 print("⚠️ Closed CAPTCHA error modal.")
#             except:
#                 pass

#             time.sleep(2)
#     else:
#         print("❌ Failed after 10 attempts.")
#         driver.quit()
#         return []
#     table_rows = driver.find_elements(By.CSS_SELECTOR, "#dispTable tbody tr")
#     results = []
#     for row in table_rows:
#         cells = row.find_elements(By.TAG_NAME, "td")
#         if len(cells) == 4:
#             case_info = cells[1].text.strip()
#             parties = cells[2].text.strip().replace("\n", " ")

#             try:
#                 # 🔍 Extract viewHistory arguments from the onclick attribute
#                 view_button = cells[3].find_element(By.TAG_NAME, "a")
#                 onclick_attr = view_button.get_attribute("onclick")
#                 print(f"👉 onclick = {onclick_attr}")

#                 match = re.search(r"viewHistory\((.*?)\)", onclick_attr)
#                 if match:
#                     raw_args = match.group(1)

#                     lexer = shlex.shlex(raw_args, posix=True)
#                     lexer.whitespace = ','  # Set comma as argument separator
#                     lexer.whitespace_split = True
#                     lexer.quotes = "'"
#                     args = list(lexer)

#                     if len(args) != 9:
#                         print(f"⚠️ View button had {len(args)} args instead of 9 — skipping.")
#                         continue

#                     # ✅ Call viewHistory with parsed arguments
#                     driver.execute_script(f"viewHistory({','.join(repr(a) for a in args)})")
#                     time.sleep(3)

#                     # ✅ Wait for filing date to ensure detail page loaded
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.XPATH, "//label[text()='Filing Date']"))
#                     )

#                     # 📅 Filing Date
#                     try:
#                         filing_label = driver.find_element(By.XPATH, "//label[text()='Filing Date']")
#                         filing_date = filing_label.find_element(By.XPATH, "./../../td[2]").text.strip()
#                     except:
#                         filing_date = "N/A"

#                     # 📅 Next Hearing Date
#                     try:
#                         next_hearing = driver.find_element(
#                             By.XPATH, "//label[contains(text(), 'Next Hearing Date')]/../following-sibling::td/strong"
#                         ).text.strip()
#                     except:
#                         next_hearing = "N/A"

#                     # 📎 Most Recent PDF Link
#                     try:
#                         WebDriverWait(driver, 5).until(
#                             EC.presence_of_element_located((By.ID, "order_judgement_table"))
#                         )
#                         order_table = driver.find_element(By.ID, "order_judgement_table")
#                         pdf_links = order_table.find_elements(By.TAG_NAME, "a")
#                         recent_pdf = pdf_links[-1].get_attribute("href") if pdf_links else "N/A"
#                     except:
#                         recent_pdf = "N/A"

#                     # ✅ Store results
#                     results.append({
#                         "case_info": case_info,
#                         "parties": parties,
#                         "filing_date": filing_date,
#                         "next_hearing_date": next_hearing,
#                         "recent_pdf": recent_pdf,
#                     })

#                 else:
#                     print("⚠️ No match found for viewHistory() — skipping this row.")
#                     continue

#             except Exception as e:
#                 print(f"❌ Error extracting view details: {e}")
#                 results.append({
#                     "case_info": case_info,
#                     "parties": parties,
#                     "filing_date": "N/A",
#                     "next_hearing_date": "N/A",
#                     "recent_pdf": "N/A",
#                 })

#         elif len(cells) == 1:
#             results.append({
#                 "court_name": cells[0].text.strip()
#             })










    # for row in table_rows:
    #     cells = row.find_elements(By.TAG_NAME, "td")
    #     if len(cells) == 4:
    #         case_info = cells[1].text.strip()
    #         parties = cells[2].text.strip().replace("\n", " ")

    #         try:
    #             # Get onclick attribute from View button
    #             view_button = cells[3].find_element(By.TAG_NAME, "a")
    #             onclick_attr = view_button.get_attribute("onclick")
    #             print(f"👉 onclick = {onclick_attr}")

    #             # 🧠 Extract and split arguments using shlex
    #             raw_args_string = onclick_attr.strip()

    #             if raw_args_string.startswith("viewHistory(") and raw_args_string.endswith(")"):
    #                 raw_args = raw_args_string[len("viewHistory("):-1]  # remove outer function call
    #                 args = shlex.split(raw_args)  # handles quoted strings properly
    #             else:
    #                 print("❌ viewHistory format invalid.")
    #                 args = []

    #             # ✅ Safely execute if correct number of arguments
    #             if len(args) == 9:
    #                 driver.execute_script(
    #                     f"viewHistory('{args[0]}','{args[1]}',{args[2]},'{args[3]}','{args[4]}',{args[5]},{args[6]},{args[7]},'{args[8]}')"
    #                 )
    #                 print("✅ viewHistory called")
    #             else:
    #                 print(f"⚠️ Unexpected argument count in viewHistory: {len(args)}")
    #                 raise Exception("viewHistory args mismatch")

    #             # ✅ Wait for the case details to load
    #             WebDriverWait(driver, 10).until(
    #                 EC.presence_of_element_located((By.XPATH, "//label[text()='Filing Date']"))
    #             )
    #             time.sleep(1)

    #             # Filing Date
    #             try:
    #                 filing_label = driver.find_element(By.XPATH, "//label[text()='Filing Date']")
    #                 filing_date = filing_label.find_element(By.XPATH, "./../../td[2]").text.strip()
    #             except:
    #                 filing_date = "N/A"

    #             # Next Hearing Date
    #             try:
    #                 next_hearing = driver.find_element(
    #                     By.XPATH, "//label[contains(text(), 'Next Hearing Date')]/../following-sibling::td/strong"
    #                 ).text.strip()
    #             except:
    #                 next_hearing = "N/A"

    #             # PDF link
    #             try:
    #                 WebDriverWait(driver, 5).until(
    #                     EC.presence_of_element_located((By.ID, "order_judgement_table"))
    #                 )
    #                 order_table = driver.find_element(By.ID, "order_judgement_table")
    #                 pdf_links = order_table.find_elements(By.TAG_NAME, "a")
    #                 print(f"📄 PDF Links found: {len(pdf_links)}")

    #                 if pdf_links:
    #                     recent_pdf = pdf_links[-1].get_attribute("href")
    #                 else:
    #                     recent_pdf = "N/A"
    #             except:
    #                 recent_pdf = "N/A"

    #             # ✅ Append final result
    #             results.append({
    #                 "case_info": case_info,
    #                 "parties": parties,
    #                 "filing_date": filing_date,
    #                 "next_hearing_date": next_hearing,
    #                 "recent_pdf": recent_pdf,
    #             })

    #         except Exception as e:
    #             print(f"❌ Error extracting view details: {e}")
    #             results.append({
    #                 "case_info": case_info,
    #                 "parties": parties,
    #                 "filing_date": "N/A",
    #                 "next_hearing_date": "N/A",
    #                 "recent_pdf": "N/A",
    #             })

    #     elif len(cells) == 1:
    #         results.append({
    #             "court_name": cells[0].text.strip()
    #         })
