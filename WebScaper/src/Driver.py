from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import src.constants as const
from src.json_tool import dicts_to_json

class Driver(webdriver.Chrome):
    def __init__(self, teardown = False):
        self.teardown = teardown
        super(Driver, self).__init__()
        self.implicitly_wait(2)

    def __exit__(self, *args):
        if self.teardown:
            time.sleep(3)
            self.quit()

    def check_exists_by_x_path(self, x_path):
        try:
            self.find_element(By.XPATH, x_path)
        except NoSuchElementException:
            return False
    
    def check_exists_by_class_name(self, class_name):
        try:
            self.find_element(By.CLASS_NAME, class_name)
        except NoSuchElementException:
            return False
        return True

    def get_pages_count(self):
        count = self.find_element(By.CLASS_NAME, "gc-sidebar__pagination--page").get_attribute('innerHTML').replace("Page 1 of ", "").strip()
        return int(count)
    
    def get_all(self):

        for role in const.ENGINNERING_ROLES:
            role_url = const.BASE_URL+role
            self.get(role_url)
            page_count = self.get_pages_count()
            for i in range(page_count):
                role_url_page = role_url+f"&page={i+1}"
                self.get(role_url_page)
                links = self.get_all_links()
                filename = f"jobs_{role}_{i+1}"
                self.save_contents(links, role, filename)
                print(f"Save jobs_page_{filename}")

    def get_all_links(self):
        link_elements = self.find_elements(By.CLASS_NAME, "gc-card")

        links = []
        for link_element in link_elements:
            links.append(link_element.get_attribute('href'))
        return links

    def save_contents(self, links, role, filename):
        contents = []
        for link in links:
            self.get(link)
            time.sleep(1)
            entry = {
                    "role":"",
                    "title":"",
                    "datePosted":"",
                    "inOfficeLocation":"",
                    "isRemoteEligible":"",
                    "minQua":[],
                    "preferQua":[],
                    "responsibilities":[],
                    "jobDescription":"",
                    "link":""
            }
            entry["role"] = role
            entry["link"] = link
            entry["title"] = self.find_element(By.CSS_SELECTOR, 'h1[itemprop="title"]').get_attribute('innerHTML').strip()
            print(f'title is {entry["title"]}')
            entry["datePosted"] = self.find_element(By.XPATH, '//span[@itemprop="datePosted"]').get_attribute('innerHTML').strip()
            print(f'date is {entry["datePosted"]}')


            if self.check_exists_by_class_name(class_name="gc-job-detail__instruction"):
                if self.check_exists_by_x_path(x_path="//b[contains(text(), 'In-office')]"):
                    try:
                        entry["inOfficeLocation"] = self.find_element(By.XPATH, "//b[contains(text(), 'In-office')]").get_attribute('innerHTML').replace("In-office locations:", "").strip()
                        entry["isRemoteEligible"] = 1
                    except:
                        entry["inOfficeLocation"] = "null"
                        entry["isRemoteEligible"] = 1
                        continue
                else:
                    try:
                        entry["inOfficeLocation"] = self.find_element(By.XPATH, '//span[contains(text(),"working location")]/b').get_attribute('innerHTML').strip()
                        entry["isRemoteEligible"] = 0
                    except:
                        entry["inOfficeLocation"] = "null"
                        entry["isRemoteEligible"] = 0
                        continue
            else:
                address = ""
                try:
                    address += self.find_element(By.XPATH, '//*[contains(@class, "gc-job-detail--loaded")]//span[@itemprop="addressLocality"]').get_attribute('innerHTML').strip()
                    address += self.find_element(By.XPATH, '//*[contains(@class, "gc-job-detail--loaded")]//span[@itemprop="addressRegion"]').get_attribute('innerHTML').strip()
                    address += self.find_element(By.XPATH, '//*[contains(@class, "gc-job-detail--loaded")]//span[@itemprop="addressCountry"]').get_attribute('innerHTML').strip()
                except:
                    address += "null"
                    continue
                entry["inOfficeLocation"] = address
                entry["isRemoteEligible"] = 0
            
            try:
                min_quas = self.find_elements(By.XPATH, '//div[@itemprop="qualifications"]//child::ul[1]/li')
                for min_qua in min_quas:
                    entry["minQua"].append(min_qua.get_attribute('innerHTML').replace("<br>", "").strip())
            except:
                entry["minQua"] = "null"
                continue
            
            try:
                prefer_quas = self.find_elements(By.XPATH, '//div[@itemprop="qualifications"]//child::ul[2]/li')
                for prefer_qua in prefer_quas:
                    entry["preferQua"].append(prefer_qua.get_attribute('innerHTML').replace("<br>", "").strip())
            except:
                entry["preferQua"] = "null"
                continue

            try:
                resps = self.find_elements(By.XPATH, '//div[@itemprop="responsibilities"]//child::ul/li')
                for resp in resps:
                    entry["responsibilities"].append(resp.get_attribute('innerHTML').replace("<br>", "").replace("</span>","").replace("<span>", "").strip())
            except:
                entry["responsibilities"] = "null"
                continue
            
            try:
                jds = self.find_elements(By.XPATH, '//div[@itemprop="description"]//child::p')
                for jd in jds:
                    entry["jobDescription"] += jd.get_attribute('innerHTML').replace("<br>", "").strip()
            except:
                entry["jobDescription"] = "null"
                continue

            contents.append(entry)

        dicts_to_json(contents, filename)
