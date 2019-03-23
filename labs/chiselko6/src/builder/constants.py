import os


DIR = os.path.join(os.getcwd(), 'gen')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>{}</title>
  </head>
  <body>
    {}
  </body>
</html>
'''
