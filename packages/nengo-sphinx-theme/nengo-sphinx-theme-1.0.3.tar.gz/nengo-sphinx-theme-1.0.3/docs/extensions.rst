***************
Extension tests
***************

This page tests the extensions that are part of this theme.

Versioning
==========

This extension is always used
if ``releases`` are passed to the Sphinx build.

:doc:`deeply/nested/testing/page`
versioned links work properly.

Default resolution
==================

This extension can be enabled by adding
``"nengo_sphinx_theme.ext.resolvedefaults"``
to the ``extensions`` list in ``conf.py``.

Autodoc with default resolution:

.. autoclass:: nengo_sphinx_theme.ext.resolvedefaults.TestClass
