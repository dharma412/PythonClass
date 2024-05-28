

def SelectClass(url,text=None,index=None,value=None):
    from selenium.webdriver.support.select import Select
    import chromedriver_autoinstaller
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.implicitly_wait(0.5)
    driver.get(url)
    # identify dropdown with Select class
    print(type(driver.find_element_by_id("RESULT_RadioButton-9")))
    sel = Select(driver.find_element_by_id("RESULT_RadioButton-9"))
    #select by select_by_visible_text() method
    sel.select_by_visible_text(text)

    #sel.select_by_value("Radio-2") # value attribute is in html

    #sel.select_by_index(2) # index start from 0
    #sel.deselect_all()

SelectClass("https://fs2.formsite.com/meherpavan/form2/index.html?1537702596407","Afternoon")

#time.sleep(0.8)
#select by select_by_index() method

# count number of option in drop list

#print(len(sel.options))

# print only options and assign in variable
#all_options=sel.options

#for i in all_options:
    #print(i.text)