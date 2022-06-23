from heyurl.utils import cross_helper
from tests.data_helper import DEFAULT_BROWSER, BrowserMock, BROWSER_MOCK, UserAgentMock


def test_get_user_agent_browser():
    browser_mock = BrowserMock('Firefox')
    mock_user_agent = UserAgentMock(browser_mock)
    browser, platform  =  cross_helper.get_user_agent(mock_user_agent)
    assert browser=='Firefox'

def test_get_user_agent_is_mobile():
    mock_user_agent = UserAgentMock(BROWSER_MOCK, True)
    browser, platform  =  cross_helper.get_user_agent(mock_user_agent)
    assert browser == DEFAULT_BROWSER and platform == 'Mobile'

def test_get_user_agent_is_tablet():
    mock_user_agent = UserAgentMock(BROWSER_MOCK, None, True, None)
    browser, platform  =  cross_helper.get_user_agent(mock_user_agent)
    assert browser == DEFAULT_BROWSER and platform == 'Tablet'

def test_get_user_agent_is_pc():
    mock_user_agent = UserAgentMock(BROWSER_MOCK, None, None, True)
    browser, platform  =  cross_helper.get_user_agent(mock_user_agent)
    assert browser == DEFAULT_BROWSER and platform == 'PC'


def test_create_random_key():
    rnd_key = cross_helper._create_random_key()
    ok_key = True
    for char in rnd_key:
        if char not in cross_helper.chars:
            ok_key = False
            break
    assert len(rnd_key) <= cross_helper.max_length_key and ok_key
