import requests
response=requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)
print(response.json())
print(response.json()["title"])
import requests

# Fetch a list of 100 posts
response = requests.get("https://jsonplaceholder.typicode.com/posts")

print("Status code:", response.status_code)

posts = response.json()  # this is now a LIST, not a single dict

print("Total posts:", len(posts))

# Loop through and print just the title of each post
for post in posts:
    print(post["id"], "-", post["title"])
    # What if the request fails?
bad_response = requests.get("https://jsonplaceholder.typicode.com/posts/9999")
print("Bad request status:", bad_response.status_code)