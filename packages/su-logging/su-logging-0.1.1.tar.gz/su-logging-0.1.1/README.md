# Logging for Stockholm University

Easy to use logging for Stockholm University.

## Usage

```python
from su.logging import logging

logger = logging.getLogger("myapp")
logger.info("My INFO message")
```

### Structured logging
We use
[logstash_formatter](https://github.com/ulule/python-logstash-formatter/)'s
`LogstashFormatterV1` and remove some unused/unnecesary fields.
```python
from su.logging import structured, logging

logger = logging.getLogger("myapp")
logger.info("User logged in", extra={"user": "simlu"})

try:
    raise Exception("User performed illegal activity")
except Exception as e:
    logger.exception(e, extra={"user": "simlu"})
```

## TODO
* [ ] [Some sort of versioning?](https://github.com/sdispater/poetry/issues/1036#issuecomment-489880822)
* [ ] Add STDOUT handler?
