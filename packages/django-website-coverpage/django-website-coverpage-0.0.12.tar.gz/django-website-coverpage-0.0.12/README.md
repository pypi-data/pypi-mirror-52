django-website-coverpage
====

Here in Thailand, it is customary for websites to show a cover page to celebrate national events, for example the King's birthday. This very simple app does just that.

### How it works:

- Website staff add details of coverpages via the admin interface. Each coverpage can have custom HTML, CSS and a start and end datetime.

- When a page is loaded, and a valid coverpage is available (i.e. the time now is between the start and end datetime), the coverpage is displayed.

Note #1: this app uses caching for speed. It is highly recommended you have caching enabled in your project.

Note #2: this app uses a cookie, and not the user's session. This is because the session is refreshed when logging in or out, and showing the coverpage again in this scenario wouldn't make any sense.

### Installation:
```
pip install django-website-coverpage
```

Add the following to your settings.py INSTALLED_APPS:
```
'websitecoverpage'
```

Add the following to your settings.py TEMPLATES > OPTIONS > context_processors:
```
'websitecoverpage.context_processor.websitecoverpage'
```

Add the following to your settings.py:
```
# The following are defaults, change them if you need to,
# i.e. if you are happy with the defaults, you don't need
# to add anything to your settings.py

# To ignore certain URLs, add values to the 'ignore_urls' list:
#    e.g. ['/a/', '/b/'] ignores all paths that startswith('/a/') and ('/b/')
#         '/favicon.ico' and '/robots.txt' are added automatically

WEBSITE_COVERPAGE = {
    'cookie_name': 'coverpage',
    'ignore_urls': [],
}
```

Add the following to your templates, immediately after the `<body>` tag:
```
{% if websitecoverpage %}{% include 'coverpage/coverpage.html' %}{% endif %}
```



### Notes:
Is testing a pain because you need to keep clearing your cookies? Incognito mode is your friend.