# we can locate the elements by
#id   -- which fast-- done
#class name  ---done
#name  -- done
#xpath  --  done
#link test   -  done
#partical link text  - donetag name   -- tag name
#css selector   ---

#************  id *****************

#********** xpath *************
    #relative xpath (xml path)  - //*[@id="pass"]
    #absolute xpath (xml path)  -- / single forward slash

# //a[contains(text(),"Privacy")]

#relative xpath
    #1.way  (tag,attribute, value)  , *
        #//tag[@attribute=value]
            #//*[@*="password"]
            # text()--function
            #contains---function
        #//a[text()="Forgotten password?"]
        # //a[contains(text(),"password")]
        # //input[contains(@type,'text')]
        # starts-with
            #//input[starts-with(@type,"pass")]

        # COMBINE multiple xpaths
            #//input[@type='password' or @name='pass1']  # or and and is case sensitive
            # //input[@type="text" and @name="email2"]

        #axes methods
            # to find complex and dynamic xpaths.
                #following  --- select all elememts in the document of the current node.
                    #//input[contains(@type,"text")]//following::a
                #ancestor   ---
                    #
                #Parent  --//a[text()="Sign in"]//parent::li//parent::ul//parent::div//parent::div
                #child    -- (//div//child::div[@class="_6lux"]//child::input)[2]

                #preceding  --
                #following-sibling.  -- doone
                #Self  --
                #Descendant

#**************** link test  ******
#*** css selector

#with ID
    #syntax: tagname#IDValue
    #input#email
    #syntax: tag.classname

    # syntax: tagname[attribute=value]
        #tagname[attribute=value][attribute=value]

    # tag attribute class value
        # tag.classname[attribute=value]
            #a._97w5[rel="nofollow"]
            #div._58mk[id="reg_pages_msg"]

    #CSS Selector - inner text
        #syntax---#css=tag.contains("inner text")
        #css=font:contains("Password:")

    # ^ for matching starting value of attribute
        #syntax :  tag[name^='startingvalueof']
        #input[type^='tex']

    #  $ for matching end value of attribute value
        #syntax : tag[name$='value']
        #input[name$='il']
        #input[name^='ema']

    #  * for matching sub string of value of attribute
        #syntax  :  tag[name*='ame']
        #input[name*='mail']

    #  Syntax:
    # To find child element we need to use >
    # tagName[attribute_name=’attribute_value’]>tagName_of_child
    #div[class="_6lux"]>input
    # TO find subchild elemenet we need to use " " space
    # div[class="_6lux"] input

    # To find the siblings
        # div[class="_6lux"]+div

    # Select by CSS Psedo-classes
        #first-child
            #div[class="_8iep _8icy _9ahz _9ah-"]>div:first-child
        #last-child
            #div[class="_8iep _8icy _9ahz _9ah-"]>div:last-child

        # nth-child
            #div[class="_8iep _8icy _9ahz _9ah-"]>div:nth-child(1)

        # first of type
            #div[class="_8iep _8icy _9ahz _9ah-"]>div:first-of-type
        #last of type
            #div[class="_8iep _8icy _9ahz _9ah-"]>div:last-of-type
        #nth-of-type
            #div[class="_8iep _8icy _9ahz _9ah-"]>div:nth-of-type(2)

        #div[class="_8iep _8icy _9ahz _9ah-"]>div:not([id="reg_pages_msg"])
            #div[class="_8iep _8icy _9ahz _9ah-"]>div:not([id="reg_pages_msg"])



#div[class="clearfix _5466 _44mg"] div:nth-of-type(1)

#div[class="clearfix _5466 _44mg"] div:not([class="_9lsa"])
