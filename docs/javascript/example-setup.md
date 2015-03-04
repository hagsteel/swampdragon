# Example setup #


## A (pseudo) example disabling inputs when the connection is not available and no subscription exist. ##

```javascript
function enableInputs() {
    // enable all inputs
}

function disableInputs() {
    // disable all inputs
}

disableInputs();

swampdragon.open(function () {
    swampdragon.subscribe(..., function () {
        enabledInputs();
    });
});

swampdragon.close(function () {
    disableInputs();
});
```

This (sparse) example starts off by disabling all inputs (assuming these are inputs that would end up calling routers).
Once a connection is open, call subscribe. Once a subscription is created enable all inputs.

If the connection is lost, disable all inputs so the end user can not trigger router calls.
Once the connection is re-established all inputs will be available again.

