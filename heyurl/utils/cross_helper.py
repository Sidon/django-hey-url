import secrets
import string

chars = f'{string.ascii_uppercase}{string.ascii_lowercase}{string.digits}'
max_length_key = 5

def _create_random_key(max_length: int = 5) -> str:
    length = secrets.choice(range(1, max_length+1))
    return "".join(secrets.choice(chars) for _ in range(length))


def get_user_agent(user_agent):
    browser = user_agent.browser.family
    if user_agent.is_mobile:
        platform = 'Mobile'
    elif user_agent.is_tablet:
        platform = 'Tablet'
    elif user_agent.is_pc:
        platform = 'PC'
    else:
        platform = 'Other'
    return browser, platform
