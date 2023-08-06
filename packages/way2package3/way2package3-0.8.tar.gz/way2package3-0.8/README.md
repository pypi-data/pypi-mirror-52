# mypackage

A testing package for **Digital Kites** processes.

## Installation

Make sure you have [python](http://nodejs.org/) and [pip](https://www.npmjs.com/) installed.

```sh
pip install mypackage
```


## Usage

```sh
import mypackage

obj = {
    app_ip:"x.x.x.x",  // optional 
    app_name:"your pm2 app name",  // optional
    app_id: 1, // pm2 process id (optional)
    date: Math.floor(new Date().setHours(0, 0, 0, 0) / 1000), // your date epoch in seconds
    time: Math.floor(Date.now() / 1000), // your time epoch in seconds
    message: "some message",//your message
    status: "online",
    log_level:"info" //["fatal", "error", "warn","info","debug"]
}

mypackage.printMessage(obj)
```

#### How to include in your process:

```sh
//Note:Must include this in the first line of your file(which is started with pm2).
//Note:Make sure this snippet runs in production envirnoment.
const dk_logger = require('dk-logger');

dk_logger.setApiKey('YOUR API KEY');

});
```