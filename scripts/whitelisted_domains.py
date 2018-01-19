from common.facebook import update_messenger_profile
from app.settings import DOMAIN
domains = ['https://09d938b8.ngrok.io']

update_messenger_profile(whitelisted_domains = domains)
