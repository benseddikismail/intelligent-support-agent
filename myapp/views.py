from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#import csrf from CSRF protection
from django.views.decorators.csrf import csrf_exempt
#import df_library
from library.df_response_lib import *
from .models import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options  
from django.core.mail import send_mail
from multiprocessing import Process
from .functions import *

import json
import time

@csrf_exempt
def home(request):
    return render(request, 'myapp/index.html')

@csrf_exempt
def contact(request):
    msg = "Une erreur s'est produite lors de l'envoi du formulaire. Veuillez réessayer !"
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_process = Process(target=send_contact_email, args=("76466@aui.ma", name, email, subject, message,))
        contact_process.start()       
        msg = "OK"
    return HttpResponse(msg)

@csrf_exempt
def popup(request):
    msg = "Une erreur s'est produite lors de l'envoi du formulaire. Veuillez réessayer !"
    if request.method == 'POST':
        LN = request.POST.get('LN')
        if 'password-FN' in request.POST:
            name = popup_check(LN, request, 'password-FN')
            if name != 'invalid':
                password_process = Process(target=register_forgotten_password, args=(name,))
                password_process.start()             
                msg = "OK"
                return HttpResponse(msg)
            else:
                msg = "Votre nom n'a pas été trouvé. Merci de bien saisir votre nom et prénom !"
                return HttpResponse(msg)
        if 'token-FN' in request.POST:
            name = popup_check(LN, request, 'token-FN')
            if name != 'invalid':
                token_process = Process(target=register_lost_token, args=(name,))
                token_process.start()    
                msg = "OK"
                return HttpResponse(msg)
            else:
                msg = "Votre nom n'a pas été trouvé. Merci de bien saisir votre nom et prénom !"
                return HttpResponse(msg)
        if 'rights-FN' in request.POST:
            name = popup_check(LN, request, 'rights-FN')
            if name != 'invalid':
                right = request.POST.get('right')
                rights_process = Process(target=register_user_right_reset, args=(name,right,))
                rights_process.start()   
                msg = "OK"
                return HttpResponse(msg)
            else:
                msg = "Votre nom n'a pas été trouvé. Merci de bien saisir votre nom et prénom !"
                return HttpResponse(msg)
    return HttpResponse(msg)

def popup_check(LN, request, form):
    FN = request.POST.get(form)
    name = str(FN+" "+LN).upper()
    if Client.objects.filter(name = name).exists():
        return name
    else:
        return "invalid"

@csrf_exempt
def webhook(request):
    # build a request object
    global intent, name
    fulfillmentText = None
    req = json.loads(request.body)
    # get action from json
    action = req.get('queryResult').get('action')
    actions_list = ["forgotten_password", "lost_token", "contact_staff"]
    if action == "name_input":
        n = req.get('queryResult').get('parameters').get('name')
        #check if name exists
        name = str(n).upper()
        print(name)
        if Client.objects.filter(name = name).exists():
            if intent == "forgotten_password":
                password_process = Process(target=register_forgotten_password, args=(name,))
                password_process.start() 
                #password_reset(name)
            elif intent == "lost_token":
                token_process = Process(target=register_lost_token, args=(name,))
                token_process.start()   
                #recycle_token(name)
            elif intent == "contact_staff":
                register_contact_user(name)
        else:
            fulfillmentText = {'fulfillmentText': "Votre nom n'a pas été trouvé, veuillez entrer votre nom complet correctement"}
    elif action in actions_list:
        intent = action
    elif action == "user_right_selection":
        right = req.get('queryResult').get('parameters').get('user_rights')
        rights_process = Process(target=register_user_right_reset, args=(name,right,))
        rights_process.start()   
        #set_user_rights(name, right)
    # return response
    return JsonResponse(fulfillmentText, safe=False)

########################################################################
#                                                                      #
#                           MOCK FUNCTIONS                             #
#                                                                      #
########################################################################


########################################################################
########################################################################

#search the person by name
def find_person(name):  
    #for a headless browser
    #chrome_options = Options()  
    #chrome_options.add_argument("--headless")  
    #driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver=webdriver.Chrome(r'path to browser driver') 
    driver=webdriver.Chrome(r'Browsers\chromedriver.exe') 
    driver.maximize_window()
    driver.get("https://dcs.renault.com/")
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "spanIdMenuRenaultN49H904887481C0")))
    element.click()
    element2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "inputIdSearchPattern")))
    element2.send_keys(name)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "imgIdSearchLoupe"))).click()
    element3 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "aIdSearchResult0")))
    element3.click()
    return driver

#mettre à jour mot de passe
def password_reset(name):
    driver = find_person(name)
    element4 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='liIdActions0']/input")))
    element4.click()
    driver.switch_to.window(driver.window_handles[-1])
    #accept the alert
    driver.switch_to.alert.accept()
    element5 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tdIdIpn")))
    username = element5.text
    password = driver.find_element_by_id("tdIdPwd").text
    nom = driver.find_element_by_id("tdIdGivenname").text
    nom = nom[0].upper() + nom[1:]
    email = driver.find_element_by_id("tdIdMail").text
    send_password_email(nom, "76466@aui.ma", username, password)
    driver.close()

#droits utilisateur
def set_user_rights(name, right):
    driver = find_person(name)
    #click on droits d'utilisateur
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='liIdActions2']/input")))
    element.click()
    #click on the selected right
    element1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '{}')]".format(right))))
    element1.click()
    driver.find_element_by_xpath('//*[@id="theadIdRights"]/tr[3]/td[2]/img[2]').click()
    driver.find_element_by_xpath('//*[@id="theadIdSubmit"]/tr/td/input').click()
    driver.close()

#recyclage token
def recycle_token(name):
    i = 0
    driver = find_person(name)
    nom = driver.find_element_by_id("tdIdGivenname").text
    nom = nom[0].upper() + nom[1:]
    email = driver.find_element_by_id("tdIdMail").text
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='liIdActions5']/input")))
    element.click()
    time.sleep(3)
    token = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "imgIdSearchResult"+str(i))))
    title = token.get_attribute("title")
    while title == "token status: recycled":
        try:
            i += 1
            title = driver.find_element_by_id("imgIdSearchResult"+str(i)).get_attribute("title")
        #NoSuchElementException 
        except:
            break
    if title == "token status: recycled":
        print("All tokens recycled")
    else:
        item = driver.find_element_by_id("aIdSearchResult"+str(i))
        # create action chain object
        action = ActionChains(driver)
        # double click the item
        action.double_click(on_element = item)
        # perform the operation
        action.perform()
        time.sleep(3)
        elt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='liIdActions1']/input")))
        elt.click()
        driver.switch_to.window(driver.window_handles[-1])
        #accept the alert
        driver.switch_to.alert.accept()
    send_recycled_email(nom, "76466@aui.ma")        
    driver.close()

#sending new credentials to user
def send_password_email(name, email, username, password):
    send_mail(
    'Vos Nouveaux Identifiants de Connexion',
    f'Bonjour {name}, votre nouveau Ipn est {username} et votre nouveau mot de passe est {password}\n\n ____________________________________________'+
    '\n\nCeci est un email automatique, merci de ne pas répondre\n\n',
    'from@yourdjangoapp.com',
    [email],
    fail_silently=False,
    )

#sending recycled token email to user
def send_recycled_email(name, email):
    send_mail(
    'Token Recyclé',
    f'Bonjour {name}, votre token a été recyclé avec succès, vous pouvez maintenant en obtenir un nouveau\n\n ____________________________________________'+
    '\n\nCeci est un email automatique, merci de ne pas répondre\n\n',
    'from@yourdjangoapp.com',
    [email],
    fail_silently=False,
    )


