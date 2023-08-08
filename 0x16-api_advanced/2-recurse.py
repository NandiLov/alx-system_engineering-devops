#!/usr/bin/python3
"""
Using reddit's API
"""
import requests

def recurse(subreddit, hot_list=[], after=None):
    # Construct the API URL for the subreddit's hot posts
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"

    # If 'after' is provided, use it to fetch the next page
    if after:
        url += f"&after={after}"

    # Set a custom User-Agent header to identify your script
    headers = {'User-Agent': 'Reddit Hot Articles Recursive Bot'}

    # Send a GET request to the API
    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'children' in data['data']:
            posts = data['data']['children']

            # Add titles of current page to the hot_list
            for post in posts:
                title = post['data']['title']
                hot_list.append(title)

            # If there are more pages, recursively call the function with the 'after' parameter
            if 'after' in data['data'] and data['data']['after']:
                return recurse(subreddit, hot_list, after=data['data']['after'])
            else:
                return hot_list
        else:
            return None
    elif response.status_code == 404:
        return None
    else:
        print("An error occurred while fetching data.")
        return None

# Example usage
subreddit = "python"  # Change this to the desired subreddit
hot_articles = recurse(subreddit)

if hot_articles:
    for i, article in enumerate(hot_articles, start=1):
        print(f"{i}. {article}")
else:
    print("No results found for the given subreddit.")
