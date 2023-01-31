# AppiumBase
- AppiumBase is a complete framework for Mobile Application automation and testing with pytest.
- The API simplifies Appium's out-of-the-box API, leading to cleaner, maintainable code.
- Includes advanced features such as Auto start appium server, Strong Base Class and cloud providers support.

## Install AppiumBase:
You can easily install AppiumBase from pypi:
> pip install appiumbase

###### Type appiumbase to verify that AppiumBase was installed successfully.

### Creating a Capability File for Test Cases:
You need to specify desired capabilities to run your tests.
Here is an example of capability file for android.

```python
desired_cap = {
  "appPackage": "com.your.app",
  "appActivity": "com.yourapp.MainActivity",
  "platformName": "Android",
  "platformVersion": "12",
  "deviceName": "MyDeviceName",
  "udid": "123456"
}
```
You can save the capability file either in py or in the json file.

## Running Your Test Case
Run your test case with the following command
> pytest --cap-file=desired_cap.py

AppiumBase supports running your test cases on LambdaTest and BrowserStack.
We need to pass --lt for LambdaTest and --bs for BrowserStack.

###### Example:
> pytest --lt --cap-file=desired_cap_lt.py
 
> pytest --bs --cap-file=desired_cap_bs.py 

#### Capability files example for LambdaTest and BrowserStack

LambdaTest Capability files:
```python
desired_cap = {
    "user": "your_username",
    "accessKey": "your_access_key",
    "app": "lt://APPID",
    "platformName": "Android",
    "deviceName": "Google Pixel 3",
    "platformVersion": "10",
    "build": "Build 1.0.12",
    "name": "Login_Test",
    "isRealMobile": True
    }
```
For more information check https://www.lambdatest.com/support/docs/desired-capabilities-in-appium/

BrowserStack Capability files:
```python
desired_cap = {
    # Set your access credentials
    "browserstack.user": "your_username",
    "browserstack.key": "your_key",

    # Set URL of the application under test
    "app": "bs://APPID",

    # Specify device and os_version for testing
    "device": "Xiaomi Redmi Note 7",
    "os_version": "10.0",

    # Set other BrowserStack capabilities
    "project": "My Project",
    "build": "Android 1.0.12 All Test Cases",
    "name": "UI_Test Android_1",

    # Set Specific capabilities regarding test
    'autoAcceptAlerts': 'true',
},
```
For more information check https://www.browserstack.com/docs/app-automate/appium/getting-started/python

