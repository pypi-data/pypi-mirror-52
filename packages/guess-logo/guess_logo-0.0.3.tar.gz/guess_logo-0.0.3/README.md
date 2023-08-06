# guess_logo
猜测网址的logo链接
Detection of logo url from any website.

# How to install.
```
pip3 install guess_logo
```

# How to use.

```
from guess_logo import GuessLogo


url = 'http://www.txdkj.com/'


logos = GuessLogo.guess(url)
print(logos)

# 调整logo大小
height = 256
width = 512
source = 'demo/ifengLogo.png'
target = 'demo/ifengLogo_{}_{}.png'.format(width, height)
Logo.resize(source, target, width, height, bgcolor='transparent')
```