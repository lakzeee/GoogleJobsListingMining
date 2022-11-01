from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import src.constants as const

class Driver(webdriver.Chrome):
	def __init__(self, teardown = False):
		self.teardown = teardown
		super(Driver, self).__init__()
		self.implicitly_wait(3)

	def __exit__(self, *args):
		if self.teardown:
			time.sleep(5)
			self.quit()
	
	def land_first_page(self):
		self.get(const.BASE_URL)