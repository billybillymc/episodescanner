from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
import time
import re
import json
import os
chrome_options = Options()
chromedriver_autoinstaller.install()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']
yt_code = input('YouTube code?      ') ## Add the YT code, like SC7D01nDpcPH0v9jgEFxCykg
show_name = input('Urlname?     ') ## Add the show name, like its-always-sunny-in-philadelphia
last = int(input('Number of seasons?       ')) ## number of seasons, like 15
for i in range(1,last+1):
    dates=[]
    titles=[]
    runtimes=[]
    driver.get(f"https://www.youtube.com/show/{yt_code}?season={i}")
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(3)
    length=len(driver.find_elements_by_xpath("//a[@id='video-title']"))
    #getting_title
    for count in driver.find_elements_by_xpath("//a[@id='video-title']"):
        titles.append(count.text)
    for count in driver.find_elements_by_xpath("//span[@id='text']"):
        runtimes.append(count.text)
    while '' in runtimes:
        runtimes=[]
        driver.refresh()
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(3)
        for count in driver.find_elements_by_xpath("//span[@id='text']"):
            runtimes.append(count.text)
    try:
        for count in driver.find_elements_by_xpath("//*[@class='style-scope ytd-channel-name']"):
            for t in months:
                if re.findall(f"{t} \d+, \d+",count.text) != []:
                    new_date=re.findall(f"{t} \d+, \d+",count.text)
                    dates.append(new_date[0])
                    break
    except:
        pass
    for count in driver.find_elements_by_xpath("//span[@class='style-scope ytd-video-meta-block']"):
        for t in months:
            if re.findall(f"{t} \d+, \d+",count.text) != []:
                new_date=re.findall(f"{t} \d+, \d+",count.text)
                dates.append(new_date[0])
                break
    path = 'C:/Users/mcint/py/episodes_' + show_name + '/' + str(i)
    isdir = os.path.isdir(path)
    if isdir == False:
        os.makedirs(path)
    for final in range(0,length):
        data={"number of episode":final+1,"date":dates[final],"runtime":runtimes[final],"episode_name":titles[final]}
        with open(f"{path}/{final+1}.json",'w+') as f:
            json.dump(data,f)