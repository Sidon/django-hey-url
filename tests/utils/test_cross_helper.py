from heyurl.utils import cross_helper
from tests.data_helper import helper_tests


def test_get_user_agent_browser():
    firefox_mock = helper_tests.browser('firefox')
    mock_user_agent = helper_tests.user_agent(firefox_mock, is_mobile=True)
    browser, platform  =  cross_helper.get_user_agent(mock_user_agent)
    assert browser=='firefox' and platform=='Mobile'


def test_create_random_key():
    rnd_key = cross_helper._create_random_key()
    ok_key = True
    for char in rnd_key:
        if char not in cross_helper.chars:
            ok_key = False
            break
    assert len(rnd_key) <= cross_helper.max_length_key and ok_key
