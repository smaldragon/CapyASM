# 32-byte iNES header
    .byte 'NES',$1a
    .byte 2             # 32kb prg rom
    .byte 2             # 16Kb chr rom
    .byte %00000001
    .byte %00000000
    .byte 0
    .byte 0,0,0,0,0,0,0

    .cpu 2a03

# Macro for writing a byte to memory
.macro wrb
    lda {0}
    sta {1}
.endmacro
# Variables - these are the memory address used for various functions
# Zero Page
.var ball_x            $0
.var ball_y            $1
.var ball_dx           $2
.var ball_dy           $3
.var ball_hist_pointer $4
.var controller        $5
.var controller_RIGHT  $5
.var controller_LEFT   $6
.var controller_DOWN   $7
.var controller_UP     $8
.var controller_START  $9
.var controller_SELECT $A
.var controller_B      $B
.var controller_A      $C
# WRAM
.var shadow_oam        $200
.var ball_hist_x       $300
.var ball_hist_y       $400

# Prg ROM
.org [$8000]
# Init Sequence
_reset
    sei
    ldx $40
    stx [$4017]
    ldx $ff
    txs
    inc X            # make x zero
    stx [PPU_CTRL]   # disable
    stx [PPU_MASK]
    stx [$4010]

    bit [PPU_STATUS]

__vblankwait1
    bit [PPU_STATUS]
    bpl (vblankwait1)

__clrmem
    sta <$0000+X>
    sta [$0100+X]
    sta [$0200+X]
    sta [$0300+X]
    sta [$0400+X]
    sta [$0500+X]
    sta [$0600+X]
    sta [$0700+X]
    inx
    bne (clrmem)

    wrb 0,<ball_dx>
    wrb 0,<ball_dy>

__vblankwait2
    bit [PPU_STATUS]
    bpl (vblankwait2)

    # Define Palette Colors
    wrb $3F,[PPU_ADDR]   
    wrb $00,[PPU_ADDR]
    wrb $15,[PPU_DATA]
    wrb $20,[PPU_DATA]

    # Define Palette Colors
    wrb $3F,[PPU_ADDR]   
    wrb $11,[PPU_ADDR]
    wrb $20,[PPU_DATA]
    wrb $10,[PPU_DATA]
   
    # Set scroll
    lda $00
    sta [PPU_SCROLL]
    sta [PPU_SCROLL]

    # Set Main Sprite to tile 1
    wrb $1,[$201]
    ldx $04
    # Set Follow Sprites to tile 2
__sprite_loop
    inx
    wrb $2,[shadow_oam+X]
    inx
    inx
    inx
    bzc (sprite_loop)
    
    # Activate Background
    lda %000_11_11_0
    sta [PPU_MASK]

    # Enable ppu interrupts
    wrb %1_0_0_0_0_0_00,[PPU_CTRL]

__forever
    jmp [forever]

_nmi
    # Perform OAM Sprite DMA
    wrb $0,[OAM_ADDR]
    wrb $2,[OAM_DMA]

    inc <ball_hist_pointer>
    ldx <ball_hist_pointer>
    wrb <ball_x>,[ball_hist_x+X]
    wrb <ball_y>,[ball_hist_y+X]

    # Ball 1
    # X
    lda [ball_hist_x+X]
    sta [$203]
    # Y
    lda [ball_hist_y+X]
    sta [$200]

    ldy $4
__ball_loop
    txa
    sec
    sbc 4
    tax
    wrb [ball_hist_y+X],[shadow_oam+Y]
    iny
    iny
    iny
    wrb [ball_hist_x+X],[shadow_oam+Y]
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

# Subroutine that reads the controller
# each individual button is stored in a seperate zp addresses
# due to nes quirks the button value is either $40 or $41
_controller_read
    # strobe the controller to read in new values
    wrb $01,[JOY1]
    lsr A
    sta [JOY1]
    # loop 8 times to grab each button
    ldx 8
__loop
    lda [JOY1]
    dec X
    sta <controller+X>
    bzc (loop)
    rts

# Vectors
    .pad [VECTORS]
    .word nmi
    .word reset
    .word reset

# Chr ROM
    .org [0]
    .pad 16
    # Ball Main
    .byte %00111100,%01111110,%11111111,%11111111,%11111111,%11111111,%01111110,%00111100
    .pad 8
    # Ball Shadow
    .pad 8
    .byte %00111100,%01111110,%11111111,%11111111,%11111111,%11111111,%01111110,%00111100
    .pad [$4000]
