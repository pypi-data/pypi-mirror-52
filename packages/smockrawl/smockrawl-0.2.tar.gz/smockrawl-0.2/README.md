# smockrawl

Basic Smockeo API crawler.

## Usage:

Initialisation:
`mySmockeo = Smockeo(username, password, smockeo_id)`

Authentication:
`mySmockeo.authenticate()`

Poll the sensor:
`mySmockeo.poll()`

Following this, properties such as the sensor state, battery level or the last alarm can be read from the object.

An info reading can be printed with:
`mySmockeo.print_status()`


