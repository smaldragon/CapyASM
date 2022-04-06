; 32-byte iNES header
    byte "NES",$1a
    byte 2             ; 32kb prg rom
    byte 2             ; 16Kb chr rom
    byte %00000001
    byte %00000000
    byte 0
    byte 0,0,0,0,0,0,0

    asm "nes_registers.asm"

; Macro for writing a byte to memory
macro wrb
    lda {0}
    sta {1}
endmacro
; Variables - these are the memory address used for various functions
; Zero Page
var ball_x            $0
var ball_y            $1
var ball_dx           $2
var ball_dy           $3
var ball_hist_pointer $4
var controller        $5
var controller_RIGHT  $5
var controller_LEFT   $6
var controller_DOWN   $7
var controller_UP     $8
var controller_START  $9
var controller_SELECT $A
var controller_B      $B
var controller_A      $C
; WRAM
var shadow_oam        $200
var ball_hist_x       $300
var ball_hist_y       $400

; Prg ROM
org [$8000]
; Init Sequence
_reset
    sei
    ldx $40
    stx [$4017]
    ldx $ff
    txs
    inc x           ; make x zero
    stx [PPUCTRL]   ; disable
    stx [PPUMASK]
    stx [$4010]

    bit [PPUSTATUS]

__vblankwait1
    bit [PPUSTATUS]
    bpl (vblankwait1)

__clrmem
    sta <$0000+x>
    sta [$0100+x]
    sta [$0200+x]
    sta [$0300+x]
    sta [$0400+x]
    sta [$0500+x]
    sta [$0600+x]
    sta [$0700+x]
    inx
    bne (clrmem)

    wrb 0,<ball_dx>
    wrb 0,<ball_dy>

__vblankwait2
    bit [PPUSTATUS]
    bpl (vblankwait2)

    ; Define Palette Colors
    wrb $3F,[PPUADDR]   
    wrb $00,[PPUADDR]
    wrb $15,[PPUDATA]
    wrb $20,[PPUDATA]

    ; Define Palette Colors
    wrb $3F,[PPUADDR]   
    wrb $11,[PPUADDR]
    wrb $20,[PPUDATA]
    wrb $10,[PPUDATA]
    sta [PPUDATA]

    ; Set scroll
    lda $00
    sta [PPUSCROLL]
    sta [PPUSCROLL]

    ; Set Main Sprite to tile 1
    wrb $1,[$201]
    ldx $04
    ; Set Follow Sprites to tile 2
__sprite_loop
    inx
    wrb $2,[shadow_oam+x]
    inx
    inx
    inx
    bzc (sprite_loop)
    
    ; Activate Background
    lda %000_11_11_0
    sta [PPUMASK]

    ; Enable ppu interrupts
    wrb %1_0_0_0_0_0_00,[PPUCTRL]

__forever
    jmp [forever]

_nmi
    ; Perform OAM Sprite DMA
    wrb $0,[OAMADDR]
    wrb $2,[OAMDMA]

    inc <ball_hist_pointer>
    ldx <ball_hist_pointer>
    wrb <ball_x>,[ball_hist_x+x]
    wrb <ball_y>,[ball_hist_y+x]

    ; Ball 1
    ; X
    lda [ball_hist_x+x]
    sta [$203]
    ; Y
    lda [ball_hist_y+x]
    sta [$200]

    ldy $4
__ball_loop
    txa
    sec
    sbc 4
    tax
    wrb [ball_hist_y+x],[shadow_oam+y]
    iny
    iny
    iny
    wrb [ball_hist_x+x],[shadow_oam+y]
    iny
    bzc (ball_loop)
__movement
    jsr [controller_read]
    lda $0
    sta <ball_dx>
    sta <ball_dy>
    lda $41
    cmp <controller_UP>
    bzc (next1)
    wrb -2,<ball_dy>
___next1
    lda $41
    cmp <controller_DOWN>
    bzc (next2)
    wrb 2,<ball_dy>
___next2
    lda $41
    cmp <controller_LEFT>
    bzc (next3)
    wrb -2,<ball_dx>
___next3
    lda $41
    cmp <controller_RIGHT>
    bzc (next4)
    wrb 2,<ball_dx>
___next4
    lda <ball_x>
    clc
    adc <ball_dx>
    sta <ball_x>
    lda <ball_y>
    clc
    adc <ball_dy>
    sta <ball_y>

    rti

; Subroutine that reads the controller
; each individual button is stored in a seperate zp addresses
; due to nes quirks the button value is either $40 or $41
_controller_read
    ; strobe the controller to read in new values
    wrb $01,[JOY1]
    lsr A
    sta [JOY1]
    ; loop 8 times to grab each button
    ldx 8
__loop
    lda [JOY1]
    dec X
    sta <controller+x>
    bzc (loop)
    rts

; Vectors
    pad [$FFFA]
    word nmi
    word reset
    word reset

; Chr ROM
    org [0]
    pad 16
    ; Ball Main
    byte %00111100,%01111110,%11111111,%11111111,%11111111,%11111111,%01111110,%00111100
    pad 8
    ; Ball Shadow
    pad 8
    byte %00111100,%01111110,%11111111,%11111111,%11111111,%11111111,%01111110,%00111100
    pad [$4000]