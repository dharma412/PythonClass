#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/smbiosparser.py#1 $

# python imports
import os
import re

# sarf imports
from common.util.utilcommon import UtilCommon


class SmbiosParser(UtilCommon):
    """
    Implement keywords for retreiving info from smbios command
    """

    def __init__(self, *args, **kwargs):
        UtilCommon.__init__(self, *args, **kwargs)
        self._smbios_verbose = None
        self._smbios_a = None
        self._dmesg = None
        self._smbios_exe = None

    # TODO: get rid of serial_number and incorporate
    #       into get_smbios_info - need modify ipcheck 
    #       test case
    def get_keyword_names(self):
        return [
            'get_smbios_memory_info',
            'get_smbios_pci_info',
            'get_smbios_platform_info',
            'get_smbios_cpu_info',
            'get_bios_version_info',
            'get_smbios_serial_number',
            'get_smbios_info',
            'get_smbios_complete_info',
        ]

    def get_smbios_complete_info(self, blockName, select=None):
        """
        Returns the blockName info block from smbios -v command
        as a list

        Example:
        | ${completBiosInfo}= | Get Smbios Complete Info | BIOS Information
        """
        self._get_smbios_verbose()

        return self._smbios_query(blockName, select)

    def get_smbios_info(self, attribute):
        """
        Parse out the "attribute" value from smbios -a

        Example:
        | ${managementInterface}= | Get Smbios Info | ManagementInterface |

        Returns <value> from the line
            "ManagementInterface=<value>"
        """
        self._get_smbios_a()
        smbios_re = re.compile('^%s="(.+)"$' % (attribute))
        for line in self._smbios_a:
            match = smbios_re.match(line)
            if match:
                value = match.group(1)

        if not value:
            value = "NA"

        return value

    def get_smbios_serial_number(self):
        """
        Parse out the IronPortSerial Number from smbios -a command

        Example:
        | ${serialNumberInfo}= | Get Smbios Serial Number |

        Returns string of the form:
            Serial No.:<serial number>
        """
        self._get_smbios_a()
        serialNumer = 'NA'
        for line in self._smbios_a:
            m = re.match('IronPortSerial="(.*)"', line)
            if m:
                serialNumber = m.group(1)
        return 'Serial No\.:%s' % (serialNumber)

    def get_bios_version_info(self):
        """
        Parse out the bios verion info from dmesg on dell
        platforms and from smbios -a from other platforms

        Example:
        | ${biosVersionInfo}= | Get Bios Version Info |

        Returns a string of the form:
            "BIOS Version:<version>"
        """
        self._get_dmesg()
        bios_version_re = re.compile("dell_bios0: Version (.*)")
        manufacturer_bios_re = re.compile("dell_bios0: Manufacturer (.)")

        bios_version = filter(None, map(lambda line, r=bios_version_re: r.match(line), self._dmesg))
        manufacturer_bios = filter(None, map(lambda line, r=manufacturer_bios_re: r.match(line), self._dmesg))

        if bios_version:
            bios_version = bios_version[0].group(1) + manufacturer_bios[0].group(1)
        else:
            # Not Dell; let's see what the BIOS version is from smbios -a ...
            self._get_smbios_a()
            smbios_biosVersion_re = re.compile('^biosVersion="(.+)"$')
            for line in self._smbios_a:
                match = smbios_biosVersion_re.match(line)
                if match:
                    bios_version = match.group(1)

        if not bios_version:
            bios_version = "NA"

        return "BIOS Version:" + bios_version

    def get_smbios_cpu_info(self):
        """
        Parse out the cpu info from smbios -v command

        Example:
        | ${cpuInfo}= | Get Smbios Cpu Info |

        Returns a multi line string of the form:
            CPU <id>:<cpu details>
        """
        config = ""
        found_cpu = 0
        self._get_smbios_verbose()
        for cpu in range(1, 4):
            for type in ("PROC_", "PROC", "Proc_", "CPU", "CPU "):
                id = "%s%d" % (type, cpu,)
                if self._smbios_cpu(id) != "":
                    config = config + "CPU %d:%s\n" % (cpu, self._smbios_cpu(id))
                    found_cpu = 1
        # strip trailing \n
        config = config[:-1]
        if not found_cpu and self._smbios_cpu("PROC") != "":
            config = config + "CPU 1:%s" % (self._smbios_cpu("PROC"))
        return config

    def get_smbios_platform_info(self):
        """
        Parse out the platform info from smbios -v command

        Example:
        | ${platformInfo}= | Get Smbios Platform Info |

        Returns a string of the form:
            Platform:<platform info>
        """
        self._get_smbios_verbose()
        platform = {}
        platform["802B"] = "PE750"
        platform["8048"] = "PE850"
        platform["8066"] = "PE860"
        platform["808C"] = "cr100"
        platform["8089"] = "r200"
        platform["8014"] = "PE2650"
        platform["8038"] = "PE2850"
        platform["805C"] = "PE2950"
        platform["80AE"] = "r710"
        platform["CARDINAL"] = "cardinal"
        query = self._smbios_query("OEM Strings", "7[")
        if len(query) == 0:
            query = self._smbios_query("System Information", "Product name")
        if len(query) > 0:
            for line in query[0].split("\n"):
                if line.find("7[") != -1:
                    result = re.sub("\].*$", "", re.sub("^.*\[", "", line))
                    if platform.has_key(result):
                        return "Platform:%s \(%s\)" % (platform[result], result)
                    else:
                        return "Platform:Unknown \(%s\)" % (result)
                if line.find("Product name") != -1:
                    result = re.sub("\].*$", "", re.sub("^.*: ", "", line))
                    if platform.has_key(result):
                        return "Platform:%s \(%s\)" % (platform[result], result)
                    else:
                        return "Platform:Unknown \(%s\)" % (result)
        return ""

    def get_smbios_pci_info(self):
        """
        Parse out PCI info from smbios -v command

        Example:
        | ${pciInfo}= | Get Smbios Pci Info |

        Returns a multi line string of the form:
            PCI <id>:<pci info>
        """
        self._get_smbios_verbose()
        config = ""
        for slot in range(1, 7):
            for type in ("PCI", "PCI_", "SLOT_", "SLOT"):
                # look for entry "System Slots"
                id = "%s%d" % (type, slot,)
                if self._smbios_pci(id):
                    config = config + "PCI %d:%s\n" % (slot, self._smbios_pci(id))
        # remove trailing \n
        config = config[:-1]
        return config

    def get_smbios_memory_info(self):
        """
        Parse out memory info from smbios -v command

        Example:
        | ${memoryInfo}= | Get Smbios Memory Info |

        Returns a multi line string of the form:
            RAM <id>:<ram info>
        """
        config = ""
        ram_total = 0
        self._get_smbios_verbose()
        for dimm in range(1, 4):
            for bank in ("A", "B"):
                index = "%s_%s" % (dimm, bank,)
                name = "RAM %s %s" % (dimm, bank,)
                if self._smbios_ram(index) != "":
                    config = config + "%s:%s\n" % (name, self._smbios_ram(index))
                    ram_total = ram_total + self._val_ram(self._smbios_ram(index))
        for dimm in range(1, 4):
            index = "_%s" % (dimm,)
            name = "RAM %s" % (dimm,)
            if self._smbios_ram(index) != "":
                config = config + "$s:%s\n" % (name, self._smbios_ram(index))
                ram_total = ram_total + self._val_ram(self._smbios_ram(index))
        for dimm in range(1, 10):
            found = None
            for bank in ("A", "B", ""):
                if bank != "":
                    index = "_%s%s" % (bank, dimm,)
                    name = "RAM %s %s" % (dimm, bank,)
                else:
                    index = "%s" % (dimm,)
                    name = "RAM %s" % (dimm,)
                if self._smbios_ram(index) != "":
                    if (bank == "" and not found) or bank != "":
                        config = config + "%s:%s\n" % (name, self._smbios_ram(index))
                        ram_total = ram_total + self._val_ram(self._smbios_ram(index))
                    found = 1
        config = config + "RAM Total:%dG" % (float(ram_total) / 1024,)
        return config

    def _get_smbios_path(self):
        """
        Return the path to smbios
        """
        if self._smbios_exe == None:
            findOutput = self._shell.send_cmd("find /data -name smbios", 300)
            if len(findOutput) <= 0:
                self._info("Cannot find smbios executable on DUT")
                raise Execption("Cannot find smbios executable on DUT")
            else:
                lines = findOutput.splitlines()
                self._smbios_exe = lines[0]
                return self._smbios_exe
        else:
            return self._smbios_exe

    def _get_smbios_a(self):
        """
        Run smbios -a on the DUT
        Sets instance variable _smbios_a as a list
        with each entry a line from smbios -a command
        """
        if self._smbios_a == None:
            # execute smbios -a command
            commandToExecute = self._get_smbios_path() + " -a"
            smbios_out = self._shell.send_cmd(commandToExecute)
            self._info("smbios_out = %s\n" % (smbios_out))
            self._smbios_a = smbios_out.splitlines()

    def _get_smbios_verbose(self):
        """
        Run smbios -v command on the DUT
        Sets instance variable _smbios_verbose as a list
        with each entry a line from smbios -v
        """
        if self._smbios_verbose == None:
            # execute smbios -v command
            commandToExecute = self._get_smbios_path() + " -v"
            smbios_out = self._shell.send_cmd(commandToExecute)
            self._info("smbios_out = %s\n" % (smbios_out))
            smbios_temp = smbios_out.splitlines()
            self._smbios_verbose = []
            for line in smbios_temp:
                if line.find("DIMM") != -1:
                    self._smbios_verbose.append(line + " ")
                else:
                    self._smbios_verbose.append(line)

    def _get_dmesg(self):
        """
        Run dmesg on the DUT
        Sets instance variable _dmesg as a list with
        each entry a line in dmesg command
        """
        if self._dmesg == None:
            dmesgOut = self._shell.send_cmd('dmesg')
            self._dmesg = dmesgOut.splitlines()

    def _smbios_query(self, type, other=None):
        """
        Return a type structure block from SMBIOS.

        :Parameters:
            - `type`:  A string corresponding to the appropriate SMBIOS type
                       structure block which needs to be parsed.
            - `other`: A distinguishing value within the block to use when
                       determining one reoccurring SMBIOS type from another. This
                       doesn't filter out keys in the type structure block.

        :Returns:
            A list of raw smbios type structure blocks specified by `type`,
            filtered according to `other`, if specified, or an empty list if no
            corresponding blocks are found.
        """
        block = ""
        returned = []
        for line in self._smbios_verbose:
            line = re.sub("\n", '', line)
            if re.match("^Type \d+:", line) != None:
                if block.find(type) != -1:
                    if not other or block.find(other) != -1:
                        block = block[0:-1]
                        returned.append(block)
                block = ""
            block = block + line + "\n"
        return returned

    def _find_it(self, string, find):
        """
        Find "find" in the given string
        """
        found = string.find(find)
        if found > 0:
            string = string[found + len(find):]
            string = re.sub("\n.*", '', string)
            return string
        else:
            return None

    def _smbios_ram(self, select):
        """
        Parse out memory information from smbios -v command
        """
        size = "NA"
        ecc = "NA"
        speed = "NA"
        query = self._smbios_query("Memory Device", "DIMM" + select + " ")
        if len(query):
            query = query[0]
            size = self._find_it(query, "Size: ")
            width = self._find_it(query, "Data width: ")
            ecc_width = self._find_it(query, "Total width: ")
            speed = self._find_it(query, "Speed: ")
            if width == ecc_width:
                ecc = "No ECC"
            elif width < ecc_width:
                ecc = "ECC"
            if size == str(0):
                return "Empty"
            else:
                return "%sM %s %sMHz" % (size, ecc, speed)
        else:
            return ""

    def _val_ram(self, info):
        temp = re.sub("M.*", '', info)
        try:
            return int(temp)
        except:
            return 0;

    def _smbios_pci(self, select):
        """
        Parse out the pci info from smbios -v command
        """
        status = "Empty"
        query = self._smbios_query("System Slots", select)
        if len(query):
            type = self._find_it(query[0], "type: ")
            bits = self._find_it(query[0], "width: ")
            if query[0].find("Available") > -1:
                return type + " " + bits + " Empty"
            else:
                return type + " " + bits + " Installed"
        else:
            return ""

    def _smbios_cpu(self, select):
        """
        Parse out the cpu information from smbios -v command
        """
        type = "NA"
        speed = "NA"
        fsb = "NA"
        cache = "NA"
        version = None
        query = self._smbios_query("Processor", select)
        if len(query):
            query = query[0]
            type = self._find_it(query, "family: ")
            version = self._find_it(query, "Version: ")
            # PE850 and PE860 also return version strings in addition to PE2950
            # and replacing the type with parsed string witll fail the ipcheck
            # and bom_check for C150 and C10, so, handling only the Xeon family
            # for now.
            if version is not None and type == "Xeon":
                # sample : Intel(R) Pentium(R) Dual CPU E2200 @ 2.20GHz
                # sample : Intel(R) Xeon(R) CPU    X5355 @ 2.66GHz
                version_tokens = version.split()
                idx = 0
                typev = ""
                while True:
                    if idx != 0 and version_tokens[idx] != "CPU":
                        typev = typev + re.sub("\(R\)", "", version_tokens[idx]) + " "
                    elif idx != 0:
                        break
                    else:
                        pass
                    idx += 1
                    if idx >= len(version_tokens):
                        typev = ""
                        break
                if typev != "":
                    typev = typev.strip()
                    type = typev
            speed = float(self._find_it(query, "Current speed: ")) / 1000
            fsb = self._find_it(query, "clock: ")

            handle = self._find_it(query, "L2 Cache handle: ")
            query = self._smbios_query("\thandle: %s" % (handle,))[0]
            cache = float(self._find_it(query, "Installed cache size: ")) / 1024

            if speed == 0:
                return "Empty"
            else:
                return re.sub("\.0", "", "%s %sG %sFSB %sM Cache" % (type, speed, fsb, cache))
        else:
            return ""
