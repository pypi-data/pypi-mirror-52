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
from guess_logo import Logo
height = 256
width = 512
source = 'demo/ifengLogo.png'
target = 'demo/ifengLogo_{}_{}.png'.format(width, height)
Logo.resize(source, target, width, height, bgcolor='transparent')


# 替换白色为透明
from guess_logo import ColorLogo
source = 'demo/logo.jpeg'
target = 'demo/logo.transparent.png'
ColorLogo.replace(source, target)

```