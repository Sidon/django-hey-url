import json
import secrets
from collections import Counter
from django.forms.models import model_to_dict  # https://stackoverflow.com/a/29088221
from . import cross_helper
from heyurl import models

def create_short_url(inputed_original_url) -> str:
    key = cross_helper._create_random_key()
    while models.Url.objects.filter(short_url=key).exists():
        key = cross_helper._create_random_key()
    url = models.Url()
    url.original_url = inputed_original_url
    url.short_url = key
    url.save()
    return json.dumps(model_to_dict(url))


def save_click(short_url, browser, platform):
    if url := models.Url.objects.filter(short_url=short_url).first():
        click = models.Click()
        click.url = url
        click.browser = browser
        click.platform = platform
        click.save()
        url.clicks = url.clicks+1
        url.save()
        return url.clicks
    else:
        return None

def check_original_url(inputed_original_url):
    if existing_url := models.Url.objects.filter(original_url=inputed_original_url).first():
        return json.dumps(model_to_dict(existing_url))
    return None


def get_original_url(short_url):
    return models.Url.objects.filter(short_url=short_url).first()


def get_metrics(short_url, year, month):
    clicks = models.Click.objects.filter(
        created_at__year=year,
        created_at__month=month,
        url__short_url=short_url
    )
    return clicks



def _get_top_n_metrics(clicks):
    cnt_browser = Counter()

    for browser in  [browser for browser in [n.browser for n in clicks]]:
        cnt_browser[browser] += 1

    cnt_platform = Counter()
    for platform in  [platform for platform in [n.platform for n in clicks]]:
        cnt_platform[platform] += 1

    metrics = dict(
        browsers=dict(cnt_browser),
        platforms=dict(cnt_platform)
    )
    return metrics

def get_top_n(n=10):
    top_n = models.Url.objects.all().order_by('-clicks')[:n]
    data = []
    for n in top_n:
        data.append(
            dict(
                type = "urls",
                id = n.id,
                atributes = {
                    'created-at' : n.created_at,
                    'original-url' : n.original_url,
                    'url': n.short_url,
                    'clicks': n.clicks
                },
                relationships = {
                    "metrics": _get_top_n_metrics(n.metrics.all())
                }
            )
        )
    return dict(data=data)
