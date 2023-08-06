# Bandwidth Python API
Client library for the [Bandwidth App Platform](http://ap.bandwidth.com/docs/rest-api/)

## Full Reference
### [dev.bandwidth.com/python-bandwidth](http://dev.bandwidth.com/python-bandwidth)

## Requirements
* [Bandwidth Account](http://bandwidth.com/products/application-platform/?utm_medium=social&utm_source=github&utm_campaign=dtolb&utm_content=_)
* [At least Python 3.6](https://www.python.org/downloads/)
## Installation
```
pip install pybandwidth_v2
```


## Usage

### Client Initialization
```python
from pybandwidth_v2.bandwidth_client import BandwidthAccountAPI, BandwidthMessagingAPI
messaging_api = BandwidthMessagingAPI('acc-account_id', 't-token', 's-secret', 'a-application_id')
account_api = BandwidthAccountAPI('acc-account_id', 'u-username', 'p-password')
```

> Each of these code sample assumes that you have already initialized a client

### Search phone number

```python
numbers = account_api.search_available_numbers(area_code = '910', quantity = 3)
print(numbers[0]['number'])
## +19104440230
```

### Send Text Message
```python
message_id = messaging_api.send_message('+1234567980',
                              ['+1234567981'],
                              'SMS message')
print(message_id)
# m-messageId
```

## Release History
### 0.0.2 (2019-09-12)
Initial release of SDK

## Developer Info
### Running tests
```python
pip3 install nose

nosetests pybandwidth_v2
```