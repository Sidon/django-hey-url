import json
import pytest
from heyurl.utils import db_services


@pytest.mark.django_db
def test_create_short_url():
    url_created  = db_services.create_short_url("https://www.fullstacklabs.co")
    url_dict = json.loads(url_created)
    assert url_dict['original_url'] == 'https://www.fullstacklabs.co'


@pytest.mark.django_db
def test_save_click():
    url_created  = db_services.create_short_url("https://www.fullstacklabs.co")
    url_dict = json.loads(url_created)
    clicks = db_services.save_click(url_dict['short_url'], 'chrome', 'PC')
    updated_clicks = db_services.save_click(url_dict['short_url'], 'chrome', 'PC')
    assert clicks==1 and updated_clicks==2

@pytest.mark.django_db
def test_check_original_url():
    url_created  = db_services.create_short_url("https://www.fullstacklabs.co")
    url_checked = db_services.check_original_url("https://www.fullstacklabs.co")
    assert url_checked==url_created

@pytest.mark.django_db
def test_get_original_url():
    url_created  = db_services.create_short_url("https://www.fullstacklabs.co")
    url_created_dict = json.loads(url_created)
    url_got = db_services.get_original_url(url_created_dict['short_url'])
    assert url_created_dict['short_url']==url_got.short_url

@pytest.mark.django_db
def test_get_metrics(short_url, year, month):
    url_created = db_services.create_short_url("https://www.fullstacklabs.co")
    url_created_dict = json.loads(url_created)
    url_got = db_services.get_original_url(url_created_dict['short_url'])
    assert url_created_dict['short_url']==url_got.short_url
