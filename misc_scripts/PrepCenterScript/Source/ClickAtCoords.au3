; #FUNCTION# ====================================================================================================================
; Name...........: ClickAtCoords
; Description ...: Use the mouse to move to pre-defined coordinates and click
; Syntax.........: ClickAtCoords($iTitle, $iCoords, [, $iButton = "left" [, $iClicks = "1" [, $iSpeed = "10" [, $iXpos = "" [, $iYpos = "" ]]]]] )
; Parameters ....: $iTitle  - The title of the window containing the control
;      $iCoords  - array containing 2-D arrays of [x, y] values which are screen coords relative to window
;      $iButton  - [optional] The button to click: "left", "right", "middle", "main", "menu", "primary", "secondary". Default is "left"
;      $iClicks  - [optional] The number of times to click the mouse. Default is 1.
;      $iSpeed  - [optional] The speed to move the mouse in the range 1 (fastest) to 100 (slowest). A speed of 0 will move the mouse instantly. Default speed is 10.
;      $iXoffset  - [optional] The x position to offset each coordinate by.
;      $iYoffset  - [optional] The y position to offset each y coordinate by. Defaults to 29 since windows window border isn't counted in the window size
; Author ........: James T.
; Derived from ..: _ControlMouseClick function
; ===============================================================================================================================
;#include <KrisUDF.au3>
;#include <Constants.au3>
;#include <AutoItConstants.au3>

;NOTE: To get coords needed use AutoIt3Info.exe to get coord of mouse in locations needed (subtract window position from mouse coord )
;Local $title = "Grafitroniks Prep Center v2.5.31 - 58 days remaining"
;Local $title = "You're browsing privately - Mozilla Firefox (Private Browsing)"
;Local $title = "New Tab - Waterfox"
;Local $winPos = WinGetPos($title)
;Local $coords[2][2] = [[1454 - $winPos[0], 584 - $winPos[1]], [545 - $winPos[0], 133 - $winPos[1]]] ;Prep center
;Local $coords[3][2] = [[871, 655], [176, 136], [0, 0]] ;Firefox on PowerPC
;Local $coords[2][2] = [[3822 - $winPos[0], 522 - $winPos[1]], [3702 - $winPos[0], 307 - $winPos[1]]] ;home-pc testing

;ClickAtCoords($title, $coords)

Func ClickAtCoords($iTitle, $iCoords, $iButton = "left", $iClicks = "1", $iSpeed = "3", $iXoffset = 0, $iYoffset = -29)
WinActivate($iTitle)
Local $iOriginal = Opt("MouseCoordMode", 2)             ;Get the current MouseCoordMode
For $i = 0 To UBound($iCoords) - 1
   MouseClick($iButton, $iCoords[$i][0] + $iXoffset, $iCoords[$i][1] + $iYoffset, $iClicks, $iSpeed) ;Move the mouse and click on the given control
Next
Opt("MouseCoordMode",$iOriginal)               ;Change the MouseCoordMode back to the original
EndFunc   ;==>ClickAtCoords
