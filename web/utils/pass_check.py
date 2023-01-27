import requests
import hashlib

api_url = "https://api.pwnedpasswords.com/range/"


def is_pawned(password):
    result = dict()
    hashed_pass = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5, tail = hashed_pass[:5], hashed_pass[5:]
    res = requests.get(api_url + f"{first5}")
    if res.status_code != 200:
        result[
            "err"
        ] = f"Error received on fetching data.\n{res.status_code}, check the API and code..."
        return result
    response_hashes = (line.split(":") for line in res.text.splitlines())
    for h, count in response_hashes:
        if h == tail:
            result["is-pwned"] = True
            result["count"] = count
            return result
    result["is-pwned"] = False
    return result
