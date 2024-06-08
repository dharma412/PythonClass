from datetime import *

token ='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'

repo_name="Test-Repo"+str(int(datetime.now().timestamp()))

repo_name2="Test-Repo"+str(int(datetime.now().timestamp()))

base_url="https://api.github.com"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
