import selenium
from selenium import webdriver
from time import sleep
import simpleaudio as sa
import time
from webdrivermanager import ChromeDriverManager

from credentials import *


class Teams:
    def __init__(self):

        self.names = []
        self.previous_names = []

        self.unmuted = True
        self.mute_value = ""

        gdd = ChromeDriverManager()
        gdd.download_and_install()
        self.driver = webdriver.Chrome()
        self.driver.get("https://teams.microsoft.com")
        sleep(2)

    def login(self):
        if pw and email:
            try:
                self.driver.find_element_by_xpath(
                    '//*[@id="i0116"]') \
                    .send_keys(email)
                self.driver.find_element_by_xpath(
                    '// *[ @ id = "idSIButton9"]') \
                    .click()
                sleep(1)
                self.driver.find_element_by_xpath(
                    '//*[@id="i0118"]') \
                    .send_keys(pw)
                self.driver.find_element_by_xpath(
                    '// *[ @ id = "idSIButton9"]') \
                    .click()
                sleep(2)
                self.driver.find_element_by_xpath(
                    '//*[@id="idSIButton9"]') \
                    .click()
            except selenium.common.exceptions.NoSuchElementException:
                pass
            except selenium.common.exceptions.StaleElementReferenceException:
                pass

    def get_names(self):
        self.previous_names = self.names
        try:
            in_call = self.driver.find_element_by_xpath(
                "//*[@id=\"page-content-wrapper\"]/div[1]/div/calling-screen/div/div[2]/meeting-panel-components/calling-roster/div/div[3]/div/div[1]/accordion/div/accordion-section[2]/div/calling-roster-section/div")
            name_objects = in_call.find_elements_by_class_name('ts-user-name')
            self.names = []
            for name_object in name_objects:
                self.names.append(name_object.text)
                # print(name_object.text)
        except selenium.common.exceptions.NoSuchElementException:
            if self.names != ["No Element"]:
                # print("No Element found! (Probably logged out or switched window)")
                self.names = ["No Element"]
        except selenium.common.exceptions.StaleElementReferenceException:
            pass


    def check_mute(self):
        try:
            bar = self.driver.find_element_by_class_name("ts-calling-unified-bar-container")
            unmuted_icon = bar.find_elements_by_class_name("icons-call-microphone")
            self.unmuted = True if unmuted_icon else False
        except selenium.common.exceptions.NoSuchElementException:
            self.unmuted = False
        try:
            self.mute_value = self.driver.find_element_by_xpath("//*[@data-tid=\"peoplePicker\"]") \
                .get_attribute('value')
        except selenium.common.exceptions.NoSuchElementException:
            pass
        except AttributeError:
            pass


session = Teams()
session.login()
session.get_names()
last_run_names = time.time()
last_run_mute = time.time()

while True:

    if (time.time() - 0.25) >= last_run_names:
        last_run_names = time.time()
        session.get_names()

        logout = False
        login = False
        logout_error = False
        login_error = False

        for previous_name in session.previous_names:
            if previous_name not in session.names:
                print("{} logged out!".format(previous_name))
                logout = True
                if previous_name == "" or previous_name == "No Element":
                    logout_error = True
        for name in session.names:
            if name not in session.previous_names:
                print("{} logged in!".format(name))
                login = True
                if name == "" or name == "No Element":
                    login_error = True

        if logout and not logout_error and not login_error:
            wave_obj = sa.WaveObject.from_wave_file("logout.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()
        if login:
            if login_error:
                wave_obj = sa.WaveObject.from_wave_file("error.wav")
            else:
                wave_obj = sa.WaveObject.from_wave_file("login.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()

    if (time.time() - 5) >= last_run_mute:
        last_run_mute = time.time()
        session.check_mute()
        if session.unmuted and session.mute_value != "off":
            wave_obj = sa.WaveObject.from_wave_file("unmuted.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()
