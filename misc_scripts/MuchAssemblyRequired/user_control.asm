;; Hardware IDs
HWID_LEGS     equ 0x1
HWID_LASER    equ 0x2
HWID_LIDAR    equ 0x3
HWID_KEYBOARD equ 0x4
HWID_DRILL    equ 0x5
HWID_INV      equ 0x6
HWID_RNG      equ 0x7
HWID_CLOCK    equ 0x8
HWID_HOLO     equ 0x9
HWID_BATTERY  equ 0xA
HWID_FLOPPY   equ 0xB

;;  Drill
;;  Version 1.0B
DRILL_POLL        equ 1 ; Cost: 0kJ
  ;; Get the status of the drill
DRILL_GATHER_SLOW equ 2 ; Cost: 1400kJ
  ;; Gather the resource located under the Cubot (4 tick)*
  ;; Not implemented yet, see:
  ;; https://github.com/simon987/Much-Assembly-Required/issues/10
DRILL_GATHER_FAST equ 3 ; Cost: 2000kJ
  ;; Gather the resource located under the Cubot (1 tick)
DRILL_STATUS_OK   equ 0
DRILL_STATUS_FAIL equ 1

;;  Additional info
;;  The drill status is either STATUS_OK (0x0000) or STATUS_BUSY = (0x0001).
;;  When trying to activate the mining drill while it is busy, it will fail silently


;;  Inventory
;;  Version 1.0B
INV_POLL  equ 1 ; Cost: 0kJ
  ;; Get the contents of the inventory (B = Item ID, 0x0000 if empty)
INV_CLEAR equ 2 ; Cost: 100kJ
  ;; Safely destroy the contents of the inventory
INV_EMPTY equ 0

;;  Laser
;;  Version 1.0B
LASER_WITHDRAW equ 1 ; Cost: 30kJ
  ;; Withdraw the desired item
LASER_DEPOSIT  equ 2 ; Cost: 30kJ
  ;; Withdraw the desired item

;; Additional Info
;; Specify the desired item by setting the value of the B register with an item ID.


;;  Legs
;;  Version 1.0B
LEGS_SET_DIRECTION          equ 1 ; Cost: 20kJ
  ;; Set the direction
LEGS_SET_DIRECTION_AND_WALK equ 2 ; Cost: 100kJ
  ;; Set the direction and walk forward

LEGS_DIR_NORTH equ 0
LEGS_DIR_EAST  equ 1
LEGS_DIR_SOUTH equ 2
LEGS_DIR_WEST  equ 3

;;  Additional Info
;;  Specify the direction in the B register


;;  LiDAR
;;  Version 1.0B
LIDAR_GET_POS       equ 1 ; Cost: 0kJ
  ;; Copy the current (x,y) coordinates in the World in the X and Y registers
LIDAR_GET_PATH      equ 2 ; Cost: 50kJ
  ;; Calculate the shortest path to the specified coordinates and copy it to memory
LIDAR_GET_MAP       equ 3 ; Cost: 10kJ
  ;; Generate the current World's map and copy it to memory
LIDAR_GET_WORLD_POS equ 4 ; Cost: 0kJ
  ;; Copy the current (x,y) coordinates in the Universe in the X and Y registers

;; Additional Info
;; Theres a lot, see it at:
;; https://github.com/simon987/Much-Assembly-Required/wiki/Hardware:-LiDAR


;;  Keyboard
;;  Version NA
KEYBOARD_CLEAR     equ 0 ; Cost: 0kJ
  ;; Clear the keypress buffer
KEYBOARD_FETCH_KEY equ 1 ; Cost: 0kJ
  ;; Reads the oldest keycode from the buffer into the B register and remove it

;;  Additional Info
;;  Keycodes: keycode.info


;;  Hologram Projector
;;  Version 1.1B
HOLO_CLEAR          equ 0 ; Cost: 0kJ
HOLO_DISPLAY_HEX    equ 1 ; Cost: 0kJ, Displays value of B register
HOLO_DISPLAY_STRING equ 2 ; Cost: 0kJ, Displays 0-terminated unicode from X register

;;  Additional Info
;;  Setting Register A to anything other than 0 will cause that value to be displayed
;;  Note that the Hologram Projector will clear itself at the end of the tick,
;;  it is only necessary to use CLEAR when you want to cancel a DISPLAY command
;;  executed within the same tick.


;;  Battery
;;  Version 1.0B
BATTERY_POLL             equ 1 ; Cost: 0kJ
  ;; Copy the current charge of the battery in kJ in the B register
BATTERY_GET_MAX_CAPACITY equ 2 ; Cost: 0kJ
  ;; Copy the maximum capacity of the battery in the B register

;;  Additional Info
;;  Maximum Capacity: 60,000 kJ
;;  As of v1.2a, the only way to refill the battery is to use the temporary
;;  REFILL = 0xFFFF value in the A register (See #2)


;;  Random Number Generator
;;  Version 1.0B
RNG_POLL equ 0 ; Cost: 1kJ
  ;; Copy a randomly generated word into the B register
  ;; Set to 0 just as a placeholder, can be any number

;;  Additional Info
;;  Random number bounds: 0x0000 - 0xFFFF


;;  Clock
;;  Version 1.0B
CLOCK_POLL equ 0 ; Cost: 0kJ
  ;; Get the current time in ticks since the beginning of the universe as
  ;; a 32-bit number stored in B:C (least significant bits in C)
  ;; Set to 0 just as a placeholder, can be any number


;;  Floppy Drive
;;  Version 1.0B
FLOPPY_POLL         equ 1 ; Cost: 0kJ
  ;; Get the status of the drive (READY = 0, NO_MEDIA=1)
FLOPPY_READ_SECTOR  equ 2 ; Cost: 1kJ
  ;; Reads sector X to CPU ram starting at address Y
FLOPPY_WRITE_SECTOR equ 3 ; Cost: 1kJ
  ;; Writes sector X from CPU ram starting at Y

;;  Additional Info
;;  The players can upload their own binary data to a floppy disk or
;;  download to a file using the floppy buttons in the editor.
;;  Floppies contains 80 tracks with 18 sectors per track. That's
;;  1440 sectors of 512 words. (total 1,474,560 bytes / 737,280 words / 1.44MB)
;;  Read and write operations are synchronous. Track seeking time is 2ms.*
;;  *Seek time is added to the total execution time, which is not yet calculated as of v1.3a

;; keys
KEY_A   equ 0x41
KEY_D   equ 0x44
KEY_E   equ 0x45
KEY_F   equ 0x46
KEY_S   equ 0x53
KEY_W   equ 0x57

;;items
ITEM_BIOMASS equ 0x1


; user_control.asm by jtara1
.text
	;CALL clear_buffer
	CALL get_key_in_and_move
	;CALL print_battery
	
clear_buffer:
	PUSH A
	MOV A, KEYBOARD_CLEAR
	HWI HWID_KEYBOARD
	POP A
	RET 0
	
get_key_in_and_move:
	PUSH A
	PUSH B
	MOV A, KEYBOARD_FETCH_KEY
	HWI HWID_KEYBOARD
	; move north
	CMP B, KEY_W
	JZ move_north
	
	; move east
	CMP B, KEY_D
	JZ move_east
	
	; move south
	CMP B, KEY_S
	JZ move_south
	
	; move west
	CMP B, KEY_A
	JZ move_west
	
	; pickup biomass
	CMP B, KEY_F
	JZ withdraw_biomass
	
	; drill slowly
	CMP B, KEY_E
	JZ drill_slow
	
	JNZ print_battery
	POP B
	POP A
	RET 0

deposit_biomass:
	PUSH A
	PUSH B
	MOV A, LASER_DEPOSIT
	MOV B, ITEM_BIOMASS
	HWI HWID_LASER
	POP B
	POP A
	RET 0

drill_slow:
	PUSH A
	MOV A, DRILL_GATHER_SLOW
	HWI HWID_DRILL
	POP A
	RET 0
	
withdraw_biomass:
	PUSH A
	PUSH B
	MOV A, LASER_WITHDRAW
	MOV B, ITEM_BIOMASS
	HWI HWID_LASER
	POP B
	POP A
	RET 0
	
print_battery:
    PUSH A
    MOV A, HOLO_DISPLAY_HEX
    HWI HWID_BATTERY
    HWI HWID_HOLO
    POP A
    RET 0

move_west:
	MOV A, LEGS_SET_DIRECTION_AND_WALK
	MOV B, LEGS_DIR_WEST
	HWI HWID_LEGS
	RET 0
	
move_north:
	MOV A, LEGS_SET_DIRECTION_AND_WALK
	MOV B, LEGS_DIR_NORTH
	HWI HWID_LEGS
	RET 0
	
move_east:
	MOV A, LEGS_SET_DIRECTION_AND_WALK
	MOV B, LEGS_DIR_EAST
	HWI HWID_LEGS
	RET 0
	
move_south:
	MOV A, LEGS_SET_DIRECTION_AND_WALK
	MOV B, LEGS_DIR_SOUTH
	HWI HWID_LEGS
	RET 0
	
print_B_hex:
	PUSH A
	MOV A, HOLO_DISPLAY_HEX
	HWI HWID_HOLO
	POP A
	RET 0
