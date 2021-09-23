#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/cres_client.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import atexit

from common.util.connectioncache import ConnectionCache
from common.util.utilcommon import UtilCommon

from sal.clients.cres import CRESGUIClient


class CRESClient(UtilCommon):
    """Keywords for interacting with Cisco
    Registered Envelope Service (CRES) server.
    """
    CLIENTS_CACHE = ConnectionCache(no_current_msg='You should connect at least ' \
                                                   'one host running CRES server')

    def get_keyword_names(self):
        return ['cres_client_connect',
                'cres_client_switch',
                'cres_client_disconnect',

                'cres_client_provision_account']

    def _get_client_obj(self):
        return self.CLIENTS_CACHE.current

    def cres_client_connect(self, host, username, password):
        """Connect to CRES server and cache connection

        *Parameters:*
        - `host`: CRES server host
        - `username`: CRES provisioning admin account name
        - `password`: CRES provisioning admin account password

        *Examples:*
        | CRES Client Connect | ${CRES_SERVER} |
        | ... | ${CRES_ADMIN} | ${CRES_ADMIN_PASSWORD} |
        """
        try:
            self.cres_client_switch(host)
        except ValueError:
            self.CLIENTS_CACHE.register(CRESGUIClient(host, username, password),
                                        host)

    def cres_client_disconnect(self):
        """Close current connection to CRES server

        *Exceptions:*
        - `ValueError`: if there are no opened and active CRES server connections

        *Examples:*
        | CRES Client Connect | ${CRES_SERVER} |
        | ... | ${CRES_ADMIN} | ${CRES_ADMIN_PASSWORD} |
        | CRES Client Disconnect |
        """
        current_client = self._get_client_obj()
        current_client.close()
        self.CLIENTS_CACHE.delete(current_client.host)

    def cres_client_switch(self, host):
        """Switch current connection to CRES server

        *Parameters:*
        - `host`: CRES server host to which connection already exists

        *Exceptions:*
        - `ValueError`: if there are no opened and active CRES server connection
        to `host`

        *Examples:*
        | CRES Client Connect | ${CRES_SERVER} |
        | ... | ${CRES_ADMIN} | ${CRES_ADMIN_PASSWORD} |
        | CRES Client Connect | esx17-cres3q01.qa.sbr.ironport.com |
        | ... | rtestuser2@ironport.com | ironport2 |
        | CRES Client Switch | ${CRES_SERVER} |
        """
        self.CLIENTS_CACHE.switch(host)

    def cres_client_provision_account(self, account_info,
                                      should_raise_if_acc_exists=False):
        """Provision account on CRES server

        *Parameters:*
        - `account_info`: dictionary containing account settings.
        Dictionary items are:
        | `Account Name` | account name to be created on CRES server |
        | `Activation Key` | serial number of the appliance to be provisioned |
        - `should_raise_if_acc_exists`: whether to raise an exception if account
        with same name was already provisioned on CRES server. ${False} by default

        *Exceptions:*
        - `ValueError`: if there are no connected hosts
        - `AssertionError`: if there was an error in provisioning procedure

        *Examples:*
        | ${version_info}= | Version |
        | ${activation_key}= | Evaluate |
        | ... | re.search(r'Serial #: ([\\w\\-]+)', '''${version_info}''').groups()[0] | re |
        | ${account_info}= | Create Dictionary |
        | ... | Account Name | ${ESA} |
        | ... | Activation Key | ${activation_key} |
        | CRES Client Provision Account | ${account_info} | ${True} |
        """
        self._get_client_obj().provision_account(account_info,
                                                 should_raise_if_acc_exists)


def shutdown_active_cres_clients():
    for conn in CRESClient.CLIENTS_CACHE.get_all_current():
        conn.close()


atexit.register(shutdown_active_cres_clients)
