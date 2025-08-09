from ocr_utils import solve_captcha
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from selenium.webdriver.chrome.options import Options
import re
import shlex


def print_progress(progress, total, length=30):
    percent = progress / total
    filled_length = int(length * percent)
    bar = "█" * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\rProgress: |{bar}| {percent:.0%}")
    sys.stdout.flush()


total_steps = 10

def run_selenium_scraper(case_type, case_no, case_year, case_status):

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    BASE = "https://services.ecourts.gov.in/ecourtindia_v6/"
    driver.get(BASE)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
    time.sleep(2)

    print_progress(1, total_steps)

    Select(driver.find_element(By.NAME, "sess_state_code")).select_by_value("14")  # Haryana
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sess_state_code"))
    time.sleep(1)

    print_progress(2, total_steps)

    Select(driver.find_element(By.NAME, "sees_dist_code")).select_by_value("5")  # Faridabad
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.NAME, "sees_dist_code"))
    time.sleep(1)

    print_progress(3, total_steps)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "court_complex_code")))
    Select(driver.find_element(By.ID, "court_complex_code")).select_by_visible_text("District Court, Faridabad")
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", driver.find_element(By.ID, "court_complex_code"))
    time.sleep(1)

    print_progress(4, total_steps)

    try:
        driver.execute_script("closeModel({modal_id:'validateError'})")
    except:
        pass

    # ✅ Switch to Case Number tab
    driver.execute_script("document.getElementById('casenumber-tabMenu').click();")
    time.sleep(2)

    print_progress(5, total_steps)

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

    print_progress(6, total_steps)

    # ✅ Fill case number and year
    driver.find_element(By.NAME, "search_case_no").send_keys(case_no)
    driver.find_element(By.NAME, "rgyear").send_keys(case_year)

    print_progress(7, total_steps)

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

    print_progress(8, total_steps)

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

                match = re.search(r"viewHistory\((.*?)\)", onclick_attr)
                if match:
                    raw_args = match.group(1)

                    lexer = shlex.shlex(raw_args, posix=True)
                    lexer.whitespace = ','
                    lexer.whitespace_split = True
                    lexer.quotes = "'"
                    args = list(lexer)
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

                        if url and not url.startswith("http"):
                            url = BASE + url

                        results['latest_judgement_pdf_link'] = url
                    else:
                        print(f"⚠️ Invalid viewHistory args: {len(args)}")
                        
                else:
                    print("❌ No viewHistory() match")
                    
            except Exception as e:
                print(f"❌ Failed view button extraction: {e}")
    print_progress(9, total_steps)
    driver.quit()
    print_progress(10, total_steps)
    return results
