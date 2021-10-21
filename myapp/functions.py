#import csrf from CSRF protection
from django.views.decorators.csrf import csrf_exempt
#import df_library
from library.df_response_lib import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options  
from django.core.mail import send_mail
from multiprocessing import Pool
import json
import time


########################################################################
#                                                                      #
#                           MOCK FUNCTIONS                             #
#                                                                      #
########################################################################

#sign in to todoist
def login():  
    #for a headless browser
    #chrome_options = Options()  
    #chrome_options.add_argument("--headless")  
    #driver = webdriver.Chrome(chrome_options=chrome_options)
    driver=webdriver.Chrome(r'C:\Users\21261\Desktop\try\Browsers\chromedriver.exe') 
    driver.maximize_window()
    driver.get("https://todoist.com/")
    #Input credentials
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[1]/header/nav/div/ul[2]/li[1]/a'))).click()
    email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'email')))
    email.send_keys("mailtestismail@gmail.com ")
    driver.find_element_by_id("password").send_keys("testmail789")
    driver.find_element_by_xpath("//*[@id='login_form']/button").click()
    return driver

def register_forgotten_password(name):
    driver = login()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='agenda_view']/div/section/div/ul/li/button"))).click()
    task = driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[1]/div[1]/div/div/div/div[2]/div/div/div/div")
    task.send_keys("Reset Password")
    description = driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[1]/div[1]/textarea")
    description.send_keys(name)
    driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[2]/div/div[1]/button").click()
    driver.close()
    send_email(name, "76466@aui.ma")

def register_lost_token(name):
    driver = login()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='agenda_view']/div/section/div/ul/li/button"))).click()
    task = driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[1]/div[1]/div/div/div/div[2]/div/div/div/div")
    task.send_keys("Recycle Token")
    description = driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[1]/div[1]/textarea")
    description.send_keys(name)
    driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[2]/div/div[1]/button").click()
    driver.close()
    send_email(name, "76466@aui.ma")

def register_user_right_reset(name, right):
    driver = login()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='agenda_view']/div/section/div/ul/li/button"))).click()
    task = driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[1]/div[1]/div/div/div/div[2]/div/div/div/div")
    task.send_keys("Set User Right: "+right)
    description = driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[1]/div[1]/textarea")
    description.send_keys(name)
    driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[2]/div/div[1]/button").click()
    driver.close()

#to be replaced by email to IT personnel containing
#necessary info about the user
def register_contact_user(name):
    driver = login()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='agenda_view']/div/section/div/ul/li/button"))).click()
    task = driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[1]/div[1]/div/div/div/div[2]/div/div/div/div")
    task.send_keys("Contact User")
    description = driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[1]/div[1]/textarea")
    description.send_keys(name)
    driver.find_element_by_xpath("//*[@id='agenda_view']/div/section/div/ul/li/form/div[2]/div/div[1]/button").click()
    driver.close()

#sending email to the user
def send_email(name, email):
    send_mail(
    'Demande Traitée',
    f'Bonjour {name}, Votre demande a été traitée avec succès\n\n ____________________________________________'+
    '\n\nCeci est un email automatique, merci de ne pas répondre\n\n',
    'from@yourdjangoapp.com',
    [email],
    fail_silently=False,
    )

########################################################################
########################################################################

#sending contact email
def send_contact_email(email, name, email_from, subject, message):
    send_mail(
    'Email Depuis le Formulaire de Contact',
    f"- Nom de l'expéditeur: {name}\n"+
    f"- Email de l'expéditeur: {email_from}\n"+
    f"- Sujet du message: {subject}\n"+
    f"- Message:\n\t{message}\n\n ____________________________________________"+
    '\n\nCeci est un email automatique, merci de ne pas répondre\n\n',
    'from@yourdjangoapp.com',
    [email],
    fail_silently=False,
    )