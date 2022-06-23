from collections import namedtuple
import pytest
from heyurl import views
from tests import data_helper
from  heyurl.utils import db_services

ORIGINAL_URL = 'https://www.fullstacklabs.co/projects/python'

POSTMock = namedtuple(
    "POSTMock",
    "get",
    defaults=[lambda orignal_url: ORIGINAL_URL]
)

POST_MOCK = POSTMock()
INVALID_POST_MOCK = POSTMock(lambda original_url: 'inv4lid#url')

RequestMock = namedtuple(
    'RequestMock',
    ['POST', 'user_agent', 'path', 'method'],
    defaults=[POST_MOCK,data_helper.USER_AGENT_MOCK,'/a', 'POST']
)

@pytest.mark.django_db
def test_store():
    response = views.store(RequestMock())
    assert response.content.decode('ascii').split("<br>")[0]=='Storing a new URL object into storage:'

@pytest.mark.django_db
def test_store_fail():
    response = views.store(RequestMock(INVALID_POST_MOCK))
    assert response.content == b'Invalid Url:<br>inv4lid#url'

@pytest.mark.django_db
def test_short_url():
    assert views.store(RequestMock()).status_code==200

@pytest.mark.django_db
def test_handler404(monkeypatch):
    request_mock = RequestMock()
    monkeypatch.setattr('heyurl.views.render', lambda request, template: request_mock )
    response = views.handler404(request_mock, None)
    assert response==request_mock

