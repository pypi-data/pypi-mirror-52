# smockrawl

Basic Smockeo API crawler.

## Usage:

**Initialisation:**
`mySmockeo = Smockeo(username, password, detectorId, loop, session)`

Where `loop` is an asyncio event loop and `session` an aiohttp session. Have a look at the code in `__main__.py` to
see how this can work. 

**Authentication:**
`mySmockeo.authenticate()`

**Poll the sensor:**
`mySmockeo.poll()`

Following this, properties such as the sensor state, battery level or the last alarm can be read from the object.

An info reading can be printed with:
`mySmockeo.print_status()`


