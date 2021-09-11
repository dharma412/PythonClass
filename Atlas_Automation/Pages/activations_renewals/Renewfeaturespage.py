from selenium.webdriver.common.by import By
from robot.api import logger

from SeleniumHelper import SeleniumHelper
import CreateCustomer

class Renewfeaturespage:
    def __init__(self):
        self.btn_renew_feature = By.NAME,"add_renew_features"
        self.txt_renew_feature_end_date = By.ID,"feat_end_date"
        self.txt_renew_feature_comment = By.ID,"comment"
        self.btn_renew_feature_ok = By.NAME,"submit"

    def renew_features(self,days):
        SeleniumHelper.click_element(self.btn_renew_feature )
        end_date = CreateCustomer.get_days_from_now(days)
        SeleniumHelper.send_keys(self.txt_renew_feature_end_date,end_date)
        SeleniumHelper.send_keys(self.txt_renew_feature_comment,"Updating features till {}".format(end_date))
        SeleniumHelper.click_element(self.btn_renew_feature_ok)
        return end_date

    def compare_feature_after_renewal(self,feature_before_renew,feature_after_renew,end_date):
        expected_feature_with_end_dates ={}
        for f in feature_before_renew:
            expected_feature_with_end_dates[f.get('feature_name')] = end_date.strip()
        actual_feature_with_end_dates = {}
        for f in feature_after_renew:
            actual_feature_with_end_dates[f.get('feature_name')] = f.get('end_date')

        logger.info("Actual feature renewal - {}".format(actual_feature_with_end_dates))
        logger.info("Expected feature renewal - {}".format(expected_feature_with_end_dates))
        if expected_feature_with_end_dates == actual_feature_with_end_dates:
            logger.info("Feature renewal passed")
            return True
        else:
            logger.info("Feature renewal failed")
            return False

