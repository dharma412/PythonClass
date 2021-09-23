from common.constants import CONSTANTS

PORTAL_SSE = CONSTANTS()

PORTAL_SSE.LOGIN_BUTTON_1 = "//button[@id='loginButton']"
PORTAL_SSE.USERNAME_FIELD = "//input[@id='user_email']"
PORTAL_SSE.PSW_FIELD = "//input[@id='user_password']"
PORTAL_SSE.LOGIN_BUTTON_2 = "//button[@name='button']"
PORTAL_SSE.ADD_DEVICE_BUTTON = "//span[@id='deviceAddButton']"
PORTAL_SSE.ADD_DEVICE_OK_BUTTON = "//button[@id='addViewDialogOkButton']"
PORTAL_SSE.CLOSE_BUTTON = "//button[@id='closeBtn']"
PORTAL_SSE.REFRESH_BUTTON = "//span[@id='refreshTableBtn']"
PORTAL_SSE.COPY_BUTTON = "//span[@class='icon-send-copy']"
PORTAL_SSE.TOKEN_STR = "//p[@id='tokenSuccess']/b"
PORTAL_SSE.TRASH_ICON = "//span[@class='icon-trash']"
PORTAL_SSE.DELETE_CONFIRM = "//button[@id='deleteDeviceConfirmBtn']"
PORTAL_SSE.NUM_OF_ENTRIES = "//span[@class='total-results']"
PORTAL_SSE.CISCO_SECURITY_ACCOUNT = "//span[contains(text(),'Cisco Security Account')]"
PORTAL_SSE.SSE_LOGO = "//h2[contains(text(),'Security Services Exchange')]"
