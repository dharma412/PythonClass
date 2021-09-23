#!/usr/bin/env python -tt
from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs

from ldap_queries import get_query_class_by_name, get_all_query_classes


TEST_SERVER_BTN = "//input[@id='server_testbtn']"
TEST_RESULTS_DIV = "//div[@id='server_test_results']"


class LDAPQueriesHolder(object):
    def __init__(self, gui_common):
        self.gui = gui_common
        self.__queries_cache = {}

    def _get_query_object(self, query_type):
        """Search for query object in local cache
        and create it if not found

        *Parameters:*
        - `query_type`: the type of destination LDAPQuery descendant
        taken from get_type output

        *Exceptions:*
        - `ValueError`: if there is no class with given name

        *Return:*
        Query object
        """
        dest_class = get_query_class_by_name(query_type)
        if dest_class is None:
            raise ValueError('There is no such LDAP Query Type "%s"' % \
                             (query_type,))
        if dest_class not in self.__queries_cache.keys():
            self.__queries_cache[dest_class] = dest_class(self.gui)
        return self.__queries_cache[dest_class]

    @set_speed(0, 'gui')
    def set_query(self, query_type, new_value):
        """Set settings of particular LDAP query in profile

        *Parameters:*
        - `query_type`: the type of LDAP query to be set
        - `new_value`: dictionary with query settings
        or boolean True/False to enable/disable
        corresponding query

        *Exceptions:*
        - `ValueError`: if any of passed valued is not correct
        """
        if isinstance(new_value, dict):
            dest_query = self._get_query_object(query_type)
            dest_query.set(new_value)
        elif new_value in (True, False):
            self.set_query_state(query_type, new_value)
        else:
            raise ValueError('Unknown settings value "%s" is passed to query '\
                             'type "%s"' % (new_value, query_type))

    @set_speed(0, 'gui')
    def get_query(self, query_type):
        """Get settings of particular LDAP query in profile

        *Parameters:*
        - `query_type`: the type of LDAP Server query

        *Exceptions:*
        - `ConfigError`: if query with given name is not enabled

        *Return:*
        Dictionary whose keys are setting names and values are their
        values
        """
        dest_query = self._get_query_object(query_type)
        return dest_query.get()

    def set_queries(self, settings):
        """Set settings of multiple LDAP queries in profile

        *Parameters:*
        - `settings`: dictionary, whose items are:
        Key: type of a query to be set
        Value: corresponding query settings dictionary

        *Exceptions:*
        - `ValueError`: if any of passed valued is not correct
        """
        for name, value in settings.iteritems():
            self.set_query(name, value)

    def get_queries(self):
        """Get settings of multiple LDAP queries in profile

        *Return:*
        Dictionary, whose items are:
        Key: name of a query
        Value: corresponding query settings dictionary
        Disabled queries will not be present in this dictionary
        """
        all_names = map(lambda x: x.get_type(), get_all_query_classes())
        details = {}
        for query_type in all_names:
            query_obj = self._get_query_object(query_type)
            if query_obj.is_enabled():
                details[query_type] = self.get_query(query_type)
        return details

    @set_speed(0, 'gui')
    def is_query_enabled(self, query_type):
        """Return particular LDAP query state in profile

        *Parameters:*
        - `query_type`: type of LDAP query whose status will be gotten

        *Return*
        True if enabled or False otherwise
        """
        dest_query = self._get_query_object(query_type)
        return dest_query.is_enabled()

    @set_speed(0, 'gui')
    def set_query_state(self, query_type, state):
        """Set state of a particular LDAP Query in profile

        *Parameters:*
        - `query_type`: type of LDAP query whose status will be set
        - `state`: new query state. Either ${True} or ${False}
        """
        dest_query = self._get_query_object(query_type)
        if state:
            dest_query.enable()
        else:
            dest_query.disable()

    @set_speed(0, 'gui')
    def get_query_test_result(self, query_type, settings):
        dest_query = self._get_query_object(query_type)
        return dest_query.get_test_result(settings)


class LDAPServerAttributesHolder(InputsOwner):
    PROFILE_NAME = ('LDAP Server Profile Name',
                    "//input[@id='LDAPServerName']")
    HOST_NAME = ('Host Name',
                 "//input[@name='hostname']")
    BASE_DN = ('Base DN',
               "//input[@name='base']")
    AUTH_METHOD_RADIO_GROUP = ('Authentication Method',
                               {'Anonymous': "//input[@id='authtype_anon']",
                                'Use Password': "//input[@id='authtype_pass']"})
    USERNAME = ('Username',
                "//input[@id='auth_user']")
    PASSWD = ('Password',
              "//input[@id='auth_pass']")
    SERVER_TYPE_COMBO = ('Server Type',
                   "//select[@id='server_type']")
    PORT = ('Port',
            "//input[@id='port']")
    CONN_PROTO_CHECKBOX = ('Connection Protocol',
                           "//input[@id='use_ssl']")
    CACHE_TTL = ('Cache TTL',
                 "//input[@id='cache_ttl']")
    CACHE_SIZE = ('Maximum Retained Cache Entries',
                  "//input[@id='cache_size']")
    MAX_CONNECTIONS = ('Maximum Number of Simultaneous '\
                       'Connections for Each Host',
                       "//input[@name='max_connections']")
    MULTI_HOST_OPTIONS_RADIO_GROUP = ('Multiple Host Options',
            {'Load-Balance Connections Among All Hosts Listed': \
                "//input[@id='load_balance']",
             'Failover Connections in the Order Listed':
                "//input[@id='failover']"})

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def get(self):
        raise NotImplementedError()

    @set_speed(0, 'gui')
    def set(self, new_value):
        """Set LDAP profile settings

        *Parameters:*
        - `new_value`: dictionary, whose keys are human-
        readable setting names and values are their values
        to set

        *Exceptions:*
        - `ValueError`: if incorrect value is passed to some
        setting
        """
        self._set_radio_groups(new_value,
                               self.AUTH_METHOD_RADIO_GROUP,
                               self.MULTI_HOST_OPTIONS_RADIO_GROUP)
        self._set_combos(new_value, self.SERVER_TYPE_COMBO)
        self._set_checkboxes(new_value, self.CONN_PROTO_CHECKBOX)
        self._set_edits(new_value,
                        self.PROFILE_NAME,
                        self.BASE_DN,
                        self.HOST_NAME,
                        self.PORT,
                        self.CACHE_TTL,
                        self.CACHE_SIZE,
                        self.MAX_CONNECTIONS,
                        self.USERNAME,
                        self.PASSWD)


class LDAPProfile(object):
    def __init__(self, gui_common):
        self.gui = gui_common
        self._queries_holder = LDAPQueriesHolder(gui_common)
        self._settings_holder = LDAPServerAttributesHolder(gui_common)

    def set(self, new_settings, new_queries):
        """Set LDAP profile settings

        *Parameters:*
        - `new_settings`: dictionary with LDAP server profile settings
        - `new_queries`: dictionary containing settings for profile queries

        *Exceptions:*
        - `ValueError`: if any of passed values is incorrect
        """
        self._settings_holder.set(new_settings)
        self._queries_holder.set_queries(new_queries)

    def get(self):
        """Get LDAP profile details

        *Return:*
        Dictionary whose keys are corresponding profile setting names
        and values are their values
        Also, this dictionary has special key `Queries`, which contains
        dictionary value with all query parameters in this particular
        profile
        """
        details = {}
        details['Queries'] = self._queries_holder.get_queries()
        details.update(self._settings_holder.get())
        return details

    def get_test_result(self):
        """Return profile testing result

        *Exceptions:*
        - `TimeoutError`: if testing was not finished within
        predefined timeout

        *Return:*
        Profile testing result text
        """
        TEST_FINISHED_MARK = 'Result:'
        TIMEOUT = 60
        self.gui.click_button(TEST_SERVER_BTN, 'don\'t wait')
        self.gui.wait_until_page_contains(TEST_FINISHED_MARK, TIMEOUT)
        result = self.gui.get_text(TEST_RESULTS_DIV)
        self.gui.go_to(self.gui.get_location())
        return result

    def get_query_test_result(self, query_type, settings):
        return self._queries_holder.get_query_test_result(query_type, settings)

