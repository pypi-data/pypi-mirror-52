# InfomaniakNewsletterClient
Integration of Infomaniak Newsletter API in Python
https://newsletter.infomaniak.com/docs/index.html

### Installation
```
virtualenv venv
venv\Scripts\activate

pip install infomaniakclient
```

### Usage
```
from infomaniakclient import Client
from infomaniakclient import Action

r = Client('API_KEY', 'API_SECRET')
```

You'll find some examples in this repos examples.py file.