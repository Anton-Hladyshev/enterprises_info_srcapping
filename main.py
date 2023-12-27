from fastapi import FastAPI, Query
from seleniumbase import DriverContext
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
import datetime

app = FastAPI(title='Service_Anton')


@app.get("/info/{edrpu_code}")
def get_code(edrpu_code: str, source=Query(description='opendatabot or youcontrol', pattern='^opendatabot|youcontrol$')):
    return get_enterprise_info(edrpu_code, source)


def get_enterprise_info(code, source):
    with DriverContext(uc=True) as driver:
        if source == 'youcontrol':
            data_from_youcontrol = get_info_youcontrol(code, driver)
            return data_from_youcontrol

        elif source == 'opendatabot':
            data_from_opendatabot = get_info_opendatabot(code, driver)
            return data_from_opendatabot


def get_info_youcontrol(code, driver):
    try:
        driver.get(f"https://youcontrol.com.ua/catalog/company_details/{code}/")

        full_name = driver.find_element(By.CSS_SELECTOR, "div.seo-table :nth-child(1) > div.seo-table-col-2 > span.copy-file-field").text
        short_name = driver.find_element(By.CSS_SELECTOR, "div.seo-table :nth-child(2) > div.seo-table-col-2 > span.copy-file-field").text
        objects_current_state = driver.find_element(By.XPATH, '//div[contains(text(), " Статус юридичної особи")]/../div[2]/span').text
        code_of_enterprise = str(code)
        date_of_creation = driver.find_element(By.XPATH, '//div[contains(text(), "Дата реєстрації")]/../div[2]/div').text
        age_of_enterprise = driver.find_element(By.CSS_SELECTOR, ".text-grey").text

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

def get_info_opendatabot(code, driver):
    try:
        driver.get(f'https://opendatabot.ua/c/{code}?from=search')

        full_name = driver.find_element(By.CSS_SELECTOR, "div.bg-body > dl.row :nth-child(2) > dd.mb-1").text
        short_name = driver.find_element(By.TAG_NAME, 'h2').text
        objects_state = driver.find_element(By.XPATH, '//dt[contains(text(), "Стан")]/../dd').text
        date_of_creation = driver.find_element(By.CSS_SELECTOR, "div.col-sm-4 > dd.mb-1").text
        # converting the date of creation into datetime.date object from str
        date_to_lst = date_of_creation.split('.')
        date_of_creation_in_datetime = datetime.date(day=int(date_to_lst[0]), month=int(date_to_lst[1]), year=int(date_to_lst[2]))
        # difference between today and the date of creation
        age_of_company = f'{relativedelta(datetime.date.today(), date_of_creation_in_datetime).years} років {relativedelta(datetime.date.today(), date_of_creation_in_datetime).months} місяців'

        dict_res = {
            'full_name': full_name,
            'short_name': short_name,
            'objects_state': objects_state,
            'code_of_enterpise': code,
            'date_of_creation': date_of_creation,
            'age_of_company': age_of_company
        }

        return dict_res

    except Exception as ex:
        return ex
