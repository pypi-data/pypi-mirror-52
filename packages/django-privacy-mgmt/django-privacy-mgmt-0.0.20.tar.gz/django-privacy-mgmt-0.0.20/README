# Django Privacy Mgmt

This python module is open-source, available here: https://gitlab.com/what-digital/django-privacy-mgmt/


## Versioning and Packages

- versioning is done in versioning in `django_privacy_mgmt/__init__.py`
- for each version a tag is added to the gitlab repository in the form of `^(\d+\.)?(\d+\.)?(\*|\d+)$`, example: 0.0.10

- There is a PyPI version which relies on the gitlab tags (the download_url relies on correct gitlab tags being set): https://pypi.org/project/django-privacy-mgmt/
- There is a DjangoCMS / Divio Marketplace add-on which also relies on the gitlab tags: https://marketplace.django-cms.org/en/addons/browse/django-privacy-mgmt/

In order to release a new version of the Divio add-on:

- Increment version number in `addons-dev/django-privacy-mgmt/django_privacy_mgmt/__init__.py`
- divio addon validate
- divio addon upload
- Then git add, commit and tag with the version number and push to the repo

```
git add .
git commit -m "<message>"
git tag 0.0.XX
git push origin 0.0.19
```

Then, in order to release a new pypi version:

- python3 setup.py sdist bdist_wheel
- twine upload --repository-url https://test.pypi.org/legacy/ dist/*
- twine upload dist/*

### Development

- Run `pip install -e ../django_privacy_mgmt/` in your demo project
- You can open django_privacy_mgmt in pycharm and set the python interpreter of the demo project to get proper django support and code completion.

## Intro - what is this all about?

### What is GDPR

GDPR is an EU law that requires public and private organisations to comply with EU user data best practises if one of the following applies (https://francoischarlet.ch/2017/gdpr-in-switzerland-10-steps-to-take/)

- Does your organisation offer services or goods to individuals in the EU?
- Does your organisation process or participate in processing of personal data of EU individuals, for itself or on behalf of another organisation?
- Does your organisation monitor online behaviour of users based in the EU?
- Does your organisation analyse the activities of EU users when they are using your organisation’s app or browsing its website?

To fulfill the new GDPR guidelines APG would need to implement a cookie alert addon into their website.

### GDPR Requirements

- user needs to be able to give consent before GDPR-relevant scripts are executed and such cookies are stored in the user's browser
- user needs to be able to see which GDPR-relevant scripts and such cookies are active on the site
- user needs to be able to deactivate these scripts
- the admin should be able to manage a list of GDPR-relevant scripts in the django admin backend.

### GDPR Trends

Loosely paraphrased from https://piwik.pro/blog/how-will-gdpr-affect-your-web-analytics-tracking/:

It appears that not every type of tracking will require consent from your users. The current form of ePrivacy (Regulation on Privacy and Electronic Communications) makes an exception for personal data used for web analytics purposes. So, if you take advantage of a web analytics tool that utilizes the collected data only to examine the performance of your website, you probably don’t need to worry about this part.

However, if you pass your analytics data to other AdTech and MarTech platforms (such as DSP or CDP), use remarketing pixels and tracking codes, or personalize your website content based on user behavior, you’ll certainly need to ask for consent for each of these activities.

### Implementation of these GDPR Trends / GDPR-relevant Script and Cookie Categories

From how others have implemented GDPR management user interface and from our conversations with compliance experts, we have come to the conclusion that we can simplify the user interface to give the user control over three categories of scripts:

- Essentials or Mandatory (cannot be deactivated): These cookies and services are necessary for you to visit our online services and use their features. Without them, you cannot use services, such as login (sessions), language settings, shopping cart and privacy settings, as well as services related to security. Except for login (sessions), no information of a sensitive nature that can be used to identify you will be collected.
- Statistics (default: activated, user can opt out): These cookies and services collect information about how you use our online services, such as which functions and pages you use most often. This data can help us optimise our online services, for example, or simplify navigation. They are also used to inform partners whether you reached our website through a partner site, and whether your visit led to using one of our offers; however, no information will be recorded that can be used to personally identify you.
- Marketing (default: deactivated, user can opt in): These cookies and services allow the advertising platforms used by APG|SGA to show you ads that are relevant to your interests, or in certain situations, prevent ads from being shown to you. They are also responsible for preventing ads from being displayed repeatedly and ensuring that ads are correctly displayed.

## Limitations of Cookie Management

While it is possible to 'see' some cookies via browser's javascript interface, some cookies cannot be accessed by the website. Therefore, once some tracking / marketing scripts such as a Facebook Pixel have executed after page load, it is impossible to programmatically remove those cookies (applies to http only, third party cookies)

## Dependencies

- django-sekizai ([read more](https://django-sekizai.readthedocs.io/en/latest/)) is used which provides the template tag `{% addtoblock "js" %}`. This allows you to have javascript (or other code) in arbitrary places in templates and then output that code in one single place (preferrably at the end of the `body` tag in the root template) as a possible page speed optimisation strategy. If you want to handle all javascript code in your frontend application, just remove the sekizai tags from the template files.
- make sure you have [django-parler](https://github.com/django-parler/django-parler#installing-django-parler) configured properly if you want to use model translations
- frontend requirements, make sure to include these or change the static resources and templates to your own frontend stack
   - jQuery
   - bootstrap3

## Setup

- Put 'django.contrib.sites' into your `INSTALLED_APPS` setting and put `SITE_ID = 1` into your `settings.py` as well.
- Put `sekizai` into your `INSTALLED_APPS` setting and add `'sekizai.context_processors.sekizai',` to `TEMPLATES[{'OPTIONS': { 'context_processors': [ ... ]}}]` in `settings.py`
- install the add-on on divio.com or via pypi
- add 'django.contrib.sites' to `INSTALLED_APPS`
- add `django_privacy_mgmt` to `INSTALLED_APPS`
- update your templates/django_privacy_mgmt to reflect your frontend toolchain situation
- load the template tag library by adding `{% load privacy %}` to your template  and then add `{% render_privacy_api %}` to the very top of your root html template's code (it should load before any other javascript so that the API is available)
- add `{% render_privacy_settings_modal %}` to the bottom where the other javascript inclusions reside
- add something like `{% render_privacy_settings_modal_link %}` somewhere on your site. Probably it will be footer in most of cases where user can click and manage privacy settings.
- optionally, you can also add `{% render_privacy_banner %}` to a template which will show a nasty banner at the bottom of the page (its just an example based on bootstrap3, you will have to adapt / style it to reflect your frontend setup)

- Then check what kind of tracking items your website is using (either in the templates or via Google Tag Manager or in any imaginable other way) and add them in the "Django Privacy Mgmt" section of the Django Admin interface to the list of 'Tracking Items'. This is necessary so that we can show a list of tracking items to the user in the 'privacy settings' modal.
- Then implement conditional logic that enables or disables the tracking items that you identified in the previous step (see next chapter).

### settings.py configuration

```
...

INSTALLED_APPS = [
    ...
    'django.contrib.sites',
    'sekizai',
    'django_privacy_mgmt',
]

...

SITE_ID = 1

...

TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

...

```


## TODOs

- Remove django-sekizai as a dependency as modern frontend strategies dont't require javascript to be in the footer of the html document anymore (instead deferred / async loading of assets and chunking is used)
- Make the use of django sites optional (separate migration, conditional field in form, model (?)) 


## Cookie and Third-Party Script Management

There are different ways how Tracking Items are added to a website. Here are a couple of common cases:

- Google Tag Manager (or any other tag manager)
- Directly in a template (for example `base.html` or `includes/ga.html`)
- In a javascript file
- ...?

### Simple example

Here is a simple example how you can control any third-party scripts (here it's the Google Analytics base tag) via the `django-privacy-mgmt` API:

```
<script>
    // There are three different cookie levels: ESSENTIALS (always on), STATISTICS (opt-out) and MARKETING (opt-in)
    if (django_privacy_mgmt && django_privacy_mgmt.getPreference('STATISTICS')) {

        // here goes the tracking script
        console.log('Activating Google Analytics base code because the user is opted-in (possibly by default).');
        (function (b, o, i, l, e, r) {

            ...

        ga('send', 'pageview');
    }
</script>
```

### Google Tag Manager example

#### How to install GTM

Before continue to read please make sure that you are familiar with [Google Tag Manager](https://developers.google.com/tag-manager/devguide).
Pay attention at topic with variables and triggers.

- Place the `<script>` code snippet in the `<head>` of your web page's HTML output, preferably as close to the opening `<head>` tag as possible, but below any dataLayer declarations.
- Place the `<noscript>` code snippet immediately after the `<body>` tag in your HTML output.

This instruction but with code you can also find at your [personal tag manager account](https://tagmanager.google.com/), but you need to have container.
When you will enter to your container in the top right corner you can find identifier of your contaner something like `GTM-XXXXXXX`.
Click on it follow instructions.

Your `<head>` tag will be similliar to next code:
```
{% load privacy %}

<!doctype html>
<html>
<head>
    {% include "includes/gtm_head.html" %}

    {% render_privacy_api %}

    {% block datalayer %}
        <script>
            window.dataLayer = window.dataLayer || [];

            var statisticsTrackingItemCategory = django_privacy_mgmt.getPreference('STATISTICS');
            var personalizationTrackingItemCategory = django_privacy_mgmt.getPreference('MARKETING');
            dataLayer.push({
                'statisticsTrackingItemCategory': statisticsTrackingItemCategory,
                'personalizationTrackingItemCategory': personalizationTrackingItemCategory

            });
        </script>
    {% endblock datalayer %}

    ...
</head>
<body>
    {% include "includes/gtm_body.html" %}
    ....
</body>
</html>

```

Pay attention at next lines, where we defined `statisticsTrackingItemCategory` and `personalizationTrackingItemCategory` variables.
It will be used to [dataLayer variables](https://developers.google.com/tag-manager/devguide#datalayer).
Then create at your container one folder `GDPR compliance` where you will store your tags and variables.
The next steps will be creating Data Layer Variables and Triggers.

##### Creating Variables

* Create at Variables sidebar next variable with the name `GDPR tracking item type - Statistics` with variable type `Data Layer variable` and Data Layer Variable Name `statisticsTrackingItemCategory`
* Create at Variables sidebar next variable with the name `GDPR tracking item type - Personalisation` with variable type `Data Layer variable` and Data Layer Variable Name `personalizationTrackingItemCategory`

##### Creating Triggers
As minimum we need 2 triggers where we will check that tracking stats or marketing is on.

* Create at Triggers sidebar next trigger with the name `Statistics DataLayer is true`, choose one type of Page View(depends on your project), This trigger fires on `Some DOM Ready events`
and add choose that your `GDPR tracking item type - Statistics`(at first column) `equals`(at second column) `true`(at third column).
* Create at Triggers sidebar next trigger with the name `Marketing DataLayer is true`, choose one type of Page View(depends on your project), This trigger fires on `Some DOM Ready events`
and add choose that your `GDPR tracking item type - Personalisation`(at first column) `equals`(at second column) `true`(at third column).

Some projects can have additional trigger on tag.
For that case we need to create triggers with `false` logic and add it as exception.
For example you need to track click on all link with ending `.pdf`. How can we block this firing? We need to add as exception(blocking trigger) to this tag.
But before we need to create in the same way triggers with `false` logic. It will be `Statistics DataLayer is true` and `Marketing DataLayer is false`.

And add this logic as a exception. If you do not understand, please make sure that you read everything about trigger at Google Tag Manager.

##### General recommendations and useful advises
Can sure that you add localhost, stage to environments at GTM. It is under ADMIN -> Environments.
When you add `localhost` for local dev machine, now you can preview you working changes before deploy to stage, production.
For preview change you can click on "Preview" button or do it via Environments and select "Share link". Via this link you can also disable preview and debug mode.
