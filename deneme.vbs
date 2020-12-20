WScript.Sleep(500)
Set ws = WScript.CreateObject("WScript.Shell")
ws.AppActivate("Aç")
WScript.Sleep(600)

ws.SendKeys(WScript.Arguments(0) + "{ENTER}" )




