
#include <MsgBoxConstants.au3>
#include <ClickAtCoords.au3>
#include <TabSpacePress.au3>

Local $continue = True

Local $hDLL = DLLOpen("user32.dll")
Local $firefox_title = "You're browsing privately - Mozilla Firefox (Private Browsing)"
Local $firefox[3][2] = [[871, 655], [176, 136], [0, 0]] ;Firefox on PowerPC

Local $prepCenterTitle = "Grafitroniks Prep Center v2.5.31 - 57 days remaining"
Local $thruCutBtn_SaveBtn_coords[2][2] = [[958, 513], [40, 60]]
Local $quantityField_coords[1][2] = [[660, 185]]

HotKeySet("f", "EditPaths")
HotKeySet("{SPACE}", "ThruCutSave")
HotKeySet("{ESC}", "End")

Init()
Do
	Sleep(100)
Until Not $continue

;Init() is ran as this program begins
;It sets active window to that of @param1 in ClickAtCoords(...)
;Moves mouse cursor and clicks in the multi-dimension array given in @param2 in ClickAtCoords(...)
Func Init()
    MsgBox($MB_OK, "", "Init")
	;ClickAtCoords($prepCenterTitle, $quantityField_coords)
	;TabSpacePress(7, 1)
EndFunc

Func ThruCutSave()
    MsgBox($MB_OK, "", "ThruCutSave")
	;ClickAtCoords($prepCenterTitle, $thruCutBtn_SaveBtn_coords)
EndFunc

Func EditPaths()
    MsgBox($MB_OK, "", "EditPaths")
	;TabSpacePress(8, 1)
 EndFunc

Func End()
   MsgBox($MB_OK, "", "Program Ended")
   $continue = False
EndFunc