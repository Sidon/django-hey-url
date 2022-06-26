from collections import namedtuple
from email.header import Header

from heyurl.views import short_url

FSL_HOME = "http://fullstacklabs.co"
FSL_PYTHON = "https://www.fullstacklabs.co/projects/python"
INEXISTENT_URLS =  ['https://bitcoinmagazine.com', "https://cryptonews.net", "https://news.bitcoin.com" ]
FSL_SHORT = 'a'
INVALID_URL = 'inv4lid#url'

BrowserMock = namedtuple(
    "ChromeMock",
    "family",
    defaults=['chrome']
)

UserAgentMock = namedtuple(
    "UserAgentMock",
    ["browser", "is_mobile", "is_tablet", "is_pc"],
    defaults = [BrowserMock, None, None, None]
)

###########################################################

POSTMock = namedtuple(
    "POSTMock",
    "get",
    defaults=[lambda orignal_url: FSL_HOME]
)

GETMock = namedtuple(
    "GETMock",
    "get",
    # defaults=[lambda *args: FSL_SHORT if args[0]=='short_url' else None]
    defaults=[lambda *args: FSL_SHORT if args[0]=='short_url' else None]
)

RequestMock = namedtuple(
    'RequestMock',
    ['POST', 'GET','user_agent', 'path', 'method'],
    defaults=[
        POSTMock(),
        dict(short_url=FSL_SHORT),
        UserAgentMock(),
        FSL_SHORT, 
        'POST'
        ]
)


HelperTests = namedtuple(
    "HelperTests",[
        "original_url_fsl_home",
        "original_url_fsl_python",
        "browser",
        "user_agent",
        "http_post",
        "http_get",
        "http_request",
        "inexistent_urls",
        "invalid_url",
        "fsl_short",
    ],
    defaults=[
        FSL_HOME,
        FSL_PYTHON,
        BrowserMock,
        UserAgentMock,
        POSTMock,
        GETMock,
        RequestMock,
        INEXISTENT_URLS,
        INVALID_URL,
        FSL_SHORT
    ] 
)

helper_tests = HelperTests()
