
misc notes
----------

influx table query: `SELECT last(value), max(value), min(value) FROM "magrathea"."autogen"."temperature" where time > now()-1d GROUP BY "name"`

TODO
----

* tasks on existsing widgets
    * clock
        * if date is hidden: make the clock great again
    * idokep days
        * show city
    * idokep hours
        * show city
        * show wind info
    * calendar
        * google cal integration
        * holidays (https://calendarific.com/)
    * server status
        * ordering
* move more than on widget simultaneously
    * select them somehow
* export / import widget settings
* new widgets
    * transmission
    * influx graph
    * network speed
        * need some lib to do with on the router
* proper install guide
* proper dev guide
* widget plugin system
    * write usage guide
    * how is the backend part?
    * plugins:
        * tvs ep tracker
        * room temperature
* zeroconf
    * host:port info
        * environment set by uwsgi conf
        * app config
* desktop client with electron
* android client with WebView
* move dashboard id from localstorage to url
    * why?
