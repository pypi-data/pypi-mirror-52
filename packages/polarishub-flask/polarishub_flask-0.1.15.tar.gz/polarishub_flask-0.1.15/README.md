# PolarisHub (Flask Version)
**[EN]** [[中文版本]](README-CN.md)

1. [What is PolarisHub](#what-is-polarishub)
2. [How to install PolarisHub](#how-to-install-polarishub)
3. [How to run PolarisHub](#how-to-run-polarishub)
4. [The advantages of PolarisHub](#the-advantages-of-polarishub)
5. [The inspiration of PolarisHub](#the-inspiration-of-polarishub)
6. [Future plan](#future-plan)


## What is PolarisHub

PolarisHub is a **free, fast, easy, secure** file transfer tool. The current version is based on *Flask (Python)*, which can be deployed on all computers with *Python*. With the command *phub*, the **PolarisHub** will start, and you can manage your **PolarisHub** with *GUI of web browser* (url: *http://localhost:5000/*). You can share your files using *url links* and *QR Code*, whoever in the same network can access your shared files. You can also gracefully shutdown **PolarisHub** with one click! 

## How to install PolarisHub

### Install with *pip* (Recommended)

1. Make sure you have the *Python3* and *pip* properly installed.
2. Run `$ pip install polarishub_flask` or `$ pip install polarishub_flask==X.X.X` (version code).
3. Done! 

### Download the source code

1. `git clone https://github.com/XieGuochao/polarishub_flask.git`

## How to run PolarisHub

### Run with *pip* installation (Recommended)

1. `$ phub` (Run `$ phub -h` for more information on the optional arguments)

### Run with source code

1. `$ cd polarishub_flask`
2. `$ python3 fastrun.py` (Run `$ python3 fastrun.py -h` for more information on the optional argumetns)

## The advantages of PolarisHub

(May use a graph)

### Compared with *OneDrive*, *iCloud*, or similar cloud file storage

1. **Fast**. Taking the advantage of LAN with almost unlimited bandwidth, the file transfer using **PolarisHub** can reach the speed limit of the network, i.e. X MB/s ~ XX MB/s. 
2. **Private**. **PolarisHub** is a decentralized platform, which originally does not provide a cloud center. Therefore, you own the **100% authority** of your files, and no one can perceive your transfer on the application layer.
3. **Secure**. **PolarisHub** is an open-source project, where everyone can contribute to fix the potential bugs and there will not be privacy compromise problem.

### Compared with *WeChat*
1. **Unlimited size of files**. We are no longer worried about the size of our files, which is restricted by *WeChat*.
2. **Fast**. The same as indicated above.

### Compared with *AirDrop*
1. **Free**. No limitation of the Apple hardware, we are building a software that every computer can use!
2. **Longer Distance**. As long as the transfer is within a LAN, it can even be done between *the upper campus and the lower campus* and across every classroom and building!

### Other advantages
1. **Easy Deployment**. **PolarisHub** can be deployed on every computer installed with *Python* using *pip*. There is no compilation requirement for it.

## The inspiration of PolarisHub

The inspiration of PolarisHub comes from the annoying experience of using the current file transfer tools, as discussed above. Therefore, we are trying to build a software which overcomes all the disadvantages of other tools, a **free, fast, easy, secure** tool.

## Future plan

We welcome everyone who is interested in **PolarisHub** to join us: **Polaris Studio**! You can find us on GitHub *https://github.com/XieGuochao/polarishub_flask* or send email to *st_polarisstudio@link.cuhk.edu.cn*.

1. **Go Version**. We are going to refactor **PolarisHub** in *Golang*, which can be compiled and deployed to every platform without *Python*.
2. **Public Server for host consultation**. We are going to build a public server such that everyone can share their file links (in local network) on it.
3. **More powerful PolarisHub**. More features will be added, such as *access password*, and etc..

## Contributors:
- Guochao Xie
- Senyue Hao
- Yongqi Zhang