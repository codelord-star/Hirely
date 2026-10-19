import requests

# 1. The provider profile endpoint
url = "http://127.0.0.1:8000/api/auth/provider/profile/"

# 2. Your JWT access token
# Replace the placeholder with your current access token.
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkyMzk3MTI3LCJpYXQiOjE3OTIzOTY4MjcsImp0aSI6ImNmZmUyMzE1MjA4MTQ2NjVhMGZkYWMzZDlmZDgxMDFhIiwidXNlcl9pZCI6IjIifQ.1hzecpRFtbpIs6Dd1euMSub28OZQfnbFkpkW5ZaUPCU"

# 3. Tell Django which user is making the request
headers = {
    "Authorization": f"Bearer {access_token}"
}

# 4. Open the image and send it as a file
image_path = r"C:\Users\user\Downloads\cleaninglogo.png"

with open(image_path, "rb") as image:
    files = {
        "profile_image": (
            "cleaninglogo.png",
            image,
            "image/png"
        )
    }

    response = requests.patch(
        url,
        headers=headers,
        files=files
    )

# 5. Display the server's response
print("Status code:", response.status_code)
print("Response:", response.text)
