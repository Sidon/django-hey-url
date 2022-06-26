from collections import namedtuple
import pytest
from heyurl import views
from tests import data_helper
from tests.data_helper import helper_tests
from  heyurl.utils import db_services

@pytest.mark.django_db
def test_store():
    mock_http_post = helper_tests.http_post(lambda orignal_url: helper_tests.inexistent_urls[0])
    mock_request = helper_tests.http_request(
        mock_http_post,
        helper_tests.user_agent(),
        None,
        'POST'
    ) 
    response = views.store(mock_request)
    assert response.content.decode('ascii').split("<br>")[0]=='Storing a new URL object into storage:'

@pytest.mark.django_db
def test_store_fail():
    mock_http_post = helper_tests.http_post(lambda orignal_url: helper_tests.invalid_url)
    mock_request = helper_tests.http_request(
        mock_http_post,
        helper_tests.user_agent(),
        None,
        'POST'
    ) 
    response = views.store(mock_request)
    
    assert response.content == b'Invalid Url:<br>inv4lid#url'

@pytest.mark.django_db
def test_short_url():
    assert views.store(helper_tests.http_request()).status_code==200

@pytest.mark.django_db
def test_handler404(monkeypatch):
    monkeypatch.setattr('heyurl.views.render', lambda request, template:helper_tests.http_request() )
    response = views.handler404(helper_tests.http_request(), None)
    assert response.status_code==302

@pytest.mark.django_db
def test_month_metrics(django_db_setup):
    metrics = views.month_metrics(helper_tests.http_request())
    assert  metrics.status_code==200
    

@pytest.mark.django_db
def test_top_ten(django_db_setup):
    top_ten = views.top_ten(helper_tests.http_request())
    assert top_ten.status_code==200
    
@pytest.mark.django_db
def test_short_url(django_db_setup):
    redirect = views.short_url(helper_tests.http_request(), helper_tests.fsl_short)
    assert redirect.status_code==302
    