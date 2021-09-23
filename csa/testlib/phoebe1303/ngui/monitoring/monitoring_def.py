from common.constants import CONSTANTS

MONITORING = CONSTANTS()
Reports = {}

MONITORING.MONITORING_URL_PATH       = 'reporting/overview-report'
MONITORING.MONITORING_HEADER_XPATH   = "//a[@translate='header.monitoring']"
MONITORING.VIEW_DATA_FOR             = "//*[@ng-model='$ctrl.selected.groupedApps']"
MONITORING.REPORT_MENU = "//*[@ng-click='$ctrl.toggle()' and @role='button']"
MONITORING.TIME_RANGE = "//*[@ng-model='$ctrl.selected']"
MONITORING.SEARCH_REPORT = "//*[@id='Search']/div[1]"
MONITORING.SEARCH = "//*[@translate='search.reporting.search']"
MONITORING.SEARCH_QUERY = "//*[@name='searchQuery']"


Reports['Remediation Report'] = {'xpath':"//a[@translate='menu_slider.reporting.remediationReports']",
                                  'href': "/reporting/remediationreports"}
Reports['Mail Flow Summary'] = {'xpath':"//a[@translate='menu_slider.reporting.overview']",
                                  'href': "/reporting/overview-report"}
Reports['User Mail Summary']= {'xpath':"//a[@translate='menu_slider.reporting.internalUsers']",
                                  'href': "/reporting/internalUsers"}
Reports['Advanced Phishing Protection'] = {'xpath':"//a[@translate='menu_slider.reporting.advancedPhishingProtection']",
                                  'href': "/reporting/advanced-phishing-protection"}
Reports['Delivery Status'] = {'xpath':"//a[@translate='menu_slider.reporting.deliveryStatus']",
                                  'href': "/reporting/delivery-status"}
Reports['System Status'] = {'xpath':"//a[@translate='menu_slider.reporting.systemStatus']",
                                  'href': "/reporting/system-status"}