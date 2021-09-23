#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/version.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

"""
IAF Command Line Interface (CLI)

command:
    - version
"""
import clictorbase

class PhoebeVersion(object):
    """
       Represents a phoebe version. Has attributes 'model, 'version',
       'build_date', 'install_date', 'serial', 'bios', 'raid', 'raid_status',
       'raid_type', and 'bmc'
    """
    def __init__(self, verstring=None):
        self.model = None
        self.version = None
        self.build_date = None
        self.install_date = None
        self.serial = None
        self.bios = None
        self.raid = None
        self.raid_status = None
        self.raid_type = None
        self.bmc = ''
        if verstring:
            self.parse(verstring)

    def __str__(self):
        return "Current Version\n===============" \
            "\nModel %s" \
            "\nVersion: %s" \
            "\nBuild Date: %s" \
            "\nInstall Date %s" \
            "\nSerial #: %s" \
            "\nBIOS: %s" \
            "\nRAID: %s" \
            "\nRAID Status: %s" \
            "\nRAID Type: %s" \
            "\nBMC: %s\n" % \
            (self.model,
             self.version,
             self.build_date,
             self.install_date,
             self.serial,
             self.bios,
             self.raid,
             self.raid_status,
             self.raid_type,
             self.bmc)

    def update(self, ctor):
        bs = ctor.version_string()
        self.parse(bs)

    def parse(self, bs):
        """ Parse some text (bs) into a
        -model
        -version
        -build_date
        -install_date
        -serial
        -bios
        -raid
        -raid_status
        -raid_type
        -bmc
        """
        lines = bs.split("\n")
        for line in lines:
            if line.startswith("Model"):
                self.model = line.split()[1].strip()
            elif line.startswith("Version"):
                self.version = self._split_line(line)
            elif line.startswith("Build"):
                self.build_date = self._split_line(line)
            elif line.startswith("Install"):
                self.install_date = self._split_line(line)
            elif line.startswith("Serial"):
                self.serial = self._split_line(line)
            elif line.startswith("BIOS"):
                self.bios = self._split_line(line)
            elif line.startswith("RAID:"):
                self.raid = self._split_line(line)
            elif line.startswith("RAID Status"):
                self.raid_status = self._split_line(line)
            elif line.startswith("RAID Type"):
                self.raid_type = self._split_line(line)
            elif line.startswith("BMC"):
                self.bmc = self._split_line(line)

    def set_from_config(self, config):
        """ Instead of parsing, set these basic attributes by fetching them from
            the config.
        """
        self.model = config.DUT.model()
        build_id = BUILD_ID.get(config.software_version)
        [ph, major, minor, subminor] = build_id.split("-")
        self.version = "%s.%s.%s-unknown" % (major, minor, subminor)
        self.build_date = None
        self.serial = None

    def __eq__(self, other):
        i = self.version.find("-")
        return self.model == other.model and self.version[:i] == other.version[:i]

    def __ne__(self, other):
        return not self.__eq__(other)

    def _split_line(self, line):
        return line.split(":",1)[1].strip()

class version(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln(self.__class__.__name__)
        raw = ''
        tries = 1
        # look for prompt up to five times
        # if we can't find the version the first time
        while raw.lower().find('current version') == -1 and tries <= 5:
            self.clearbuf()
            raw = self._sess.read_until()
            tries += 1

        # attempt to parse and return version data
        return PhoebeVersion(raw)

if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess object is present in namespace, we're using
    # the dev unit test harness, don't get a new one
    # also set valid gateway address to eng env if present, qa if not
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = version(cli_sess)
    # test case
    print cli()
