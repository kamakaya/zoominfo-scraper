from playwright.sync_api import Playwright, sync_playwright
import pandas as pd

USERNAME = 'brd-customer-hl_7151f78f-zone-scraping_browser1'
PASSWORD = '8t6f75tr72zc'
# AUTH = 'brd-customer-hl_7151f78f-zone-scraping_browser1:8t6f75tr72zc'  
SBR_WS_CDP = f'wss://{USERNAME}:{PASSWORD}@brd.superproxy.io:9222' 

def launch_browser(playwright: Playwright):
    # browser = playwright.chromium.launch(headless=False)
    browser = playwright.chromium.connect_over_cdp(SBR_WS_CDP)  
    context = browser.new_context()
    page = context.new_page()

    return browser, context, page

def get_company_data(page, company_name: str):
    page.goto(f"https://www.google.com/search?q={company_name}+zoominfo")
    
    try:
        page.wait_for_load_state('load')
        page.wait_for_selector('h3')
        page.click('h3')
    except:
        return {
            'company_name': company_name,
            'headquarters': None,
            'website': None,
            'revenue': None,
            'industries': None
        }

    page.wait_for_load_state('load')

    try:
        headquarters = page.locator('xpath=//h3[text()="Headquarters"]/following-sibling::span').text_content()
    except:
        headquarters = None
    try:
        website = page.locator('xpath=//h3[text()="Website"]/following-sibling::a').text_content()
    except:
        website = None
    try:
        revenue = page.locator('xpath=//h3[text()="Revenue"]/following-sibling::span').text_content()
    except:
        revenue = None
    try:
        industry_elements = page.locator('xpath=//h3[text()="Industry"]/following-sibling::span/zi-directories-chips/a')
        industries = [element.text_content() for element in industry_elements.element_handles()]
    except:
        industries = None

    print(f"Company Name: {company_name}")
    print(f"Headquarters: {headquarters}")
    print(f"Website: {website}")
    print(f"Revenue: {revenue}")
    print(f"Industries: {'; '.join(industries) if industries else 'N/A'}\n")

    return {
        'company_name': company_name,
        'headquarters': headquarters,
        'website': website,
        'revenue': revenue,
        'industries': '; '.join(industries) if industries else 'N/A'
    }

def read_company_names(file_path: str):
    with open(file_path, 'r') as file:
        company_names = file.read().splitlines()
    return company_names

def save_to_csv(data, output_file: str, mode='a'):
    df = pd.DataFrame([data])
    df.to_csv(output_file, mode=mode, index=False, header=not pd.io.common.file_exists(output_file))

with sync_playwright() as playwright:
    browser, context, page = launch_browser(playwright)

    company_names = read_company_names('company_names.txt')
    output_file = 'company_data.csv'

    for company in company_names:
        try:
            data = get_company_data(page, company)
            save_to_csv(data, output_file)
        except:
            print(f"Unable to retrieve data for: {company}")

    context.close()
    browser.close()
