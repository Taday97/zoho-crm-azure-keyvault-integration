from zcrmsdk import ZCRMRestClient

def initialize():
    configuration = {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "redirect_uri": "http://localhost:8000/zoho/callback",  
        "currentUserEmail": "tadayglezchav@gmail.com",
        "token_persistence_path": "path/to/zcrm_oauthtokens.txt"
    }
    ZCRMRestClient.initialize(configuration)