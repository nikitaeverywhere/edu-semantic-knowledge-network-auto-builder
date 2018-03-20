# Auto Semantic Knowledge Network Builder

An implementation of [Nikita Savchenko's](https://nikita.tk) semantic knowledge network building 
algorithm.

Preview
-------

Article [Ink helps drive democracy in Asia](http://news.bbc.co.uk/2/hi/technology/4276125.stm):

![2018-02-01_142301](https://user-images.githubusercontent.com/4989256/35678359-af18c3d2-075b-11e8-908b-49e8d9a495bc.png)

Composites from many articles:

![2018-02-01_125026](https://user-images.githubusercontent.com/4989256/35675268-108ba938-0750-11e8-9190-aaafe5a0210a.png)
![2018-02-01_130034](https://user-images.githubusercontent.com/4989256/35675269-10bd0280-0750-11e8-925d-75078583751a.png)

Requirements & Setup
--------------------

1. Python v3 with pip3
2. Git

Clone this repository and install all prerequisites:

```bash
git clone --recursive https://github.com/ZitRos/edu-semantic-knowledge-network-auto-builder
cd edu-semantic-knowledge-network-auto-builder
pip3 install -r requirements.txt
py setup.py
```

Additionally, when running scripts from this repository, `nltk` may ask you to download more 
modules. Follow the command line instructions then.

To run a sample graph building from multiple texts, put those texts in `input` directory and use this
to generate graph to `output` directory:

```bash
py process.py
```

License
-------

Apache License v2 © [Nikita Savchenko](https://nikita.tk)
