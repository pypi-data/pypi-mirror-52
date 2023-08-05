# NOSpy - Official Python client for N.O.S.

## A brief introduction to N.O.S.

N.O.S. is a fast Network Object Store that stores objects as binary data.
The primary interface for NOS is HTTP/s.
N.O.S. is written in GO, and is designed for high performance.
This Python client aims to keep the objects as native as possible to python.
It provides a thin layer of abstraction just to keep things pythonic, but
the lower level HTTP api is always availble for you to use at your discretion.

## Installation

Install NOSpy via pip:
`pip install nospy`

## Setup & Usage

In order to use NOSpy you'll need to have a working NOS server setup, running and accessible via HTTP.

**NOTE:** NOS is not publicly available at the moment.

Connect to the NOS server:

```python
from nospy import NOSClient

nos = NOSClient("http://localhost:9900")
```
