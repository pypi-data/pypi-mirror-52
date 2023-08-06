# rocketloghandler

Send your Python logs to RocketChat.

Implements a custom handler for the Python logging module.

For a full working example see `rocketlog_test.py`.

## Using Logging in multiple modules
Ensure there is a hierarchical structure in the logger name separated by dots. The name is set when calling 
`logging.getLogger`.

## Usage example
```python
import logging

from rocketloghandler.rocketloghandler import RocketLogHandler

rocketHandler = RocketLog(USER_ID, TOKEN, SERVER, CHANNEL_NAME, USER_ALIAS)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
rocketHandler.setFormatter(formatter)
log.addHandler(rocketHandler)
log.warning("Never say no to the panda! Otherwise: https://www.youtube.com/watch?v=XYz3sl0LEA4")
```

## Contributing
Feel free to contribute to this project. A 
[contribution guide](https://mygit.th-deg.de/fwahl/rocketlog/blob/master/CONTRIBUTING.md) is available. Please add 
yourself to the [list of contributors](https://mygit.th-deg.de/fwahl/rocketlog/blob/master/CONTRIBUTORS.md) when you 
submit the pull request.
