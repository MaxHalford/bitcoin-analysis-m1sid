from instagram.client import InstagramAPI
import keys

api = InstagramAPI(access_token=keys.access_token,
                   client_secret=keys.client_secret)
media = api.tag("bitcoin")
