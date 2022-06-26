class Amy:
    def __init__(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver import ActionChains
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        import undetected_chromedriver as uc

        from time import sleep

        #Definig variables which will be used during the work.
        login_url = "https://accounts.google.com/signin"
        mail_url = "https://mail.google.com/mail/u/0/#inbox"
        user_account = "dr246029@gmail.com"
        psw = "Pa$s1234"
        invalid_psw = "1111"

        #This is an item we are looking for. Can be set manually or asked from user by input method....
        required_item = 3

        #Unfortunately, the only way I found to bypass the google protection of using Chrome in automated mode for gmail testing is to use undetected_chromedriver
        #undetected_chromedriver must be imported: import undetected_chromedriver as uc and installed: pip3 install undetected_chromedriver
        #Restriction: Chrome must be updated to the last version
        driver = uc.Chrome(use_subprocess = True)
        delay = 10
        wait = WebDriverWait(driver, delay)

        #Starting Chrome
        def start_browser():
            driver
            driver.maximize_window()
            driver.get(login_url)
            driver.implicitly_wait(10)

        #This function gets the N-th item in the mailbox
        def get_nth_item(item):
            xpt = "/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[9]/div/div[1]/div[3]/div/table/tbody/tr[" + str(item) + "]"
            ttl = "/td[5]/div/div/div/span/span"
            snd = "/td[4]/div[2]/span/span"
            item_title = wait.until(EC.presence_of_element_located((By.XPATH, xpt + ttl))).get_attribute("innerHTML")
            sender_details = wait.until(EC.presence_of_element_located((By.XPATH, xpt + snd))).get_attribute("innerHTML")
            return [sender_details, item_title, item]

        #This function counts and returning the total number of items in the mailbox
        def count_items():
            inbox_items = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=":4r"]/span/span[2]'))).get_attribute("innerHTML")
            if int(inbox_items) > 999:
                return int(inbox_items.replace(",", ""))
            else:
                return int(inbox_items)
            
        #This function counts items per page
        def get_items_list():
            items_in_page = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "zA")))
            return items_in_page

        #In case there are more than one page in the mailbox, this functions takes the user to the required page(in which the required item was detected)
        def pagination(num, item):
            for i in range(0, num):
                    next_page = wait.until(EC.presence_of_element_located((By.ID, ":4t")))
                    next_page.click()
                    sleep(3)
            return [get_nth_item(item)[0], get_nth_item(item)[1], num]

        #Gathering the required data: Sender, Title and Required item
        def getting_data(num):
            required_item = num
            inbox_items = count_items()
            if required_item == 0:
                required_item = inbox_items
            if required_item <= inbox_items:
                items_in_page = get_items_list()
                if required_item > len(items_in_page):
                    page = (required_item - 1) // items_in_page
                    required_item = required_item - (page * len(items_in_page))
                    return pagination(page,required_item)
                else:
                    return get_nth_item(required_item)
            else:
                print("The selected item doesn't exist")
                driver.quit()

        start_browser()
        login_input = wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
        login_input.send_keys(user_account)

        next_button = wait.until(EC.presence_of_element_located((By.ID, "identifierNext")))
        next_button.click()

        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_input.send_keys(psw)

        next_pass = wait.until(EC.presence_of_element_located((By.ID, "passwordNext")))
        next_pass.click()

        driver.get(mail_url)
        driver.get(mail_url)

        print(getting_data(required_item))




if __name__ == '__main__':
    amy=Amy()