import os, sys, csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# these Polycom web consoles are trash. Xpath is often the only way :(

def login(driver):
	driver.find_element_by_name("password").send_keys("xxxxxxxxxxxx")
	driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[6]/td[1]/input").click()
	driver.find_element_by_id("content")

def extractGeneralInfo(driver):
	model = driver.find_element_by_id("phoneModelInformationTd").text
	part_num = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[3]/td[2]').text
	mac_addr = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[4]/td[2]').text
	return [model,part_num,mac_addr]

def extract8500Info(driver):
	bt_mac_addr = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[5]/td[2]').text
	ip_addr = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[6]/td[2]').text
	firmware_version = driver.find_element_by_id('UCS_software_version').text
	update_signature = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[8]/td[2]').text
	sys_name = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[9]/td[2]').text
	return [bt_mac_addr, ip_addr, firmware_version, update_signature, sys_name]

def extract8800Info(driver):
	bt_mac_addr = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[6]/td[2]').text
	ip_addr = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[7]/td[2]').text
	firmware_version = driver.find_element_by_id('UCS_software_version').text
	update_signature = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[9]/td[2]').text
	sys_name = driver.find_element_by_xpath('//*[@id="home"]/div[1]/table/tbody/tr[10]/td[2]').text
	return [bt_mac_addr, ip_addr, firmware_version, update_signature, sys_name]

def extractServerInfo(driver):
	driver.find_element_by_xpath('/html/body/div[2]/ul[2]/li[4]/a/span').click()
	driver.find_element_by_xpath('/html/body/div[2]/ul[2]/li[4]/ul/li[15]/a/span').click()

	server_type = Select(driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[6]/div[2]/form/div[1]/div/table/tbody/tr[1]/td[2]/select')).first_selected_option.get_attribute("value")
	server_addr = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[6]/div[2]/form/div[1]/div/table/tbody/tr[2]/td[2]/input').get_attribute("value")
	boot_server = Select(driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[6]/div[2]/form/div[2]/div/table/tbody/tr[1]/td[2]/select')).first_selected_option.get_attribute("value")
	return [server_type, server_addr, boot_server]

def checkTimeZone(driver):
	driver.find_element_by_xpath('//*[@id="topMenuItem2"]/a/span').click()
	time_zone_id = driver.find_element_by_id("olsonTimezoneIDCombo1").get_attribute('value')
	return [time_zone_id]

#-------------------------------------------------------------------------------------------------------------

# csv as "room name, ip of room,\n"
with open(os.path.join(sys.path[0], 'input06-02.csv'), newline='') as csvfile: #UPDATE THIS INPUT FILE BEFORE RUNNING
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	
	out = open(os.path.join(sys.path[0], 'pollResults.csv'), 'w')
	print('Room Name,Targeted URL,Phone Model,Part Number,MAC Address,Bluetooth MAC Address,IP Address,UC Software Version,Updater Signature,System Name,Server Type(3=HTTPS),Server Address,Boot Server(2=Static),Time Zone', file=out)

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	caps = webdriver.DesiredCapabilities.CHROME.copy()
	caps['acceptInsecureCerts'] = True
	driver = webdriver.Chrome('C:/Users/crobertson/Downloads/chromedriver_win32/chromedriver.exe', chrome_options=options, desired_capabilities=caps)
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
			general = extractGeneralInfo(driver)

			if general[0] == 'Trio 8500':
				details = extract8500Info(driver)
			else:
				details = extract8800Info(driver)
			
			server_info = extractServerInfo(driver)
			time_info = checkTimeZone(driver)

			print(','.join([room, url] + general + details + server_info + time_info))
			print(','.join([room, url] + general + details + server_info + time_info), file=out)
		except NoSuchElementException as ex:
			print('%s, %s, element not found, %s' % (room, ip, str(ex).split('\n')[0]), file=out)
			continue
		except Exception as ex: 
			print('%s, %s, Unknown error, %s' % (room, ip, str(ex)), file=out)
			continue

	driver.quit()
	out.close()