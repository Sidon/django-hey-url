import json
from datetime import datetime
from jsonview.decorators import json_view
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
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
def month_metrics(request):
    valid_query = True
    if short_url := request.GET.get('short_url', None):
        if db_services.get_original_url(short_url):
            today = datetime.today()
            month = request.GET.get('month', today.month)
            year = request.GET.get('year', today.year)
        else:
            valid_query = False
    else:
        valid_query = False

    if not valid_query:
        return render(request, 'heyurl/errors/404.html')

    clicks = db_services.get_metrics(short_url, year, month)
    day_metrics = dict()
    if clicks:
        for click in clicks:
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
        original_url=db_services.get_original_url(short_url).original_url,
        year=year,
        month=month,
        data=[day_metrics]
    )
    return metrics

@json_view
def top_ten(request):
    return db_services.get_top_n()