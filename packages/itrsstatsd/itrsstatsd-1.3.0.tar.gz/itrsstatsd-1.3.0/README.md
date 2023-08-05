# itrsstatsd

[![PyPI Version](https://img.shields.io/pypi/v/itrsstatsd)](https://pypi.org/project/itrsstatsd)

Python module for publishing custom metrics to an ITRS StatsD server.

The module is part of the [Orchestrated Netprobe][1] solution for collecting metrics in orchestrated environments.
See the [docs][1] for complete details.

## Requirements
- Python 3.7

## Installation

The module is available via PyPI:
```
pip3 install itrsstatsd
```

## Module Documentation

How to get and use a statsd API handle:  
```
pydoc3 itrsstatsd  
```

API documentation:  
```
pydoc3 itrsstatsd.api
```

Units of measure documentation:
```  
pydoc3 itrsstatsd.units
```

## Getting Started

```python
from itrsstatsd import build_statsd
from itrsstatsd.units import Unit

# Create an instance of the client that sends to localhost:8125
statsd = build_statsd()

# Optionally add dimension(s) to all metrics
statsd.default_dimensions(app_name="pyapp")
 
# Record some metrics
statsd.increment("failed_logins")
statsd.gauge("cache_size", 52.5, Unit.Megabytes)
statsd.timer("query_time", 56)
```

Refer to the pydoc for complete usage details.


[1]: https://docs.itrsgroup.com/docs/orchestrated-netprobe