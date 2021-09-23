#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/antivirusconfig.py#1 $


"""
    IAF 2 CLI ctor - antivirusconfig
"""

import clictorbase as ccb
from sal.containers.yesnodefault import YES, NO

DEFAULT = ccb.DEFAULT
DEBUG = True
REQUIRED = ccb.REQUIRED


class antivirusconfig(ccb.IafCliConfiguratorBase):
    """antivirusconfig
        - will return -1 when there's no Sophos feature key
    """
    _vendors = ('sophos', 'mcafee')

    def __call__(self, vendor='sophos'):
        """Parameters:
             vendor - an allowed AV vendor or 'Tune'
                      to use the undocumented TUNE menu command
        """

        if vendor == None or vendor.lower() == 'tune':
            self._writeln('antivirusconfig')
            self._expect(['requires activation', 'Choose the operation'])
            if self._expectindex == 0:
                return -1
            return self

        vendor = vendor.lower()
        if not vendor in self._vendors:
            raise ccb.IafCliError('Illegal vendor: %s. Allowed vendors: %s'
                                  % (vendor, ', '.join(self._vendors)))

        self.clearbuf()
        self._writeln('antivirusconfig')
        self._expect(['requires activation', 'Choose the operation'])
        lines = self.getbuf()
        if self._expectindex == 0:
            return -1
        if self._expectindex == 1:
            if lines.find('Anti-Virus:') == -1:
                self._query_response(vendor)
                # import handlecluster
                # handlecluster.handle_cluster_questions(self._get_sess())
                lines = self._read_until('Anti-Virus:')

            if lines.find('Sophos') >= 0 and vendor == 'sophos':
                return antivirusconfigSophos(self._get_sess())
            elif lines.find('McAfee') >= 0 and vendor == 'mcafee':
                return antivirusconfigMcAfee(self._get_sess())
            else:
                raise ccb.IafCliError('Feature is not activated. Please make ' \
                                      'sure that featurekey is valid and the feature is bundled')

    def tune(self, input_dict=None, **kwargs):
        """ Global Tune option.
        """
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['conf'] = ['server performance tuning',
                             DEFAULT, True]
        param_map['num_msg'] = ['number of messages', DEFAULT]
        param_map['traffic'] = ['Limit traffic', DEFAULT]
        param_map['rescan'] = ['Rescan messages', DEFAULT]
        param_map['num_retries'] = ['Number of retries', DEFAULT]
        param_map['sleep_time'] = ['Time to sleep', DEFAULT]
        param_map['num_obj'] = ['scanning objects', DEFAULT]
        param_map['scan_policy'] = ['server scanning policy', DEFAULT, True]
        param_map.update(input_dict or kwargs)

        self._query_response('TUNE')
        self._process_input(param_map)


class antivirusconfigSophos(ccb.IafCliConfiguratorBase):
    """antivirusconfig -> Sophos """

    _newline = 1

    def setup(self, input_dict=None, **kwargs):
        """
        Sophos Antivirus setup
        Parameters:
            use_av - enable Antivirus: [YES or NO]
            scan_timeout - scanning timeout [int]
            confirm_disable - confirm whether disable Antivirus [YES or NO]
            license_agreement - confirm licence agreement [YES or NO]
        """
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_av'] = ['to use Sophos', YES]
        param_map['scan_timeout'] = ['scanning timeout', DEFAULT]
        param_map['confirm_disable'] = ['want to disable', YES]
        param_map['license_agreement'] = ['license agreement?', YES]
        param_map['enable_automatic_updates'] = ['enable automatic updates for Sophos', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        self._process_input(param_map)

    def tune(self, input_dict=None, **kwargs):
        """ Sophos-specific hidden Tune option.
        """
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['conf'] = ['server performance tuning',
                             DEFAULT, True]
        param_map['num_msg'] = ['number of messages', DEFAULT]
        param_map['traffic'] = ['Limit traffic', DEFAULT]
        param_map['rescan'] = ['Rescan messages', DEFAULT]
        param_map['num_retries'] = ['Number of retries', DEFAULT]
        param_map['sleep_time'] = ['Time to sleep', DEFAULT]
        param_map['num_obj'] = ['scanning objects', DEFAULT]
        param_map['scan_policy'] = ['server scanning policy', DEFAULT, True]
        param_map['attachment_depth'] = ['maximum depth of attachment', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('TUNE')
        self._process_input(param_map)

    def pdf(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['report_clean'] = ['unscannable PDFs as clean', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('PDF')
        self._process_input(param_map, timeout=10)

    def clusterset(self):
        raise ccb.IafCliCtorNotImplementedError

    def clustershow(self):
        raise ccb.IafCliCtorNotImplementedError


class antivirusconfigMcAfee(ccb.IafCliConfiguratorBase):
    """antivirusconfig -> Sophos """

    _newline = 1

    def setup(self, input_dict=None, **kwargs):
        """
        Sophos Antivirus setup
        Parameters:
            use_av - enable Antivirus: [YES or NO]
            check_update - period of checking for new virus definitions [int]
            confirm_disable - confirm whether disable Antivirus [YES or NO]
            license_agreement - confirm licence agreement [YES or NO]
        """
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['use_av'] = ['to use McAfee', YES]
        param_map['scan_timeout'] = ['scanning timeout', DEFAULT]
        param_map['confirm_disable'] = ['want to disable', YES]
        param_map['license_agreement'] = ['license agreement?', YES]
        param_map['enable_automatic_updates'] = ['enable automatic updates for McAfee', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        self._process_input(param_map)

    def clusterset(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Settings')
        param_map['action'] = ['can copy the current settings', REQUIRED,
                               True]
        param_map['group_copy'] = ['group name or number to copy', DEFAULT]
        param_map['machine_copy'] = ['machine name or number to copy',
                                     DEFAULT]
        param_map['cluster_copy'] = ['cluster name or number to copy',
                                     DEFAULT]
        param_map['group_move'] = ['group name or number to move',
                                   DEFAULT]
        param_map['machine_move'] = ['machine name or number to move',
                                     DEFAULT]
        param_map['cluster_move'] = ['cluster name or number to move',
                                     DEFAULT]
        param_map['delete_cluster'] = ['from the cluster', DEFAULT]
        param_map['delete_group'] = ['from the Group', DEFAULT]
        param_map['delete_machine'] = ['from the machine', DEFAULT]
        param_map['force'] = ['you sure you want to continue', DEFAULT]

        param_map.update(input_dict or kwargs)

        self._query_response('CLUSTERSET')
        return self._process_input(param_map)

    def clustershow(self):
        self._query_response('CLUSTERSHOW')
        raw = self._read_until('Choose the operation')
        self._to_the_top(2)
        return raw


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    avc = antivirusconfig(cli_sess)

    try:
        avc(vendor='sophos').setup(use_av=YES)
        avc(vendor='sophos').tune()
        # Blocker specific unit test
        avc(vendor='sophos').tune(conf='custom', num_msg=10, traffic=29360129, rescan='Y', \
                                  num_retries=3, sleep_time=30, num_obj=6, scan_policy='Aggressive')
        avc(vendor='sophos').pdf()
        avc(vendor='sophos').setup(use_av=NO)
        avc(vendor='sophos').setup(use_av=YES)
    except ccb.IafCliError:  # feature not activated, just ignore
        print "Skipping Sophos unit tests as Sophos is not enabled."
        cli_sess.interrupt_writeln()
        cli_sess.wait_for_prompt()

    try:
        avc(vendor='mcafee').setup(use_av=YES)
        avc(vendor='mcafee').setup(use_av=NO)
        avc(vendor='mcafee').setup(use_av=YES)
        # Set global Tune option (Not available if Mcafee is disabled
        avc(vendor='tune').tune(conf='Default')
        avc(vendor=None).tune(conf='custom', num_msg=6, rescan=YES)
    except ccb.IafCliError:  # feature not activated, just ignore
        print "Skipping Mcafee unit tests as Mcafee is not enabled."
        cli_sess.interrupt_writeln()
        cli_sess.wait_for_prompt()

    # Set global Tune option
    avc(vendor=None).tune(conf='default')
    avc(vendor=None).tune(conf='custom', num_msg=10, traffic=29360129, rescan='Y')
    # Blocker specific unit test
    avc(vendor=None).tune(conf='custom', num_msg=10, traffic=29360129, rescan='Y', \
                          num_retries=3, sleep_time=30, num_obj=6, scan_policy='Aggressive')
    # Set Sophos-specific Tune option
    avc().tune(num_obj=5, scan_policy='default')
