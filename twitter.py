from warnings import simplefilter
from selenium import webdriver
import time
from os import close
from selenium.webdriver.common import action_chains 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from userinfo import userName, passWord

keyword = input("What do you want to get Tweets about: ")

class Twitter:
    def __init__(self, userName, passWord):
        self.browser = webdriver.Chrome()
        self.userName = userName
        self.passWord = passWord

    def signin(self):
        self.browser.get("https://twitter.com/login?lang=tr")
        time.sleep(2)
        self.browser.maximize_window()
        self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input").send_keys(userName)
        self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input").send_keys(passWord)
        self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div").click()
        time.sleep(2)

    def gettweets(self):
        searchinput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/label/div[2]/div/input")
        time.sleep(2)
        searchinput.send_keys(keyword)
        time.sleep(2)
        searchinput.send_keys(Keys.ENTER)
        time.sleep(2)
        searchinput2 = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div")
        searchinput2.click()
        time.sleep(2)
        
        resultlist = []

        list = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[2]/div[1]")
        time.sleep(2)
        print("count: "+ str(len(list)))

        for i in list:
            resultlist.append(i.text)

        loopcounter = 0 # popüler kelimelerle arama yapıldığında çok fazla tweet gelecektir ve bundan dolayı scroll bar'ın ne kadar kaydırılacağını sınırlamak gerekir. bu değişken bunun için tanımlanır.
        last_height = self.browser.execute_script("return document.documentElement.scrollHeight") # execute_script, JavaScript komutlarını çalıştırıyor. Bu satırdaki kod scroll barın son yüksekliğini döndürür.
        
        while True:
            if loopcounter > 5:
                break
            self.browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
            time.sleep(2)
            new_height = self.browser.execute_script("return document.documentElement.scrollHeight") # execute_script, JavaScript komutlarını çalıştırıyor. Bu satırdaki kod scroll barın yeni yüksekliğini döndürür.
            if last_height == new_height:
                break
            last_height = new_height
            loopcounter+=1

            list = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[2]/div[1]")
            time.sleep(2)
            print("count: "+ str(len(list)))

            for i in list:
                resultlist.append(i.text)
        count = 1
        with open("saved_tweets.txt", "w", encoding="UTF-8") as file:
            for item in resultlist:
                file.write(f"{count}-{item}\n")
                count+=1
                
        # count = 1
        # for item in resultList:
        #     print(f"{count}-{item}")
        #     count +=1
        #     print("\n*******************************************************************************************************\n")
        print(f"{len(resultlist)} tweets found.")
        print("Tweets has been saved.")
        self.browser.close()    
   

twttr = Twitter(userName,passWord)
twttr.signin()
twttr.gettweets()


      








