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
; Author . : James Taracevicz, jtaracevicz@yahoo.com