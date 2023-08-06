# guess_logo
猜测网址的logo链接
Detection of logo url from any website.


# How to use.

```
from guess_logo import GuessLogo


url = 'http://www.txdkj.com/'


logos = GuessLogo.guess(url)
print(logos)
```