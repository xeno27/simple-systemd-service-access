# simple Phython systemd service access
simple class to use dbus more handy in python.
just give the name and check run state or start/stop/restart Service in Systemd (need admin right..)

Maybe this helps you in your simple projects :grinning:

## Example

Start a Service check starte then stop and check state then Restart

```python
    simple = SimpleSystemDService('test.service')
    simple.StartService()
    a=simple.IsRunning()
    print(a)
    simple.StopService()
    a=simple.IsRunning()
    print(a)
    simple.RestartService()
```