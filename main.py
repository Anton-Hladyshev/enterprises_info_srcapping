from fastapi import FastAPI
from seleniumbase import DriverContext
from selenium.webdriver.common.by import By

app = FastAPI(title='Service_Anton')


@app.get("/info/{edrpu_code}")
def get_code(edrpu_code: int):
    return main(edrpu_code)


def main(code):
    with DriverContext(uc=True) as driver:
        data_from_youcontrol = get_info_youcontrol(code, driver)
        return data_from_youcontrol


def get_info_youcontrol(code, driver):
    try:
        driver.get(f"https://youcontrol.com.ua/catalog/company_details/{code}/")

        full_name = driver.find_element(By.CSS_SELECTOR, "div.seo-table :nth-child(1) > div.seo-table-col-2 > span.copy-file-field").text 
        short_name = driver.find_element(By.CSS_SELECTOR, "div.seo-table :nth-child(2) > div.seo-table-col-2 > span.copy-file-field").text
        objects_current_state = driver.find_element(By.CSS_SELECTOR, "div.seo-table :nth-child(4) > div.seo-table-col-2 > span.copy-file-field").text
        code_of_enterprise = str(code)
        date_of_creation = driver.find_element(By.CSS_SELECTOR, "div.seo-table :nth-child(6) > div.seo-table-col-2 > div.copy-file-field").text
        age_of_enterprise = driver.find_element(By.CSS_SELECTOR, "div.seo-table :nth-child(6) > div.seo-table-col-2 > div.copy-file-field > span.text-grey").text
        
        dict_res = {
            'full_name': full_name,
            'short_name': short_name,
            'objects_current_state': objects_current_state,
            'code_of_enterprise': code_of_enterprise,
            'date_of_creation': date_of_creation.split(')')[0].split('(')[0],
            'age_of_enterprise': age_of_enterprise.split(')')[0].split('(')[1]
        }

        return dict_res
    
    except Exception as ex:
        return ex
