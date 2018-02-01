# Auto Semantic Knowledge Network Builder

An implementation of [Nikita Savchenko's](https://nikita.tk) semantic knowledge network building 
algorithm.

Preview
-------

Article [Ink helps drive democracy in Asia](http://news.bbc.co.uk/2/hi/technology/4276125.stm):

![Graph](https://user-images.githubusercontent.com/4989256/35646980-ca425876-06d9-11e8-9c06-2e63b1ed2981.png)

Composites from many articles:

![2018-02-01_125026](https://user-images.githubusercontent.com/4989256/35675268-108ba938-0750-11e8-9190-aaafe5a0210a.png)
![2018-02-01_130034](https://user-images.githubusercontent.com/4989256/35675269-10bd0280-0750-11e8-925d-75078583751a.png)

Requirements & Setup
------------

1. Python v3 with pip3
2. Git

Clone this repository and install requirements:

```bash
git clone --recursive https://github.com/ZitRos/edu-semantic-knowledge-network-auto-builder
cd edu-semantic-knowledge-network-auto-builder
pip3 install -r requirements.txt
```

Additionally, when running scripts from this repository, `nltk` may ask you to download more 
modules. Follow the command line instructions then.

License
-------

Apache License v2 © [Nikita Savchenko](https://nikita.tk)