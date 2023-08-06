GitHub Provider
===============

This is a provider for [gqlmod](https://pypi.org/project/gqlmod/) that adds the
`github` provider.

The provider itself just takes a `token`, which is the Bearer token to send. 
There's a few ways to get this:

* Personal Access Token: Head to the [appropriate settings page](https://github.com/settings/tokens) and just ask GitHub for a token
* OAuth: [Implement the appropriate callbacks](https://developer.github.com/v3/guides/basics-of-authentication/) and get a token
* Username and password: GitHub has an [HTTP Basic Authentication endpoint](https://developer.github.com/v3/auth/#via-username-and-password) for username/password authentication (does not work with SAML SSO or two-factor authentication)
* Private Key: To act as an app, download your private key and follow the [private key flow](https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/) to produce a JWT

Previews
--------

GitHub API previews are handled automatically. If your query invokes an API
preview, the appropriate flags will be sent as part of the request.

Be sure to use some kind of CI system to make sure changes to previews won't
break your code.

The full list of previews can be found in [the API documentation](https://developer.github.com/v4/previews/).
