import json
import pytest
from heyurl.utils import db_services
from tests.data_helper import helper_tests


# @pytest.mark.django_db
# def test_get_top_n(django_db_setup):
#     top_ten = db_services.get_top_n()
#     assert len(top_ten['data'])==10
    

# @pytest.mark.django_db
# def test_get_metrics(django_db_setup):
#     short_url = 'a'
#     month=6
#     year=2022
    
#     clicks = db_services.get_metrics(short_url, month=month, year=year)    
#     different_url = [
#         click.url.shor_url for click in clicks 
#         if click.url.short_url != short_url or 
#         click.created_at.year != year or 
#         click.created_at.month != month
#         ]
#     assert not different_url
    
# @pytest.mark.django_db
# def test_create_short_url():
#     url_created  = db_services.create_short_url(helper_tests.original_url_fsl_python)
#     url_dict = json.loads(url_created)
#     assert url_dict['original_url']==helper_tests.original_url_fsl_python


# @pytest.mark.django_db
# def test_save_click_and_check_url(django_db_setup):
#     got_url = db_services.check_original_url(helper_tests.original_url_fsl_home)
#     url_dict = json.loads(got_url)
#     clicks = db_services.save_click(url_dict['short_url'], 'chrome', 'PC')
#     updated_clicks = db_services.save_click(url_dict['short_url'], 'firefox', 'tablet')
#     assert clicks==url_dict['clicks']+1


# @pytest.mark.django_db
# def test_get_original_url():
#     url_created  = db_services.create_short_url(helper_tests.original_url_fsl_home)
#     url_created_dict = json.loads(url_created)
#     url_got = db_services.get_original_url(url_created_dict['short_url'])
#     assert url_created_dict['short_url']==url_got.short_url

