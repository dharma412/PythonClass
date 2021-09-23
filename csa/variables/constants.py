#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/variables/constants.py#2 $
# $DateTime: 2019/06/03 22:56:07 $
# $Author: revlaksh $

class webcats(object):
    """ Defines common Web Categories """
    #Ironport Engine
    ADULT = 'Adult'
    ADULT_SEX = 'Adult/Sexually Explicit'
    ADVERTISE = 'Advertisements'
    ADVERTISEMENTS = 'Advertisements & Popups'
    ALCOHOL = 'Alcohol & Tobacco'
    ARTS = 'Arts'
    ASTROLOGY = 'Astrology'
    BUSINESS = 'Business'
    CELL = 'Mobile Phones'
    CHAT = 'Chat and Instant Messaging'
    CHEAT = 'Cheating and Plagiarism'
    CHILD_PORN = 'Child Porn'
    COMPUTER_SEC = 'Computer Security'
    COMPUTING = 'Computing & Internet'
    CRIMINAL = 'Criminal Activity'
    CULTS = 'Cults'
    DATE = 'Dating'
    DATING = 'Personals & Dating'
    DINE = 'Dining and Drinking'
    DINING = 'Food & Dining'
    DRUGS = 'Illegal Drugs'
    EDUCATION = 'Education'
    ENTERTAINMENT = 'Entertainment'
    EXTREME = 'Extreme'
    FILE_TRANSFER = 'Downloads'
    FILE_XFER = 'File Transfer Services'
    FILTER = 'Filter Avoidance'
    FASHION = 'Fashion & Beauty'
    FINANCE = 'Finance & Investment'
    FORUMS = 'Blogs & Forums'
    FREEWARE = 'Freeware and Shareware'
    GAMBLING = 'Gambling'
    GAMES = 'Games'
    GOVERNMENT = 'Government'
    GOVT_LAW = 'Government and Law'
    HACKING = 'Hacking'
    HATE = 'Intolerance & Hate'
    HATE_SPCH = 'Hate Speech'
    HEALTH = 'Health & Medicine'
    HLTH_NUTR = 'Health and Nutrition'
    HOBBY = 'Hobbies & Recreation'
    ILLEGAL_ACT = 'Illegal Activities'
    INFRA = 'Infrastructure'
    IM = 'Instant Messaging'
    JOB = 'Job Search & Career Development'
    JOB_SRCH = 'Job Search'
    KIDS_SAFE = 'Kids Sites'
    LINGERIE = 'Intimate Apparel & Swimwear'
    LINGERIE_SWIM = 'Lingerie and Swimsuits'
    LOTTERY = 'Lottery and Sweepstakes'
    MOBILE = 'Ringtones/Mobile Phone Downloads'
    NATURE = 'Nature'
    NEWS = 'News'
    NONSEX_NUDE = 'Non-sexual Nudity'
    OFFENCE = 'Tasteless & Offensive'
    ONLINE_COMM = 'Online Communities'
    ONLINE_TRADE = 'Online Trading'
    ONLINE_STOR = 'Online Storage and Backup'
    ORGANIZATION = 'Philanthropic & Professional Orgs.'
    P2P = 'Peer-to-Peer'
    PEER_FILE_XFER = 'Peer File Transfer'
    PARANORMAL = 'Paranormal and Occult'
    PHOTO_SEARCH = 'Photo Searches'
    POLITICS = 'Politics'
    PORN = 'Porn'
    PROXY = 'Proxies & Translators'
    REAL_ESTATE = 'Real Estate'
    REFERENCE = 'Reference'
    RELIGION = 'Religion'
    SAFE_KIDS = 'Safe for Kids'
    SEARCH = 'Search Engines'
    SEARCH_PORT = 'Search Engines and Portals'
    SEX_EDU = 'Sex Education'
    SEX_EDU_ABORT = 'Sex Ed and Abortion'
    SCIENCE = 'Science and Technology'
    SHOPPING = 'Shopping'
    SOCIAL = 'Society & Culture'
    SOCIAL_NET = 'Social Networking'
    SOCIAL_SCI = 'Social Science'
    SOCIETY = 'Society and Culture'
    SOFTWARE_UP = 'Software Updates'
    SPIRITUAL = 'Spiritual Healing'
    SPORT = 'Sports'
    SPORT_REC = 'Sports and Recreation'
    STREAMING = 'Streaming Media'
    TASTELESS = 'Tasteless or Obscene'
    TATTOOS = 'Tattoos'
    TRANSPORTATION = 'Transportation'
    THREAT_CONTENT = 'Suspect/Threat URLs'
    TRAVEL = 'Travel'
    VEHICLES = 'Motor Vehicles'
    VIOLENCE = 'Violence'
    VOIP = 'Internet Telephony'
    WEAPONS = 'Weapons'
    WEBHOSTING = 'Hosting Sites'
    WEBHOST = 'Web Hosting'
    WEBCHAT = 'Web-based Chat'
    WEBPAGE = 'Web Page Translation'
    WEBMAIL = 'Web-based E-mail'
    WEBEMAIL = 'Web-based Email'

    # Cisco Web Controls
    IW_ADLT = 'Adult' # 1006
    IW_ADV = 'Advertisements' # 1027
    IW_AT = 'Alcohol and Tobacco' # 1048
    IW_AL = 'Alcohol' # 1077
    IW_AUC = 'Auctions' # 1088
    IW_TO = 'Tobacco' # 1078
    IW_ART = 'Arts and Entertainment' # 1002
    IW_BUSI = 'Business and Industry' # 1019
    IW_PLAG = 'Cheating and Plagiarism' # 1051
    IW_CPRN = 'Child Porn' # 1064
    IW_CSEC = 'Computer Security' # 1065
    IW_COMP = 'Computers and Internet' # 1003
    IW_CULT = 'Cults' # 1041
    IW_DATE = 'Dating' # 1055
    IW_DP = 'Digital Postcards' # 1082
    IW_DRE = 'Dynamic and Residential' # 1091
    IW_FOOD = 'Dining and Drinking' # 1061
    IW_EDU = 'Education' # 1001
    IW_FASH = 'Fashion' # 1076
    IW_FTS = 'File Transfer Services' # 1023
    IW_FILT = 'Filter Avoidance' # 1025
    IW_FNNC = 'Finance' # 1015
    IW_FREE = 'Freeware and Shareware' # 1068
    IW_GAMB = 'Gambling' # 1049
    IW_GAME = 'Games' # 1007
    IW_GOV = 'Government and Law' # 1011
    IW_HACK = 'Hacking' # 1050
    IW_HATE = 'Hate Speech' # 1016
    IW_HLTH = 'Health and Nutrition' # 1009
    IW_HUM = 'Humor'
    IW_ILAC = 'Illegal Activities' # 1022
    IW_ID = 'Illegal Downloads'
    IW_DRUG = 'Illegal Drugs' # 1047
    IW_INFR = 'Infrastructure' # 1018
    IW_IM = 'Instant Messaging' # 1039
    IW_VOIP = 'Internet Telephony' # 1067
    IW_JOB = 'Job Search' # 1004
    IW_LING = 'Lingerie and Swimsuits' # 1031
    IW_LOTR = 'Lottery and Sweepstakes' # 1034
    IW_CELL = 'Mobile Phones' # 1070
    IW_NATR = 'Nature' # 1013
    IW_NEWS = 'News' # 1058
    IW_NGO = 'Non-governmental Organizations' # 1087
    IW_NSN = 'Non-sexual Nudity' # 1060
    IW_COMM = 'Online Communities' # 1024
    IW_OSB = 'Online Storage and Backup' # 1066
    IW_TRAD = 'Online Trading' # 1028
    IW_OREM ='Organizational Email' # 1085
    IW_PARA = 'Paranormal and Occult' # 1029
    IW_PADO = 'Parked Domains' # 1092
    IW_P2P = 'Peer File Transfer' # 1056
    IW_PS = 'Personal Sites'
    IW_PORN = 'Porn' # 1054
    IW_PNET ='Professional Networking' #1089
    IW_PSI = 'Photo Search and Images' # 1090
    IW_REST = 'Real Estate' # 1045
    IW_REF = 'Reference' # 1017
    IW_KIDS = 'Safe for Kids' # 1057
    IW_SAB2 = 'SaaS and B2B'
    IW_SCI = 'Science and Technology' # 1012
    IW_SRCH = 'Search Engines and Portals' # 1020
    IW_SXED = 'Sex Ed and Abortion' # 1052
    IW_SHOP = 'Shopping' # 1005
    IW_SNET = 'Social Networking' # 1069
    IW_SOCS = 'Social Science' # 1014
    IW_SCTY = 'Society and Culture' # 1010
    IW_SWUP = 'Software Updates' # 1053
    IW_HEAL = 'Spiritual Healing' # 1042
    IW_SPRT = 'Sports and Recreation' # 1008
    IW_MDIA = 'Streaming Media' # 1026
    IW_VID = 'Streaming Video'
    IW_AUD = 'Streaming Audio'
    IW_OBS = 'Tasteless or Obscene' # 1033
    IW_TAT = 'Tattoos' # 1043
    IW_TRNS = 'Transportation' # 1044
    IW_TRVL = 'Travel' # 1046
    IW_VIOL = 'Violence' # 1032
    IW_WEAP = 'Weapons' # 1036
    IW_WHST = 'Web Hosting' # 1037
    IW_TRAN = 'Web Page Translation' # 1063
    IW_CHAT = 'Web-based Chat' # 1040
    IW_MAIL = 'Web-based Email' # 1038
    IW_RELIG = 'Religion' # 1086
    UNCATEGORIZED = 'Uncategorized URLs'

class mwcats(object):
    """ Defined recognized malware categories """
    ADWARE = 'Adware'
    ADDONS = 'Browser Helper Object'
    COMM_SYSMON = 'Commercial System Monitor'
    DIALER = 'Dialer'
    SPYWARE = 'Generic Spyware'
    HIJACKER = 'Hijacker'
    OTHER = 'Other Malware'
    PHISHING_URL = 'Phishing URL'
    PUA = 'PUA'
    SYSMON = 'System Monitor'
    DOWNLOADER = 'Trojan Downloader'
    TROJAN = 'Trojan Horse'
    PHISHER = 'Trojan Phisher'
    VIRUS = 'Virus'
    WORM = 'Worm'
    ENCRYPTED = 'Encrypted File'
    UNSCANNABLE = 'Unscannable'
    HEURISTICS = 'Outbreak Heuristics'
# Following malware categories are deprecated for coeus75
#    UNKNOWN = 'Unknown'
#    NOT_SCANNED = 'Not Scanned'
#    TIMEOUT = 'Timeout'
#    OVERFLOWS = 'Freelist Exhaustion'
    SUA = 'Suspect User Agents'
#Added to select all Malware and other categories to block
    ALLMALWARE = 'All Malware'
    ALLOTHERMALWARE = 'Other Categories'

class mwthreats(object):
    """ Defined recognized malware threats """
    W32_DUMARU = 'W32/Dumaru.w.gen'

class catsites(object):
    """Define the sites for testing the categories"""
    AUCTIONS = 'http://www.ebay.com'
    APPLE = 'http://www.apple.com'
    AUDIO = 'http://www.shoutcast.com'
    ALCO = 'http://www.samueladams.com'
    ASTRO = 'http://www.astro.com'
    BADREP = 'http://ihaveabadreputation.com'
    BADSITE = 'http://badsite.com'
    CHAT = 'http://www.yesichat.com'
    DYNAM_RESID = 'http://dynalink.co.jp'
    ENTERTAINMENT = 'http://www.eonline.com'
    EXTREME = 'http://www.cadaver.org'
    FASHION = 'http://www.fashion.net'
    FASHION2 = 'http://www.bowiesalonandspa.com'
    ILLEGAL_DOWNLOADS = 'http://www.dvdup2u.com'
    HUMOR = 'http://www.jokes.com'
    ART = 'http://kidrock.com'
    NONGOVERORG = 'http://westviewfuneralchapel.com'
    PARANORMAL = 'http://www.tarot.com'
    PARKEDDOMS = 'http://www.parked.com'
    PERSONAL = 'http://www.danieldiges.com'
    PHOTO = 'http://www.flickr.com'
    POLITICS = 'http://www.politics.com'
    POSTCARDS = 'http://www.all-yours.net'
    RELIGION1 = 'http://www.ahimsa.ru'
    RELIGION2 = 'http://www.religionfacts.com'
    RELIGION3 = 'http://www.voodoo.de'
    SAAS = 'http://www.salesforce.com'
    SEARCH1 = 'http://google.com'
    SEARCH2 = 'http://badsite.com'
    SHOPPING = 'http://www.amazon.com'
    SOCIAL_NET1 = 'http://www.linkedin.com'
    SOCIAL_NET2 = 'https://www.facebook.com'
    SOCIAL_NET3 = 'http://www.twitter.com'
    TATOO = 'http://www.studiotattoo.gr'
    TOBACCO = 'http://www.tobacco.org'
    VIDEO  = 'http://www.youtube.com'
    VIOLANCE = 'http://www.realfights.com'
    WIKIEDIT = 'http://en.wikipedia.org/w/index.php?title=Software_testing\\&action=edit'
    HEAL = 'dancing-bear.com'

class sites(object):
    """external sites needed for testing"""
    IPV6G = 'ipv6.google.com'
    IPV6CISCO = 'ipv6.cisco.com'
    IPV6GOOGLE = 'ipv6.google.com'
    IPV6 = 'ipv6.google.com'
    CISCO = 'www.cisco.com'
    GMAIL = 'gmail.com'
    MUS_CISCO='mus.cisco.com'
    IPV6CNN = 'ipv6.cnn.com'
    IPV6_CISCO = 'ipv6.cisco.com'
    GOOGLE = 'www.google.com'
    SALEFORCE = 'https://saml.salesforce.com'
    WIKI = 'www.wikipedia.org'
    SERVICES = 'http://services.wga'

class apps(object):
    YOUTUBE = 'YouTube'
    WIKI = 'Wikipedia'

class app_types(object):
    MEDIA = 'Media'
    COLABOR = 'Collaboration'

class useragents(object):
    """ Defined custom user agents """
    MSIE11 = 'MSIE11'
    MSIE10 = 'MSIE10'
    MSIE9 = 'MSIE9'
    MSIE8 = 'MSIE8'
    MSIE7 = 'MSIE7'
    MSIE6 = 'MSIE6'
    MSIE5 = 'MSIE5'
    MSIE = 'MSIE'
    FF3 = 'Firefox/3'
    FF2 = 'Firefox/2'
    FF1 = 'Firefox/1'
    FF43 = 'Firefox/43'
    FF42 = 'Firefox/42'
    FF41 = 'Firefox/41'
    FF40 = 'Firefox/40'
    FF = 'Firefox'
    GC = 'Chrome'
    GC48 = 'Chrome/48'
    GC47 = 'Chrome/47'
    GC46 = 'Chrome/46'
    GC45 = 'Chrome/45'
    OPR = 'Opera'
    OPR35 = 'Opera/35'
    OPR34 = 'Opera/34'
    OPR33 = 'Opera/33'
    OPR32 = 'Opera/32'
    SF = 'Safari'
    SF9 = 'Safari/9'
    SF8 = 'Safari/8'
    SF7 = 'Safari/7'
    SF6 = 'Safari/6'
    SF5 = 'Safari/5'
    SF4 = 'Safari/4'
     
    MS_UPDATE = 'Microsoft Windows Update'
    ADOBE_UPDATER = 'Adobe Acrobat Updater'

class filetypes(object):
    # Archives
    ARC_7Z = '7 zip'
    ARC_ARC = 'ARC'
    ARC_ARJ = 'ARJ'
    ARC_BINHEX = 'BinHex'
    ARC_BZIP2 = 'BZIP2'
    ARC_CPIO = 'CPIO'
    ARC_GZIP = 'GZIP'
    ARC_LHA = 'LHA'
    ARC_LHARC = 'LHARC'
    ARC_MSCAB = 'Microsoft CAB'
    ARC_RAR = 'RAR'
    ARC_STUFFIT = 'StuffIt'
    ARC_TAR = 'TAR'
    ARC_Z = 'Compress Archive (Z)'
    ARC_ZIP = 'ZIP Archive'

    # Document Types
    DOC_MSOFFICE = 'Microsoft Office'
    DOC_FM = 'FrameMaker Document (FM)'
    DOC_PDF = 'Portable Document Format (PDF)'
    DOC_PS = 'PostScript Document (PS)'
    DOC_RTF = 'Rich Text Format (RTF)'
    DOC_XML = 'XML Document (XML)'
    DOC_OASIS ='OASIS Open Document Format'
    DOC_OPENOFFICE = 'OpenOffice Document'

    # Executable Code
    EXE_ACTIVEX = 'ActiveX Plugin'
    EXE_WINEXEC = 'Windows Executable'
    EXE_JAVA = 'Java Applet'
    EXE_UNIXEXEC = 'UNIX Executable'
    EXE_FFEXT = 'Mozilla/Firefox Extension'

    # Installers
    INST_UNIX = 'UNIX/LINUX Packages'

    # Media
    MEDIA_AUDIO = 'Audio'
    MEDIA_STREAMING = 'Streaming Media'
    MEDIA_VIDEO = 'Video'
    MEDIA_IMAGE = 'Photographic Image Processing Formats (TIFF/PSD)'

    # P2P Metafiles
    P2P_BITTORRENT = 'BitTorrentLinks (.torrent)'

    # Web Page Content
    WEB_FLASH = 'Flash'
    WEB_JS = 'JavaScript'
    WEB_IMAGE = 'All Images'
    WEB_IMAGE80 = 'Images' # use it instead of WEB_IMAGE in coeus80+

    # Miscellanious
    MISC_VCAL = 'Calendar Data'

class mimetypes(object):
    AUDIO_MPEG3 = 'audio/mpeg3'

    TEXT_RTF = 'text/rtf'
    # TODO Add MIME types on demand

class alert_types(object):
    SYSTEM = 'System'
    HARDWARE = 'Hardware'
    UPDATER = 'Updater'
    PROXY = 'Web Proxy'
    DVS_AMW = 'DVS and Anti-Malware'
    L4TM = 'L4 Traffic Monitor'
    ALL = 'All'

class log_type(object):
    """Names of all WSA log subscriptions types.
    Log subscriptions default file names are used as keys.
    """
    acllog = 'Access Control Engine Logs'
    aclog = 'Access Logs'
    musd_log = 'AnyConnect Secure Mobility Daemon Logs'
    authlog = 'Authentication Framework Logs'
    avclog = 'AVC Engine Framework Logs'
    avc_log = 'AVC Engine Logs'
    cli = 'CLI Audit Logs'
    configlog = 'Configuration Logs'
    connlog = 'Connection Management Logs'
    dsdataloss_log = 'Data Security Logs'
    dslog = 'Data Security Module Logs'
    dcalog = 'DCA Engine Framework Logs'
    dca_log = 'DCA Engine Logs'
    proxyerrlog = 'Default Proxy Logs'
    diskmgrlog = 'Disk Manager Logs'
    external_auth_logs = 'External Authentication Logs'
    feedback_log = 'Feedback Logs'
    feedsd_log = 'Feedsd Logs'
    ftplog = 'FTP proxy Logs'
    ftpd_text = 'FTP Server Logs'
    gui = 'GUI Logs'
    haystackd = 'Haystack Logs'
    httpslog = 'HTTPS Logs'
    licenselog = 'License Module Logs'
    logframeworklog = 'Logging Framework Logs'
    logderrlog = 'Logging Logs'
    mcafeeframeworklog = 'McAfee Integration Framework Logs'
    mcafee_log = 'McAfee Logs'
    memmgrlog = 'Memory Manager Logs'
    misclog = 'Miscellaneous Proxy Modules Logs'
    sntpd = 'NTP Logs'
    ocspd_logs = 'OCSP Logs'
    pacd_log = 'PAC File Hosting Daemon Logs'
    tmon_bypass = 'Proxy Bypass Logs'
    reportd = 'Reporting Logs'
    reportqueryd = 'Reporting Query Logs'
    saas_auth_log = 'SaaS Auth Logs'
    shd = 'SHD Logs'
    snmp_logs = 'SNMP Logs'
    snmplog = 'SNMP Module Logs'
    sockslog = 'SOCKS Proxy Logs'
    sophosframeworklog = 'Sophos Integration Framework Logs'
    sophos_log = 'Sophos Logs'
    status_log = 'Status Logs'
    system = 'System Logs'
    tmon_err = 'Traffic Monitor Error Logs'
    tmon_misc = 'Traffic Monitor Logs'
    uds_log = 'UDS Logs'
    updater_logs = 'Updater Logs'
    w3c_log = 'W3C Logs'
    wbnp_log = 'WBNP Logs'
    wbrsframeworklog = 'WBRS Integration Framework Logs'
    wccplog = 'WCCP Module Logs'
    webcatframeworklog = 'Webcat Integration Framework Logs'
    webrootframeworklog = 'Webroot Integration Framework Logs'
    webrootlog = 'Webroot Logs'
    welcomeack_log = 'Welcome Page Acknowledgement Logs'

class https_cert_info(object):
    DEFAULT = {'name': "ironport.com",
               'org': "QA Automation",
               'org_unit': "QA",
               'country': "US",
               'duration': 12,
               'constraints': False}

class saas_cert_info(object):
    DEFAULT = {'name': "ironport.com",
               'org': "QA Automation",
               'org_unit': "QA",
               'country': "US",
               'duration': 12}

class alert_levels(object):
    CRITICAL = 'Critical'
    WARNING = 'Warning'
    INFO = 'Info'
    ALL = 'All'

class Constant(object):
    """ Aggregates constant's Id and screen name

    - id: internal product's identifier (usually number) if cannot be retrived,
    any unique within set of constants
    - name: screen name - the published on the page name
    """
    def __init__(self, identifier, name):
        self.id = identifier
        self.name = name

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return 'Id: %s; Name: %s' % (self.id, self.name)

class applications(object):
    #Application Names
    #Blogging
    BLOGGER = Constant('1058', 'Blogger')
    DISQUS = Constant('1124', 'Disqus')
    FC2BLOG = Constant('1255', 'FC2 Blog')
    LIVEJOURNAL = Constant('1057', 'LiveJournal')
    TUMBLR = Constant('1056', 'Tumblr')
    WORDPRESS = Constant('1059', 'Wordpress')

    #Collaboration
    ANSWERS = Constant('1187', 'Answers.com')
    PASTEBIN = Constant('1217', 'Pastebin')
    WIKIPEDIA = Constant('1152', 'Wikipedia')

    # Enterprise Applications
    AMAZONS3 = Constant('1259', 'Amazon S3')
    CONCUR = Constant('1077', 'Concur')
    SHAREPOINT = Constant('1125', 'SharePoint')
    SUGARCRM = Constant('1072', 'SugarCRM')

    # Facebook
    FACEBOOKAPP_ENTERTAINMENT = Constant('1040', 'Facebook Applications: Entertainment')
    FACEBOOKAPP_GAMES = Constant('1041', 'Facebook Applications: Games')
    FACEBOOKAPP_OTHER = Constant('1042', 'Facebook Applications: Other')
    FACEBOOKAPP_SPORTS = Constant('1043', 'Facebook Applications: Sports')
    FACEBOOKAPP_UTILITIES = Constant('1044', 'Facebook Applications: Utilities')
    FACEBOOKEVENTS =  Constant('1030', 'Facebook Events')
    FACEBOOKGENERAL = Constant('1031', 'Facebook General')
    FACEBOOKCHAT = Constant('1158', 'Facebook Messages and Chat')
    FACEBOOKNOTES = Constant('1031', 'Facebook Notes')
    FACEBOOKPHOTOSVIDEOS = Constant('1034', 'Facebook Photos and Videos')

    # File Sharing
    RAPIDSHARE = Constant('1081', 'RapidShare')
    BITTORRENT = Constant('1022', 'BitTorrent')
    FOURSHARED = Constant('1109', '4shared')
    YOUSENDIT = Constant('1023', 'HighTail/YouSendIt')

    # Games
    EVONY = Constant('1132', 'Evony')
    HANGAMECOJP = Constant('1251', 'Hangame.co.jp')
    POGO = Constant('1123', 'Pogo')
    WII = Constant('1089', 'Wii')

    # Google +
    GOOGLEPLUSGAMES = Constant('1122', 'Google+ Games')
    GOOGLEPLUSGENERAL = Constant('1116', 'Google+ General')
    GOOGLEPLUSHANGOUTS = Constant('1118', 'Google+ Hangouts/Chat ')
    GOOGLEPLUSLOCATION_TAGGING = Constant('1120', 'Google+ Location Tagging')
    GOOGLEPLUSPHOTOS = Constant('1117', 'Google+ Photos')
    GOOGLEPLUSVIDOES = Constant('1119', 'Google+ Videos')

    # Instant Messaging
    AOL_IM = Constant('1007', 'AOL Instant Messenger')
    FETION = Constant('1256', 'Fetion')
    GTALK = Constant('1008', 'Google Talk')
    ILOVEIM = Constant('1148', 'ILoveIM')
    KOOLIM = Constant('1144', 'KoolIM')
    MESSENGERFX = Constant('1130', 'MessengerFX')
    MIBBIT = Constant('1146', 'Mibbit')
    MSN_IM = Constant('1009', 'MSN Messenger')
    WECHATWEB = Constant('1444', 'Wechat_web')
    YAHOO_IM = Constant('1010', 'Yahoo Messenger')

    #Internet Utilities
    EBAY = Constant('1010', 'eBay')
    GOOGLEANALYTICS = Constant('1010', 'Google Analytics')
    GOOGLEAPPENGINE = Constant('1010', 'Google App Engine')
    GOOGLECALENDAR = Constant('1010', 'Google Calendar')
    GOOGLEMAP = Constant('1435', 'Google Maps')
    GOOGLETRANSLATE = Constant('1010', 'Google Translate')
    YAHOOTOOLBAR = Constant('1010', 'Yahoo Toolbar')

    #iTunes
    ITUNES_DESKTOP = Constant('1126', 'iTunes Desktop')
    ITUNES_IPAD= Constant('1129', 'iTunes iPad')
    ITUNES_IPHONE = Constant('1127', 'iTunes iPhone')
    ITUNES_IPOD = Constant('1128', 'iTunes iPod')

    # LinkedIn
    LINKEDINCONTACTS = Constant('1052', 'LinkedIn Contacts')
    LINKEDINGENERAL = Constant('1050', 'LinkedIn General')
    LINKEDININBOX = Constant('1054', 'LinkedIn Inbox')
    LINKEDINJOBS = Constant('1051', 'LinkedIn Jobs')
    LINKEDINPROFILE = Constant('1053', 'LinkedIn Profile')

    # Media
    MEDIA500PX = Constant('1249', '500px')
    MEDIA56COM = Constant('1246', '56.com')
    ASF = Constant('1013', 'ASF')
    DAILYMOTION = Constant('1181', 'Dailymotion')
    DEEZER = Constant('1229', 'Deezer')
    FLASH = Constant('1001', 'Flash Video')
    FLICKR = Constant('1017', 'Flickr')
    FOTKI = Constant('1137', 'Fotki')
    FREEETV = Constant('1073', 'FreeeTV')
    GYAO = Constant('1242', 'Gyao')
    HULU = Constant('1002', 'Hulu')
    JANGO = Constant('1135', 'Jango')
    JOOST = Constant('1099', 'Joost')
    LASTFM = Constant('1136', 'Last.fm')
    LIVE365 = Constant('1068', 'Live365')
    LIVESTREAM = Constant('1235', 'Livestream')
    MEGAVIDEO = Constant('1090', 'Megavideo')
    MPEG = Constant('1006', 'MPEG')
    NETFLIX = Constant('1098', 'Netflix')
    NICONICODOUGA = Constant('1194', 'Nico Nico Douga')
    PANDORA = Constant('1064', 'Pandora')
    PANDORATV = Constant('1065', 'Pandora TV')
    PHOTOBUCKET = Constant('1185', 'Photobucket')
    PICASA = Constant('1097', 'Picasa')
    PLAYMUSIC = Constant('1434', 'Play Music')
    PPSTV = Constant('1245', 'PPS.tv')
    PPTV = Constant('1243', 'PPTV')
    QTIME = Constant('1005', 'QuickTime')
    REAL_MEDIA = Constant('1004', 'RealMedia')
    SHUTTERFLY = Constant('1066', 'Shutterfly')
    SILVERLIGHT = Constant('1020', 'Silverlight')
    SMUGMUG = Constant('1176', 'SmugMug')
    SOHUVIDEO = Constant('1267', 'Sohu Video')
    TUDOU = Constant('1238', 'Tudou')
    VIDDLER = Constant('1021', 'Viddler')
    VIMEO = Constant('1195', 'Vimeo')
    WINAMPREMOTE = Constant('1174', 'Winamp Remote')
    WIN_MEDIA = Constant('1003', 'Windows Media')
    YOUKU = Constant('1236', 'Youku')
    YOUTUBE = Constant('1011', 'YouTube')
    IMDB = Constant('1413', 'IMDb')

    # Myspace
    MYSPACEGENERAL = Constant('1108', 'MyspaceGeneral')
    MYSPACEMUSIC = Constant('1162', 'MyspaceMusic')
    MYSPACEPHOTOS = Constant('1160', 'MyspacePhotos')
    MYSPACEVIDEOS = Constant('1161', 'MyspaceVideos')

    # Presentation/Conferencing
    CROSSLOOP = Constant('1094', 'Crossloop')
    EROOMNET = Constant('1157', 'eRoom.net')
    GLIDE = Constant('1189', 'Glide')
    TEAMVIEWER = Constant('1075', 'TeamViewer')
    TECHINLINE = Constant('1188', 'Techinline')
    TWIDDLA = Constant('1191', 'Twiddla')
    WEBEX = Constant('1019', 'WebEx')

    # Proxies
    ASPROXY = Constant('1196', 'ASProxy')
    AVOIDR = Constant('1113', 'Avoidr')
    CAMOPROXY = Constant('1193' ,'CamoProxy')
    CGIPROXY = Constant('1103' ,'CGIProxy')
    CORALCDN = Constant('1199' ,'CoralCDN')
    FLYPROXY = Constant('1134' ,'FlyProxy')
    GLYPE = Constant('1104' ,'Glype')
    GUARDSTER = Constant('1221' ,'Guardster')
    KPROXY = Constant('1149','KProxy')
    MEGAPROXY = Constant('1105','Megaproxy')
    OTHERWEBPROXY = Constant('1028','OtherWebProxy')
    PHPPROXY = Constant('1084','PHPProxy')
    PROXONO = Constant('1198','Proxono')
    SOCKS2HTTP = Constant('1083','Socks2HTTP')
    SURESOME = Constant('1192','Suresome')
    SURROGAFIER = Constant('1201','Surrogafier')
    VTUNNEL = Constant('1155','Vtunnel')
    ZELUNE = Constant('1197','Zelune')

    # Social Networking
    AMEBA = Constant('1168', 'Ameba')
    DELICIOUS = Constant('1046', 'Delicious')
    DIGG = Constant('1047', 'Digg')
    FRIENDFEED = Constant('1113', 'FriendFeed')
    GOOGLEGROUPS = Constant('1163', 'GoogleGroups')
    GOOGLEWAVE = Constant('1080', 'GoogleWave')
    GREE = Constant('1178', 'Gree')
    KAIXIN001 = Constant('1254', 'Kaixin001')
    MIXI = Constant('1180', 'Mixi')
    PINTEREST = Constant('1173', 'Pinterest')
    QUORA = Constant('1240', 'Quora')
    REDDIT = Constant('1228', 'Reddit')
    RENREN = Constant('1253', 'RenRen')
    SNAPCHAT = Constant('1433', 'Snapchat')
    SCRIBD = Constant('1175', 'Scribd')
    SLASHDOT = Constant('1048', 'Slashdot')
    SOHUWEIBO = Constant('1248', 'SohuWeibo')
    STUMBLEUPON = Constant('1239', 'StumbleUpon')
    TENCENTWEIBO = Constant('1250', 'TencentWeibo')
    TWITTER = Constant('1045', 'Twitter')
    TWOCHANNEL = Constant('1167', 'TwoChannel')
    VIADEO = Constant('1308', 'Viadeo')
    WEIBO = Constant('1244', 'Weibo')
    XING = Constant('1159', 'Xing')
    YAHOOMOBAGE = Constant('1166', 'YahooMobage')
    YIKYAK = Constant('1432', 'Yik Yak')
    ZHIHU = Constant('1257', 'Zhihu')

    # Software Updates
    MACAFEE_UPDATE = Constant('1078', 'MacafeeUpdate')
    SOPHOS_UPDATE = Constant('1088', 'SophosUpdate')
    SYMANTEC_UPDATE = Constant('1202', 'SymantecUpdate')
    TRENDMICRO_UPDATE = Constant('1093', 'TrendMicroUpdate')
    WINDOWS_UPDATE = Constant('1200', 'WindowsUpdate')

    # Webmail
    AOLMAIL= Constant('1183', 'Aolmail')
    COMCASTMAIL = Constant('1115', 'comcastmail')
    EYEJOT = Constant('1156', 'eyejot')
    GMAIL = Constant('1062', 'Gmail')
    GMXEMAIL = Constant('1223', 'Gmxemail')
    HUSHMAIL = Constant('1220', 'Hushmail')
    MAILRU = Constant('1286', 'Mail.Ru')
    MOBILEME = Constant('1085', 'Mobileme')
    OUTLOOK = Constant('1063', 'Outlook')
    YAHOOMAIL = Constant('1061', 'Yahoo Mail')

    # Other (from coeus-7-5 branch)
    BING = Constant('1016', 'Bing')
    CRAIGSLIST = Constant('1018', 'Craigslist')
    FLICKR = Constant('1017', 'Flickr')
    GOOGLE = Constant('1014', 'Google Search')
    YAHOO = Constant('1015', 'Yahoo Search')
    FACEBOOK = Constant('1025', 'Facebook')
    FACEBOOKBUSINESS = Constant('1037', 'FaceBookBusiness')

    # Application types
    BLOGGING = Constant('10', 'Blogging')
    COLLABORATION = Constant('17', 'Collaboration ')
    ENTERPRISEAPP = Constant('13', 'Enterprise Applications')
    FACEBOOK = Constant('8', 'Facebook')
    P2P = Constant('5', 'File Sharing')
    GAMES = Constant('14', 'Games')
    GOOGLEPLUS = Constant('15', 'Google+')
    IM = Constant('2', 'Instant Messaging')
    UTILITIES = Constant('12', 'Internet Utilities')
    ITUNES = Constant('16', 'iTunes')
    LINKEDIN = Constant('9', 'LinkedIn')
    MEDIA = Constant('1', 'Media')
    MYSPACE = Constant('18', 'Myspace')
    TELEPRESENCE = Constant('4', 'Presentation / Conferencing')
    PROXIES = Constant('7', 'Proxies')
    SOCIAL = Constant('6', 'Social Networking')
    UPDATES = Constant('19', 'Software Updates')
    WEBMAIL = Constant('11', 'Webmail')

    # Other (from coeus-7-5 branch)
    SEARCH = Constant('3', 'Search Engine')

class ssh_keys:
    """Provides ssh keys"""
    PUBLIC_KEY = ('ssh-dss AAAAB3NzaC1kc3MAAACBAKlMl4beBf/JD4F5sNym0l5LDRMWhH'
        'hH7oKyJPWzvSi/DjVJ6HWQnhPp3aq2CORtpd6yO8tExXDRx5VBzI2slBCi+rIaQ6sWr4'
        'Ie/aAr/FdXycbPdeKxwHawQr5esqeWb0+z59wDzSOblAx4R1JfE2HdLcRPx9GhGjHx55'
        'T+qZVtAAAAFQDuNCywyl6f57Wa48+YX2Kk86dw1QAAAIB4vpeYVOZ+6T9ohXuJajRQ8d'
        'xgID40cvxGnz3je2Y9EO7fY8gtFai8mojih2Mbkbt6fdpS+mWEDIIQAjLNi75ih/ONz8'
        'OfBzvkUznAcHjRTHrW7tSJ3Xtkpx02ddT/bDQRLIj5/V8/vY9Wsuf+l7h/7LvzXCZOo1'
        'IAILnpogK1ggAAAIEAket7Jq8HFSyp3NTlZdQNeOB0K46VK7X1I8YzHfdILeAoXxNqFW'
        'EvhB50iHw1390ETx3J9luGHtOze9JeAFr+m2HrkltfTwvUwyxbjX0yAHsXWvQ5xwXhpV'
        '0nm1hOhxHg60/5QfXu75ZKhEAz/ZWKkteK0na+mWbFAnKMUG04TwI= iaf@vampire.e'
        'ng')

class default_feature_keys:
    """cpt default feature keys"""
    coeus77 = {
        'CIWUC' : '30day',
        'HTTPS' : '30day',
        'L4 Traffic Monitor' : '30day',
        'MUS' : '30day',
        'McAfee' : '30day',
        'Sophos' : '30day',
        'Web Proxy & DVS Engine' : '30day',
        'Web Reputation Filters' : '30day',
        'Webroot' : '30day',
        }

    coeus75 = {
        'CIWUC' : '30day',
        'HTTPS' : '30day',
        'L4 Traffic Monitor' : '30day',
        'MUS' : '30day',
        'McAfee' : '30day',
        'Sophos' : '30day',
        'Web Proxy & DVS Engine' : '30day',
        'Web Reputation Filters' : '30day',
        'Webroot' : '30day',
        }

    coeus71 = {'CIWUC' : '30day',
        'HTTPS' : '30day',
        'L4 Traffic Monitor' : '30day',
        'MUS' : '30day',
        'McAfee' : '30day',
        'Sophos' : '30day',
        'URL Filtering' : '30day',
        'Web Proxy & DVS Engine' : '30day',
        'Web Reputation Filters' : '30day',
        'Webroot' : '30day',
        }

    phoebe76 = {'Bounce Verification' : '30day',
        'IronPort Anti-Spam' : '30day',
        'IronPort Email Encryption' : '30day',
        'McAfee' : '30day',
        'Outbreak Filters' : '30day',
        'RSA Email Data Loss Prevention' : '30day',
        'Receiving' : '30day',
        'Sophos' : '30day',
        }

    zeus78 = {'Cisco IronPort Centralized Email Message Tracking' : '30day',
        'Cisco IronPort Centralized Email Reporting' : '30day',
        'Cisco IronPort Centralized Web Reporting' : '30day',
        'Cisco IronPort Spam Quarantine' : '30day',
        'Incoming Mail Handling' : 'Perpetual',
        }

class fkey_status(object):
    ACTIVE = 'Active'
    DORMANT = 'Dormant'
    PERPETUAL = 'Perpetual'
    EXPIRED = 'Expired'

class log_level(object):
    CRITICAL = 'Critical'
    DEBUG = 'Debug'
    INFO = 'Info'
    TRACE = 'Trace'
    WARNING = 'Warning'

