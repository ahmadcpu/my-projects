import requests
import json

with open("cookies.json", "r") as f:
    cookies = json.loads(f.read())

headers = {
    'x-csrftoken': cookies["csrftoken"],
    'cookie': 'mid={}; ig_did={}; ds_user_id={}; csrftoken={}; sessionid={}; shbid={}; shbts={}; rur={}'
    .format(cookies["mid"], cookies["ig_did"], cookies["ds_user_id"], cookies["csrftoken"], cookies["sessionid"], cookies["shbid"], cookies["shbts"], cookies["rur"]),
}

class Instagram:
    def __init__(self) -> None:
        pass

    def follow(self, username):
        id = requests.get(f"https://www.instagram.com/{username}/?__a=1", headers=headers).json()["graphql"]["user"]["id"]
        requests.post(f'https://www.instagram.com/web/friendships/{id}/follow/', headers=headers)
        
    def unfollow(self, username):
        id = requests.get(f"https://www.instagram.com/{username}/?__a=1", headers=headers).json()["graphql"]["user"]["id"]
        requests.post(f'https://www.instagram.com/web/friendships/{id}/unfollow/', headers=headers)
        
    def like(self, post_link):
        link = post_link.replace("?utm_source=ig_web_copy_link", "?__a=1")
        media_id = requests.get(link, headers=headers).json()["graphql"]["shortcode_media"]["id"]
        requests.post(f'https://www.instagram.com/web/likes/{media_id}/like/', headers=headers)

    def unlike(self, post_link):
        link = post_link.replace("?utm_source=ig_web_copy_link", "?__a=1")
        media_id = requests.get(link, headers=headers).json()["graphql"]["shortcode_media"]["id"]
        requests.post(f'https://www.instagram.com/web/likes/{media_id}/unlike/', headers=headers)

    def comment(self, text, post_link):
        link = post_link.replace("?utm_source=ig_web_copy_link", "?__a=1")
        media_id = requests.get(link, headers=headers).json()["graphql"]["shortcode_media"]["id"]
        data = {
            'comment_text': text,
            'replied_to_comment_id': ''
        }
        requests.post(f'https://www.instagram.com/web/comments/{media_id}/add/', headers=headers, data=data)

    def last_followers(self, username, count=12):
        id = requests.get(f"https://www.instagram.com/{username}/?__a=1", headers=headers).json()["graphql"]["user"]["id"]
        params = (
            ('count', count),
            ('search_surface', 'follow_list_page'),
        )
        response = requests.get(f'https://i.instagram.com/api/v1/friendships/{id}/followers/', headers=headers, params=params)
        return response.json()["users"]

    def last_followings(self, username, count=12):
        id = requests.get(f"https://www.instagram.com/{username}/?__a=1", headers=headers).json()["graphql"]["user"]["id"]
        params = (
            ('count', count),
        )

        response = requests.get(f'https://i.instagram.com/api/v1/friendships/{id}/following/', headers=headers, params=params)
        return response.json()["users"]

    def like_count(self, post_link):
        link = post_link.replace("?utm_source=ig_web_copy_link", "?__a=1")
        return requests.get(link, headers=headers).json()["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]
        
    def user_info(self, username):
        response = requests.get(f"https://www.instagram.com/{username}/?__a=1", headers=headers).json()
        posts = response["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
        followers = response["graphql"]["user"]["edge_followed_by"]["count"]
        followings = response["graphql"]["user"]["edge_follow"]["count"]

        return [posts, followers, followings]

        



