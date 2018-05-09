; Original source: http://stackoverflow.com/questions/131955/keyboard-shortcut-to-paste-clipboard-content-into-command-prompt-window-win-xp
; Redefine only when the active window is a console window 
#IfWinActive ahk_class ConsoleWindowClass

; Close Command Window with Ctrl+Shift+w
$^+w::
WinGetTitle sTitle
If (InStr(sTitle, "-")=0) { 
	Send EXIT{Enter}
} else {
	Send ^w
}
return 


; Open new Command Window with Ctrl+Shift+n
$^+n::
Run cmd.exe


; Ctrl+Shift+up / Down to scroll command window back and forward
^+Up::
Send {WheelUp}
return

^+Down::
Send {WheelDown}
return


; Ctrl+Shift+v to Paste in command window
^+v::
; Edit->Paste
Send !{Space}ep
return


; Ctrl+Shift+c to copy selected text in command window
^+c::
; Edit->Copy
Send !{Space}ey


#IfWinActive
