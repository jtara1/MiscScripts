; Script Info
; Name .... : Prep-center-script
; Hotkeys . :
;	1. Key 'Space bar' selects thru-cut and saves piece
;	2. Key 'f' will select and press the Edit Path button for next piece
;	3. Key 'Esc' terminates program (confirmation message window will be sent)
; Purpose . : Assist user edit paths of each piece and select thru-cut and save each piece within Prep-center software
; Method .. :
;	1. Initialize with Init() function which has a pop up info message box, then once ok is pressed, selects (with mouse) Quantity field for first piece then presses tab seven times and space bar once to edit path of first piece.
;	2. Continuously loop and wait for a hotkey to be pressed.
;	3. If hotkey 'Space bar" pressed, select thru-cut and save piece (using mouse)
;	4. If hotkey 'f' pressed, edit path of next piece (by pressing tab eight times and space bar once)
;	5. If hotkey 'Esc' pressed, terminate program
; Notes ... :
;	1. For Method step 3, User input required to select path for piece that will be thru-cut.
;	2. No longer needed with v1.1. Variable $prepCenterTitle will needed to be updated
;	3. Coordinates provided are relative to Prep-center window. They may need to be updated if windows are resized.
;	4. This script functions by hotkeys so it will wait for one of the three defined hotkeys to be pressed to do something (after initialization)
; Bugs ... :
;	1. Moving the edit paths window will cause a mismatch in the provided coordinates thus misclicking.
;	2. Resizing any of the Prep-center windows will cause a mismatch in the provided coordinates thus misclicking.
; Todo ... :
;	1. Get button via ID rather than coordinates
; Author . : James T, jtara@tuta.io

;#include <Misc.au3>
#include <MsgBoxConstants.au3>
#include <ClickAtCoords.au3>
#include <TabSpacePress.au3>

Local $continue = True

;Local $hDLL = DLLOpen("user32.dll")
;Local $firefox_title = "You're browsing privately - Mozilla Firefox (Private Browsing)"
;Local $firefox[3][2] = [[871, 655], [176, 136], [0, 0]] ;Firefox on PowerPC

Local $prepCenterTitle = "Grafitroniks Prep Center" ;this is only a substring of the title
Local $thruCutBtn_SaveBtn_coords[2][2] = [[958, 513], [40, 60]] ;relative to prep-center window (may need changing if windows are resized)
Local $quantityField_coords[1][2] = [[660, 185]] ;relative to prep-center window	

HotKeySet("f", "EditPaths")
HotKeySet("{SPACE}", "ThruCutSave")
HotKeySet("{ESC}", "End")

Init()
Do
	Sleep(100)
Until Not $continue

Func Init()
    Local $prompt = MsgBox($MB_OK, "James's Script", "Requirement: All pieces loaded into Prep Center" & @LF & "Hotkeys:" & @LF & "Space: Save as Thru cut layer" & @LF & "f: Get next EditPaths"  & @LF & "Esc: End Program")
	If $prompt == $IDOK Then
		ClickAtCoords($prepCenterTitle, $quantityField_coords)
		TabSpacePress(7, 1)
	EndIf
EndFunc

Func ThruCutSave()
    ;MsgBox($MB_OK, "", "ThruCutSave")
	ClickAtCoords($prepCenterTitle, $thruCutBtn_SaveBtn_coords)
EndFunc

Func EditPaths()
    ;MsgBox($MB_OK, "", "EditPaths")
	TabSpacePress(8, 1)
 EndFunc

Func End()
   MsgBox($MB_OK, "James's Script", "Program Ended")
   $continue = False
EndFunc