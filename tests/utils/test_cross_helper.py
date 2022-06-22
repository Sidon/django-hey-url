from collections import namedtuple
from django.urls import reverse
from heyurl.utils import cross_helper


mock_user_agent_class = namedtuple("FakeUserAgent", ["browser", "is_mobile", "is_tablet", "is_pc"])

def test_create_random_key():
    rnd_key = cross_helper._create_random_key()
    ok_key = True
    for char in rnd_key:
        if char not in cross_helper.chars:
            ok_key = False
            break
    assert len(rnd_key) <= cross_helper.max_length_key and ok_key


def test_get_user_agent_browser_is_pc():
    mock_user_agent = mock_user_agent_class('Mozzila Firefox', None, None, True)
    browser, platform  =  cross_helper.get_user_agent(mock_user_agent)
    assert browser=='Mozzila Firefox' and platform=='PC'

def test_get_user_agent_is_mobile():
    mock_user_agent = mock_user_agent_class(None, True, None, None)
    browser, platform  =  cross_helper.get_user_agent(mock_user_agent)
    assert not browser and platform=='Mobile'


def test_get_user_agent_is_tablet():
    mock_user_agent = mock_user_agent_class(None, None, True, None)
    browser, platform  =  cross_helper.get_user_agent(mock_user_agent)
    assert not browser and platform=='Tablet'