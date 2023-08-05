# itrsstatsd

## Overview
itrsstatd is a Python module for collecting custom application metrics.

It is intended for use with the Collection Agent and statsd-plugin.  The client sends metrics via UDP or TCP
to the agent which aggregates and reports the metrics every 10 seconds (by default).

## Specification
The client is based on the standard [statsd] protocol with the following enhancements:
- Dimensions (a.k.a. tags) can be added to all metrics or to specific metrics
- Unit of measure can be specified per metric

## Requirements
- Python 3.7

## Installation
```
pip install itrsstatsd
```

## Module documentation
\# How to get and use a statsd API handle  
$ pydoc3 itrsstatsd  
  
\# API documentation  
$ pydoc3 itrsstatsd.api

\# Units of measure documentation  
$ pydoc3 itrsstatsd.units

## Usage

```python
from itrsstatsd import build_statsd
from itrsstatsd.api import Api
from itrsstatsd.units import Unit

# Create an instance of the client that sends to localhost:8125
statsd = build_statsd()

# Or create an instance with a non-default statsd server and port
# statsd = build_statsd(hostname="127.0.0.1", port=9125)

# Or create an instance that uses TCP instead of the default UDP
# statsd = build_statsd(protocol='tcp')

# Optionally add dimensions to all metrics
statsd.default_dimensions(custom1="abc", custom2="xyz")
 
# Increment a counter
statsd.increment("failed_logins")

# Decrement a counter
statsd.decrement("thread_count")

# Adjust a counter
statsd.count("items_processed", 5)

# Set a gauge with an absolute value
statsd.gauge("cache_size", 123.5)

# Set a gauge with a unit of measure
statsd.gauge("cache_size", 52.5, Unit.Megabytes)

# Adjust a gauge
statsd.gauge("tank", -5.0)

# Count unique values in a bucket
statsd.unique("unique_logins", "alice")

# Record a timer
statsd.timer("db_query_time", 56)

# Include dimensions with a metric
statsd.increment("failed_logins", dim1="a", dim2="b")

# Close the client when no longer needed
statsd.close()
```

### Statsd Server

When building a client, if the server/port of the statsd server are not explicitly provided, the builder will look for 
the `STATSD_SERVER` and `STATSD_PORT` environment variables.  If they are not present, the client will default to 
localhost:8125.

### Adding Dimensions

There are three ways to add dimensions to a metric:
- **Default Dimensions**:  Custom dimensions specified when building the client. These are applied to every metric (see
  example above).
- **Per-metric Dimensions**:  Custom dimensions specified for one metric, for example:
  ```
  statsd.increment("failed_logins", region="Europe");
  ```
- **Environmental Dimensions**:  The client will create dimensions from specific environment variables based on the 
  deployment environment:

  - Kubernetes/OpenShift:
  
    | Variable       | Dimension      |
    | ---------------|----------------|
    | POD_NAME       | pod_name       |
    | CONTAINER_NAME | container_name |
    | NAMESPACE      | namespace      |
    
  - Default (if no other environment type is detected): 
    
    | Variable       | Dimension      |
    | ---------------|----------------|
    | APP_NAME       | app_name       |
    | HOSTNAME       | hostname       |
    
### Sampling Rate

When sampling high-frequency operations, it is possible to flood the statsd server with a large number of messages.  
To mitigate this impact, certain operations can use a sampling rate which causes the client to send a message for 
only _n_ percent of all invocations.  For example:

```python
def frequently_invoked_method():
    statsd.increment("metric", 0.5)
```

The client will send the increment message for approximately half of the times it is invoked.  In those instances,
the client includes the sampling rate in the message: `metric:1|c|@0.5`.  This instructs the server to multiply the 
value (1) by 2 to approximate the actual value.

This feature is available only for counters and timers.

### Sets

To count the number of unique items in a bucket/set:

```python
def login(username):
    statsd.unique("unique_logins", username)
```

The statsd server will track the number of unique values per reporting interval and publish as a counter metric. 

## Developer Info (omit from product docs)

### Install module on local machine
$ cd statsd-client-python  
$ pip3 install .

[statsd]: https://github.com/statsd/statsd