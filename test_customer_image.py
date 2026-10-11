import requests

# 1. The customer profile endpoint
url = "http://127.0.0.1:8000/api/auth/me/customer-profile/"

# 2. Your JWT access token
# Replace the placeholder with your current access token.
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkxNzI4NzIzLCJpYXQiOjE3OTE3Mjg0MjMsImp0aSI6IjhhZTc2NzRmMzY4YzRhNzM5ZWY5OTAzZTc0NjdlZTRmIiwidXNlcl9pZCI6IjIifQ.EcMgwb4rkapFsp4wrt4zF2j83oB-IWQOrcQlbG9uRdU"

# 3. Tell Django which user is making the request
headers = {
    "Authorization": f"Bearer {access_token}"
}

# 4. Open the image and send it as a file
image_path = r"C:\Users\user\Pictures\Wallpapers\DC\batman-wallpapers.jpg"

with open(image_path, "rb") as image:
    files = {
        "profile_image": (
            "batman-wallpapers.jpg",
            image,
            "image/jpeg"
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
