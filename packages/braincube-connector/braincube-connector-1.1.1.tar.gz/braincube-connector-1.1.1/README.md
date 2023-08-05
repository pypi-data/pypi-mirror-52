# Braincube API for Python

This connector allow a braincube user to access his data.

## Pre requisites

The connector is supported for python 3+

## Installation

```
pip install braincube-connector
```

## Running the  connector

### First run

>The first time the connector is launch, it will retrieve an oauth2 access token.

You will need to 
* log in to your braincube, and go to "User" > Configure > Applications
* Add an application (set a name as you wish and `https://localhost:5000/token` as the redirect url)
* Clic on the newly created application and copy the `Client ID` and `Client Secret` fields
* Run the connector

```python
from braincube import connector as co
braincube_connector = co.get_data_collector() 
```
* You will be asked to fill a config file with the `Client ID` and `Client Secret` from above
  * If you connect to `subdomain.mybraincube.com` (instead of `mybraincube.com`) then you also have to fill the `domain` key with `subdomain.mybraincube.com`
* Re-run the connector (you need to accept the browser security exception as we running on a self-signed ssl certificate)

### Connector usage
The connector comes in 2 versions:
* A raw version return plain python objects
* A Panda version return pandas dataframes

```python
import datetime
from braincube import connector as co

# Retrieve a connector
braincube_connector = co.get_data_collector() # by defaut the panda connector is used
braincube_connector_raw = co.get_data_collector(format_type="raw") # allow to get the raw connector

# Get the braincube list
braincube_connector.get_braincube_list()

# Get a braincube object
my_braincube = braincube_connector.get_braincube("my_braincube_name")

# Get the memory base list
my_braincube.get_memorybase_list()
# or
braincube_connector("my_braincube_name").get_memorybase_list()

# Get a memory base object
my_memory_base = my_braincube.get_memorybase("my_memory_base_id")

# Return the id of the variable which is used to order the memorybase (not necessarily the memory base reference)
my_memory_base.get_memorybase_order_variable()

# Return a list of variable id and names
my_memory_base.get_variable_list()

# Retrieve datas from all variables of the memorybase since 1 jan 2012
# Specifiying the starting date is mandatory if no ending date is specified datetime.now() is used
my_memory_base.retrieve_all_variables_from_memory_base(datetime.date(2012,1,1)) 

# To retrieve only some variable since 1 jan 2012
my_memory_base.retrieve_data([var_id1, var_id2], datetime.date(2012,1,1))
```


