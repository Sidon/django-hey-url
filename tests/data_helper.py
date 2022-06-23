from collections import namedtuple


DEFAULT_BROWSER = 'chrome'
BrowserMock = namedtuple(
    "BrowserMock",
    "family",
    defaults=[DEFAULT_BROWSER]
)
BROWSER_MOCK = BrowserMock()
UserAgentMock = namedtuple(
    "UserAgentMock",
    ["browser", "is_mobile", "is_tablet", "is_pc"],
    defaults = [BROWSER_MOCK , None, None, None]
)
USER_AGENT_MOCK = UserAgentMock()
