html_stripper: Strip html down to text in various ways.
=======================================================

html_stripper is a simple Python module to strip HTML down to plain text. In addition, it also parses HTML entities propperly. For example, "&#39;" would become "'".

.. code-block:: python

    >>> import html_stripper
    >>>
    >>> html = "<h1>This is a test</h1><p>Of the emergency broadcast system.</p>"
    >>> text = html_stripper.extract_text(html)
    >>> print(text)

