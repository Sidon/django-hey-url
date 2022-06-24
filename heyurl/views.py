import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from jsonview.decorators import json_view
from .models import Url
from .utils import db_services
from .utils.cross_helper import get_user_agent

def index(request):
    urls = Url.objects.order_by('-created_at')
    context = {'urls': urls}
    return render(request, 'heyurl/index.html', context)

def store(request):
    # FIXME: Insert a new URL object into storage

    inputed_original_url = request.POST.get('original_url')
    validator = URLValidator()
    try:
        validator(inputed_original_url)
    except ValidationError:
        return HttpResponse(f'Invalid Url:<br>{inputed_original_url}')

    if existing_url := db_services.check_original_url(inputed_original_url):
       return HttpResponse(f'Original url already exists:<br>{existing_url}')

    shortened_url = db_services.create_short_url(inputed_original_url)
    return HttpResponse(f'Storing a new URL object into storage:<br>{shortened_url}')


def _update_clicks(request, short_url):
    if not (url := db_services.get_original_url(short_url)):
        return False
    target_url = url.original_url
    browser, platform = get_user_agent(request.user_agent)
    clicks = db_services.save_click(short_url, browser, platform)
    return target_url


def short_url(request, short_url):
    # FIXME: Do the logging to the db of the click with the user agent and browser
    if not (target_url := _update_clicks(request, short_url)):
        return HttpResponse(f'Invalid Url:<br>{short_url}')
    return redirect(target_url)
    # return HttpResponse("You're looking at url %s" % short_url)


def handler404(request, exception):
    short_url = [fragment for fragment in request.path.split('/') if fragment][-1]
    if not (target_url := _update_clicks(request, short_url)):
        return render(request, 'heyurl/errors/404.html')
        # return render(request, 'heyurl/404-0.html')

    return redirect(target_url)


@json_view
def month_metrics(request,short_url, year, month):
    # f1 = models.Click.objects.filter(created_at__year=2022,created_at__month=6, url__short_url='a')
    clicks = db_services.get_metrics(short_url, year, month)
    list_clicks = []
    day_metrics = dict()
    for click in clicks:
        breakpoint()
        if not click.created_at.day in day_metrics:
            day_metrics[click.created_at.day] = dict(browser=dict(), platform=dict())
        if click.browser in day_metrics[click.created_at.day]['browser']:
            day_metrics[click.created_at.day]['browser'][click.browser] += 1
        else:
            day_metrics[click.created_at.day]['browser'][click.browser] = 1
        if click.platform in day_metrics[click.created_at.day]['platform']:
            day_metrics[click.created_at.day]['platform'][click.platform] += 1
        else:
            day_metrics[click.created_at.day]['platform'][click.platform] = 1
    metrics = dict(
        short_url=short_url,
        original_url=clicks[0].url.original_url,
        year=year,
        month=month,
        metrics=day_metrics
    )
    return metrics