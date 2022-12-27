'''
syntax of Xpath
# xpath always start with forward slash
# example
//input[@value='log in']
//input[@type='log in']
1.values or type is recommended  in single qoutes.
2.his is xpath with single attribute value input=tagname, attribute preceded by the @ symbol.
3.Always use static attributes.
4.We can use any attribute value.
'''

'''
1.Use multiple attribute with OR condition.
2.Can use any attribute.
//input[@value='login' or @type='Logging']
here or is case sensitive.
'''
'''
1.Use multiple attributes with AND
2.Here and is case sensitive.

//Select[@name='birthday_day' and @title='birthday']
'''
'''
Use * in place of attribute name
Use * in place of tag name

//select[@*='login] It matches any element with tag select and any attribute.
//*[@type='log in'] It matches any element with any tag anf type attribute
//*[@*='log in]it matches the element with any tag and attribute name.

'''
'''
xpath using the Inner_Text  text() is inbuild function in the selenium to find the text on the element to match the element

//dev[text()='Create a new account'] here no need to use '@' symbol beacuse text is not attribute but we have to use () symbol.

//a[text()='Create a Page']
'''
'''
xpath using the partial innertext.
we can use this when there is not attribute value to find the xpath value.
//dev[text()='Create a new account'] sometimes 'Create a new account'  value text is dynamic, so we can write the xpath using the partial text.

//dev[contains(text(),'new account')]

'''
'''
Xpath using the partial value of attribute.
//input[@type='username'] normal one
//input[contains(@type(),'username'] here we have to use @ symbol since we are searching by using the attribute value.

'''
'''
when mentioned rules are not working , we can use Location of elements using the its parents methods.

URL used:
https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f

//*[@id="login-form"]/div[1]/div
'''
'''
LOcation of element using its child
//input[@type='email']/parent::div/parent::form
'''
'''
Xpath starts with 
//input[start-with(@id,'message')]
'''
'''
Locate Elements through its siblings
Consider we are not able to locate any element by using any above methods.
'''

'''
Xpath axes methods
1.following 
//input[@type='text']//following::input if this path matches more than one elemnet we can focus on the specific element by index
//input[@type='text']//following::input[1]
2.ancestor -it will select all the ancestor elements of current node. 
//input[text()='Enterprise testing']//ancestor::div input if this path matches more than one elemnet we can focus on the specific element by index
//input[text()='Enterprise testing']//ancestor::div[1]
3.child - it will select all the child element
//input[@type='Java Technologies']//child::li input if this path matches more than one elemnet we can focus on the specific element by index
//input[@type='Java Technologies']//child::li[1]
4.preceding - it will match all node come before the current node
//*[@type='submit']//preceding::input
we can focus on the particular element just by index
//*[@type='submit']//preceding::input[1]
5.following-siblings
xpath=//*[@type='submit']//following-sibling::input
6.Parent
Xpath=//*[@id='rt-feature']//parent::div
Xpath=//*[@id='rt-feature']//parent::div[1] we can focus on spcific element
7.Self:
Selects the current node or 'self' means it indicates the node itself as shown in the below screen.
Xpath =//*[@type='password']//self::input
Descendant:In the below expression, it identifies all the element descendants to current element 
Xpath=//*[@id='rt-feature']//descendant::a
Xpath=//*[@id='rt-feature']//descendant::a[1] to focus on specific element
'''

'''



'''