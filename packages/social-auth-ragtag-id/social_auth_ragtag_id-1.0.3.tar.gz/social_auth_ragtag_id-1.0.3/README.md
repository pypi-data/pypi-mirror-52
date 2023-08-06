# python-social-auth-ragtag-id

An OAuth2 backend for [python social auth](https://github.com/python-social-auth/social-core).

## Installation

```sh
pipenv install social_auth_ragtag_id
```

## Django Configuration

First, follow the instructions at http://python-social-auth.readthedocs.io/en/latest/configuration/django.html.

Then, add this backed to `AUTHENTICATION_BACKENDS`:

```python
AUTHENTICATION_BACKENDS = (
  ...
  'social_auth_ragtag_id.backends.RagtagOAuth2',
  ...
  'django.contrib.auth.backends.ModelBackend',
)
```

Finally, add the client ID and secret:

```python
SOCIAL_AUTH_RAGTAG_KEY = 'xxxxxxxxxxx'
SOCIAL_AUTH_RAGTAG_SECRET = 'xxxxxxxxxxx'
```

These can be obtained from a member of Ragtag staff.

Assuming the default URL setup from social_core, you can now login at `/login/ragtag/`.

Optionally you may define `SOCIAL_AUTH_RAGTAG_SCOPES` to limit which data your app needs access to. Available scopes can be seen at https://id.ragtag.org/api/scopes/. For example:

```python
SOCIAL_AUTH_RAGTAG_SCOPES = ['identity', 'email']
```

And you may define `SOCIAL_AUTH_RAGTAG_APPROVAL_PROMPT` as `force` to force the approval screen to appear every time the user signs in.

```python
SOCIAL_AUTH_RAGTAG_APPROVAL_PROMPT = 'force'
```
