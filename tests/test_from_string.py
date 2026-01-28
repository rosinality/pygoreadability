from pygoreadability import from_string


def test_from_string_accepts_null_bytes():
    html = """<!doctype html>
    <html>
      <head>
        <title>Null Byte Test</title>
      </head>
      <body>
        <p>Hello\x00World</p>
      </body>
    </html>
    """
    article = from_string(html, url="https://example.com")
    assert article.title == "Null Byte Test"
