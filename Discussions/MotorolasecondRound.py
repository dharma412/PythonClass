# import requests
#
#
# def post_client():
#
#     url="https://wms-ugw101-sqa.kodiakcloudsqapoc.com/auth/realms/datagw/protocol/openid-connect/token"
#
#     payload={"clientid": f"{cleintid}","clientsecret": f"{clientsecret}"}
#
#     response=requests.post(url,payload)
#
#     assert response.status_code==201
#     data=response.text
#
#
#
# robot --A textfile.txt  --testcase=post_client tescase.robot
#
# # def read_File():
# #     with open("file.txt") as f1:
# #         result=f1.readlines()
# #
# --argumnets
# clientid:jduuhruf
# clientsecret:7845894587
#
#
# get post path
#
#
# launch appium
#     [Argumets]   port=5030
#     open application   //htttps:122  port   application activty  platomt  version
#
# laun appium   port=5020   application="new name"
#
#
#
# - IBCf--
#
# Invite
#
# Reinvite
#
# R -RUi
#
# P-Asserted
#
# PAIn
#
#
#
# ims CORE
#
#
#
# *** settings ***
#
# suitsteup    methdo1
# suite teardown  method2
#
#
# 4 tetcase
#
#
# ***
#
# @{list1}   3  4 4 5 6 6 7
# &{dic1}    name=pyro  version=2.8
# ${scalr}
#
#
# ** keyword
# keyword1
#     [Argument]   a   b
#
#     [retunr]    a+b
#
#
# *** testcase ***
# tescase1
#     ${value}    keyword1   valie1  value2
#
#     FOR  ${ITEM}  IN  @{list1}
#
#         LOG TO CONSOLE   ${ITEM}
#
#     END
#
#     log to console  ${value}