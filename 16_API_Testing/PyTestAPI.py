import json
import requests
import jsonpath
import pytest

def test_getAPI():
    url="https://reqres.in/api/users?page=2"

    responce=requests.get(url)
    v_content=responce.text
    print(v_content)

    v_Statuscode=responce.status_code
    print(v_Statuscode)
    json_Data=json.loads(v_content)
    print(json_Data)
    print(jsonpath.jsonpath(json_Data,"per_page"))

def test_PostAPI():
    url = "https://reqres.in/api/users"

    fobject = open("../tests/jsonfile", mode='r')
    v_inputData = fobject.read()

    # print(v_inputData)
    # print(type(v_inputData))

    json_input = json.loads(v_inputData)
    print(json_input)
    responce = requests.post(url, json_input)
    # print(responce.text)
    responce_code = responce.status_code
    print(responce_code)

    json_Data = json.loads(responce.text)
    print(json_Data)
    assert responce_code == 201

    v_id = jsonpath.jsonpath(json_Data, 'id')

    print(v_id[0])

def test_PUTAPI():
    url = "https://reqres.in/api/users/2"

    fobject = open("../tests/jsonfile2", mode='r')
    v_inputData = fobject.read()

    json_input = json.loads(v_inputData)

    print("--------name in the json file is ---------")
    name = json_input['name']
    print(name)
    print("--------job in the json file is ---------")
    job = json_input["job"]
    print(job)
    responce = requests.put(url, json_input)
    print(responce.status_code)

    json_data = json.loads(responce.text)
    print(json_data)

    v_name = jsonpath.jsonpath(json_data, 'name')
    v_job = jsonpath.jsonpath(json_data, 'job')
    v_upatedat = jsonpath.jsonpath(json_data, "updatedAt")

    assert v_name[0] == name

    assert v_job[0] == job

    assert v_upatedat[0] is not None

def test_DeleteAPI():
    url = "https://reqres.in/api/users/2"

    responce = requests.delete(url)
    print(responce.status_code)

    assert len(responce.text) == 0

    assert responce.status_code == 204