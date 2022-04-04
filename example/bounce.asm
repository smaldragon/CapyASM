; 32-byte iNES header
    byte "NES",$1a
    byte 2             ; 32kb prg rom
    byte 2             ; 16Kb chr rom
    byte %00000001
    byte %00000000
    byte 0
    byte 0,0,0,0,0,0,0

    asm "nes_registers.asm"

macro wrb
    lda {0}
    sta {1}
endmacro

    ; Zero Page
    var ball_x            $0
    var ball_y            $1
    var ball_dx           $2
    var ball_dy           $3
    var ball_hist_pointer $4
    ; WRAM
    var shadow_oam        $200
    var ball_hist_x       $300
    var ball_hist_y       $400

; Prg ROM
    org [$8000]
_reset
    sei
    cld
    ldx $40
    stx [$4017]
    ldx $ff
    txs
    inx
    stx [PPUCTRL]
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

    wrb 2,<ball_dx>
    wrb 1,<ball_dy>

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

    ; Activate Sprites
    ldx $00
__sprite_loop
    inx
    wrb $1,[shadow_oam+x]
    inx
    inx
    inx
    bzc (sprite_loop)
    
    ; Activate Background
    lda %000_11_11_0
    sta [PPUMASK]

    wrb %1_0_0_0_0_0_00,[PPUCTRL]

__forever
    jmp [forever]

_nmi
    wrb $0,[OAMADDR]
    wrb $2,[OAMDMA]     ; Begin Sprite DMA

__dx
    lda <ball_dx>
    clc 
    adc <ball_x>
    sta <ball_x>
    cmp 0
    bzc (next1)
    wrb 2,<ball_dx>
___next1
    cmp 250
    bzc (next2)
    wrb -2,<ball_dx>
___next2
__dy
    lda <ball_dy>
    clc 
    adc <ball_y>
    sta <ball_y>
    cmp 8
    bzc (next1)
    wrb 1,<ball_dy>
___next1
    cmp 224
    bzc (next2)
    wrb 255,<ball_dy>
___next2
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
    wrb [ball_hist_y+x],[$200+y]
    iny
    iny
    iny
    wrb [ball_hist_x+x],[$200+y]
    iny
    bzc (ball_loop)
    rti

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