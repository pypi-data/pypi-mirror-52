python-kaiterra-async-client
============================

Python 3 client for retrieving readings from your Laser Egg or Sensedge using the `Kaiterra REST API <https://www.kaiterra.com/dev>`__.

To use it, you'll first need to create an account at the `Kaiterra Dashboard <https://dashboard.kaiterra.cn/>`__, then create an API key under Settings -> Profile -> Developer.


Getting Started
-------------------

Install the library using pip:

.. code:: bash

	pip install kaiterra-async-client

Example
-------------

Here's some code to retrieve readings from a couple test devices, one Laser Egg and one Sensedge:

.. code:: python

	import aiohttp
	from kaiterra_async_client import KaiterraAPIClient

	async with aiohttp.ClientSession() as session:
		client = KaiterraAPIClient(session, api_key='YOUR_API_KEY_HERE')
		r = await client.get_latest_sensor_readings([
			'/lasereggs/00000000-0001-0001-0000-00007e57c0de',
			'/sensedges/00000000-0031-0001-0000-00007e57c0de',
		])
		print(r)

Development
-------------

Source code, issues, and pull requests are managed using `Github <https://github.com/Michsior14/python-kaiterra-async-client>`__.
