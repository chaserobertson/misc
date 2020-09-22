import os, sys, csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException

# these Polycom web consoles are trash. Xpath is often the only way :(

def login(driver):
	driver.find_element_by_name("password").send_keys("xxxxxxxxxxx")
	driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[6]/td[1]/input").click()
	driver.find_element_by_id("content")

def restore(driver):
	try:
		driver.find_element_by_xpath("/html/body/div[2]/ul[2]/li[6]/a/span").click()
		driver.find_element_by_xpath("/html/body/div[2]/ul[2]/li[6]/ul/li[2]/a/span").click()
		driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[6]/div[2]/div[2]/p/strong/span").click()
		driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[6]/div/div[2]/div/form/table/tbody/tr[1]/td[2]/div/span[1]/input").send_keys(config)
		driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[6]/div/div[2]/div/form/table/tbody/tr[2]/td[2]/input").click()
		WebDriverWait(driver,10).until(cond.visibility_of(driver.find_element_by_xpath("/html/body/div[8]/div[3]/button")))
		return "Success"
	
	except (NoAlertPresentException, TimeoutException) as py_ex:
		print (py_ex)
		print (py_ex.args)
		return "Failed"

#-------------------------------------------------------------------------------------------------------------

# csv as "room name, ip of room,\n"
with open(os.path.join(sys.path[0], 'test-IP.csv'), newline='') as csvfile: #UPDATE THIS INPUT FILE BEFORE RUNNING
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

	config_filepath = os.path.join(sys.path[0], 'targetConfig.pbu')
	print('Config file to restore: %s' % config_filepath)
	out_filepath = os.path.join(sys.path[0], 'restoreConfigResults.csv')
	out = open(out_filepath, 'w')
	print('Room Name,Targeted URL, Restore Status', file=out)

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	caps = webdriver.DesiredCapabilities.CHROME.copy()
	caps['acceptInsecureCerts'] = True
	driver = webdriver.Chrome('C:/Users/crobertson/Downloads/chromedriver_win32/chromedriver.exe', options=options, desired_capabilities=caps)
	driver.implicitly_wait(10)
	driver.set_page_load_timeout(10)

	for row in spamreader:
		room = row[0]
		ip = row[1]
		url = 'https://' + ip

		if len(room) < 1 or len(ip) < 1:	#skip lines missing data
			continue

		try:	
			driver.get(url)	#try loading login page
			login(driver)	#try correct password
		except TimeoutException as ex:
			print('%s, %s, Error: Timeout' % (room, ip), file=out)
			continue
		except NoSuchElementException as ex:
			print('%s, %s, Login failed,' % (room, ip), file=out)
			continue
		try:
			restoreStatus = restore(driver)
			print(','.join([room, url, restoreStatus]))
			print(','.join([room, url, restoreStatus]), file=out)
		except NoSuchElementException as ex:
			print('%s, %s, element not found, %s' % (room, ip, str(ex).split('\n')[0]), file=out)
			continue
		except Exception as ex: 
			print('%s, %s, Unknown error, %s' % (room, ip, str(ex)), file=out)
			continue

	driver.quit()
	print("Output sent to: %s" % out_filepath)
	out.close()