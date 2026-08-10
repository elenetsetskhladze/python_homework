import requests


def get_user_by_id(user_id):
    url = "https://jsonplaceholder.typicode.com/users"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            users = response.json()

            for user in users:
                if user["id"] == user_id:
                    return {
                        "name": user.get("name"),
                        "email": user.get("email"),
                        "city": user.get("address", {}).get("city"),
                        "company": user.get("company", {}).get("name"),
                    }
        return None
    except requests.RequestException:
        return None

print(get_user_by_id(2))


print(get_user_by_id(99))