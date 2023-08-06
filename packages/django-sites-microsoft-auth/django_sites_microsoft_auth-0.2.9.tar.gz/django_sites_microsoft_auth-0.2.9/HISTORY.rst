=======
History
=======

0.2.9 (2019-09-23)
------------------

* Update cache to work on a per-site basis.

0.2.8 (2019-09-23)
------------------

* Fix bug where migrations were relying on undefined ordering.

0.2.7 (2019-09-23)
------------------

* Fix tests to work with new default for login_enabled.

0.2.6 (2019-09-23)
------------------

* Make sure migrations for sites_microsoft_auth run after migrations for sites framework.

0.2.5 (2019-09-23)
------------------

* Add SiteConfiguration object for all sites during initial migrate.
* Change default for login_enabled to False

0.2.4 (2019-09-23)
------------------

* Fix bug where 'MicrosoftAuthenticationBackend` is not respecting `site` on the MicrosoftAccount model.

0.2.3 (2019-09-23)
------------------

* Fixed bug with `MicrosoftAuthenticationBackend` not restricting users to their respective sites.

0.2.2 (2019-09-23)
------------------

* Updated package name to `sites_microsoft_auth` from `microsoft_auth`

0.2.1 (2019-09-23)
------------------

* Updated documentation.

0.2.0 (2019-09-23)
------------------

* First working release on PyPi
