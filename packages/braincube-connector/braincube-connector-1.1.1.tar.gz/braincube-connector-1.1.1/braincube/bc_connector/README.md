# PandasConnector

## Installation
```
pip install braincube
```
## Running
```
from braincube import connector as co
```
### Get data from web
```
data = co.retrieve_data_from_web()
```
### Make connection with Braincube
```
connector = co.connect()
#or
connector = co.connect("your token")
```
> By default, the data returned will be a pandas's dataframe to be easily readable.
However you can also specify an option to return the data in raw
```
connector = co.connect(format_type="raw")
#or
connector = co.connect("your token", "raw")
```

### Use the python API
* **Get informations**

    > All these methods return an object with some informations.
    You can display it as below or store it in variables and use it into your code.
     ```
        #To get useful informations
        connector.get_token()
        connector.get_braincube_list()
        connector.get_memorybase_list("name of the braincube")
        connector.get_memorybase_order_variable("name of the braincube", memorybaseID)
        connector.get_variable_list("name of the braincube", memorybaseID)
     ```

* **Retrieve data**

    > To retrive data, just specifie the right parameters to target your data.
    Then choose a time interval for your data (take the current date if no end_date specified).
    You can display it like below or store it in a variable to use it.
    ```
        #To retrieve data
        connector.retrieve_data("name of the braincube", memorybaseID, [variableId, variableId...], datetime(start_date), optional datetime(end_date))
        connector.retrieve_all_variables_from_memorybase("name of the braincube", memorybaseID, datetime(start_date), optional datetime(end_date))
    ```
    
* **API Objects**

    > To simplify the choice of parameters, objects are available to store parameters for you.
    By using them, you can use all the methods of connector as above, without passing the parameters used to build the objects.
    ```
        braincube = connector.create_braincube("name of the braincube")
        memorybase = connector.create_memorybase("name of the braincube", memorybaseID)
        variable_set = connector.create_variable_set("name of the braincube", memorybaseID, [variableId, variableId...])
        # Examples :
        braincube.get_memorybase_list()
        memorybase.create_variable_set([variableId, variableId...])
        variable_set.retrieve_data(datetime(2015, 5, 20), datetime(2015, 5, 25))
        variable_set.get_selected_variables() # New, return a dataframe listing the variables of the set
    ```
