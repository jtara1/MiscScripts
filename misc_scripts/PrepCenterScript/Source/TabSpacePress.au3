;Local $keys[3] = ["{TAB " & $tabPresses & "}", "{SPACE}", "a"]
;$title = "Grafitroniks Prep Center v2.5.31 - 57 days remaining"
;WinActivate($title)
;TabSpacePress(7, 0)

Func TabSpacePress($tabPresses, $spacePresses)
Local $defaultSendKeyDelay = Opt("SendKeyDelay", 100)
Send("{TAB " & $tabPresses & "}")
Send("{SPACE " & $spacePresses & "}")
Opt("SendKeyDelay", $defaultSendKeyDelay)
EndFunc ;=> PressKeys($keys)