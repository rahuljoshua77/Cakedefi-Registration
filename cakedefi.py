import requests
import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os, random, time, requests
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd

cwd = os.getcwd()
opts = uc.ChromeOptions()

 
 
opts.add_argument('--start-maximized')
 
def xpath_type(el,mount):
    return wait(browser,15).until(EC.element_to_be_clickable((By.XPATH, el))).send_keys(mount)
 
def xpath_el(el):
    element_all = wait(browser,30).until(EC.element_to_be_clickable((By.XPATH, el)))
    
    return browser.execute_script("arguments[0].click();", element_all)
        
def register(data):
    global email
    global password
    email = data.split("|")[0]
    password = data.split("|")[1]
    
    get_id = get_id[1]
    while True:
        time.sleep(5)
        r = requests.get(f'https://2captcha.com/res.php?key= &action=get&id={get_id}')

        if r.text == "CAPCHA_NOT_READY":
            print(f"[*] [{email}] {r.text}!")
        else:
            global token_captcha
            print(f"[*] [{email}] Captcha Solved")
            get_capt =  str(r.text)
            ress = get_capt.split("|")
            token_captcha = ress[1]
            break
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,id;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://app.cakedefi.com/register",
        "Referrer-Policy": "no-referrer-when-downgrade"
    }

    data = {
    "email": email,
    "password": password_acc,
    "g-recaptcha-response": token_captcha,
    "promoCode": "",
    "affiliateRefCode": "",
    "referredById": "",
    "currentLanguage": "en",
    "utm_source": "",
    "utm_medium": "",
    "utm_campaign": "",
    "revealInfoToReferrer": "",
    "learnAndEarnCode": "",
    "voucherCode": ""
    }
    global send
    send = requests.Session()
    response = send.post("https://api.cakedefi.com/register",json=data,headers=headers).text
    if "emailVerified" in str(response):
        print(f"[*] [{email}] Registrated, Trying to Verification!")
        try:
            verification()
        except:
            print(f"[*] [{email}] Verification Failed")
            with open('fail.txt','a') as f: f.write(f'{email}|{password_acc}\n')
            browser.quit()
            
    else:
        print(f"[*] [{email}] {response}")
    
def get_otp():
    global browser
   
    browser = uc.Chrome(driver_executable_path=f"{cwd}//chromedriver.exe")
    browser.get('https://mail.google.com/mail/u/0/#inbox')
    sleep(3)
    xpath_type('//input[@type="email"]',email)
    sleep(1)
    xpath_type('//input[@type="email"]',Keys.ENTER)
    sleep(3)
    xpath_type('//input[@type="password"]',password)
    sleep(1)
    xpath_type('//input[@type="password"]',Keys.ENTER)
    print(f'[*] [{email}] Checking mail')
    sleep(5)
    browser.get('https://mail.google.com/mail/u/0/#inbox')
    sleep(2)
    xpath_el('(//span[contains(text(),"[Cake] Verify Your Email")])[2]')
    sleep(3)
    your_otp = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '(//*[@style="padding:10px 25px;word-break:break-word"])[4]'))).text
     
    return your_otp

def verification():
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,id;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://app.cakedefi.com/email-verification/email",
        "Referrer-Policy": "no-referrer-when-downgrade"
    }
    otp = get_otp()
    
    data = {"userEmail":email,"token":f"{otp}"}
    response = send.put("https://api.cakedefi.com/verify/email/token",json=data,headers=headers)
    if '{"emailVerified":true}' in response.text:
        print(f"[*] [{email}] Verification Success")
        with open('success.txt','a') as f: f.write(f'{email}|{password_acc}\n')
    else:
        print(f"[*] [{email}] Verification Failed")
        with open('fail.txt','a') as f: f.write(f'{email}|{password_acc}\n')
    
    browser.quit()
if __name__ == '__main__':
    global password_acc
    
    print('[*] Cakedefi Registration')
    password_acc = input("[*] Password Account: ")
    myfile = open(f"{cwd}\\list.txt","r")
    list_account = myfile.read()
    list_accountsplit = list_account.split("\n")
    for i in list_accountsplit:
        register(i)

                            
            
