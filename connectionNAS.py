import os
import uuid
import requests
import urllib3

from dotenv import load_dotenv

load_dotenv()

# 지원되는 파일 확장자 목록
SUPPORTED_EXTENSIONS = ['.pdf', '.txt', '.hwp', '.pptx', '.ppt', '.xlsx', '.xls']

SID = ""





# def list_all_files(nas_ip, nas_port, folder_path, sid):
#     print(f"*****sid: {sid}")
#     files = list_files(nas_ip, nas_port, folder_path, sid)
#     all_files = []

#     for file in files:
#         if file['isdir']:
#             subfolder_path = file['path']
#             print(f"subfolder_path: {subfolder_path} ")
#             all_files.extend(list_all_files(nas_ip, nas_port, subfolder_path, sid))
#         else:
#             if os.path.splitext(file['name'])[1].lower() in SUPPORTED_EXTENSIONS:
#                 all_files.append(file['path'])

#     return all_files


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##로그인 
def authenticate():
    login_url = os.getenv("NAS_API")
    login_params = {
        'api': 'SYNO.API.Auth',
        'version': 2,
        'method': 'login',
        'account': os.getenv("NAS_ID"),
        'passwd': os.getenv("NAS_PW"),
        'session': 'FileStation',
        'format': 'sid'
    }


    response = requests.get(login_url, params=login_params, verify=False)
    data = response.json()
    print("로그인 데이터")
    print(data)
    print(data['success'])


    if data['success']:
        print(data['data']['sid'])  
        SID = data['data']['sid']
        return "11111111"
    else:
        return "22222222"
    

##전체파일리스트 조회
def list_files():
    list_url = os.getenv("NAS_API")
    list_params = {
        'api': 'SYNO.FileStation.List',
        'version': 2,
        'method': 'list',
        'folder_path': os.getenv("NAS_FILE_PATH"),
        '_sid': SID
    }

    response = requests.get(list_url, params=list_params, verify=False)
    data = response.json()
    print(data)
    print(">>>>>>>>>>>>>>>>>>>")
    if data['success']:
        return data['data']['files']
    else:
        raise Exception('Failed to retrieve files')


    
    
    
def flow():
    welcome=authenticate()
#     if(welcome == "11111111"): 
#         list_ = list_files()
#         print(list_)
    

flow()


##접속해서 파일 다 다운로드 -> 가져오기 ?