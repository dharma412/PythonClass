#!/usr/bin/env python -tt

from common.gui.decorators import go_to_page, set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

CERTIFICATE_PATH = "cert_file"
CERTIFICATE_PASSWORD = "//input[@id='cert_pass']"
CERTIFICATE_NAME = "//input[@id='cert_name']"
NEXT_BUTTON = "//input[starts-with(@value, 'Next') and @type='button']"
FQDN_VALIDATION = "//input[@id='fqdn_validation']"
UPLOAD_SIGNED_CERT = "//input[@name='signed_cert']"
DOWNLOAD_CSR = "//a[contains(text(), 'Download Certificate Signing Request')]"
INTERMEDIATE_CERT_OPEN_ARROW = "//img[@id='interm_certs_arrow']"
UPLOAD_INTERMEDIATE_CERT = "//input[@name='interm_cert']"


class ImportSettings(InputsOwner):
	def _get_registered_inputs(self):
		return get_module_inputs_pairs(__name__)

	def set(self, new_value):
		browse_element = self.gui._selenium.find_element_by_name(
			CERTIFICATE_PATH)
		browse_element.send_keys(new_value['Path'])
		self.gui.input_text(CERTIFICATE_PASSWORD, new_value['Password'])
		self.gui.click_button(NEXT_BUTTON)
		self.gui._wait_until_element_is_present(CERTIFICATE_NAME)
		self.gui.input_text(CERTIFICATE_NAME, new_value['Name'])

		if 'FQDN Validation' in new_value:
			if new_value['FQDN Validation'].lower() == 'yes':
				self.gui._select_checkbox(FQDN_VALIDATION)
			else:
				self.gui._unselect_checkbox(FQDN_VALIDATION)

		if 'Signed Certificate' in new_value:
			self.gui.input_text(UPLOAD_SIGNED_CERT, new_value['Signed Certificate'])

		if 'Intermediate Certificate' in new_value:
			self.gui.click_element(INTERMEDIATE_CERT_OPEN_ARROW)
			self.gui.input_text(UPLOAD_INTERMEDIATE_CERT, new_value['Intermediate Certificate'])
		
		if 'Download CSR' in new_value:
			self.gui.click_element(DOWNLOAD_CSR)
