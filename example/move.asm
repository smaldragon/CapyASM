# 32-byte iNES header
    .byte 'NES',$1a
    .byte 2             # 32kb prg rom
    .byte 2             # 16Kb chr rom
    .byte %00000001
    .byte %00000000
    .byte 0
    .byte 0,0,0,0,0,0,0

    .cpu 2a03

# Variables - these are the memory address used for various functions
# Zero Page
.zp ball_x
.zp ball_y           
.zp ball_dx          
.zp ball_dy          
.zp ball_hist_pointer
.zp controller        0
.zp controller_RIGHT
.zp controller_LEFT
.zp controller_DOWN
.zp controller_UP
.zp controller_START
.zp controller_SELECT
.zp controller_B     
.zp controller_A    
# WRAM
.org [$200]
.var shadow_oam        256
.var ball_hist_x       256
.var ball_hist_y       256

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

    lda 0; sta <ball_dx>
    lda 0; sta <ball_dy>

__vblankwait2
    bit [PPU_STATUS]
    bpl (vblankwait2)
    
    # Fill Nametables with 0 bytes
    bit [PPU_STATUS]
    lda $20; sta [PPU_ADDR]
    lda $00; sta [PPU_ADDR]
    ldy 2048/256
    __clr
      ldx 0
      ___loop
        sta [PPU_DATA]
      inc X; bne (loop)
    dec Y; bne (clr)
    
    # Define Palette Colors
    lda $3F; sta [PPU_ADDR]   
    lda $00; sta [PPU_ADDR]
    lda $15; sta [PPU_DATA]
    lda $20; sta [PPU_DATA]

    # Define Palette Colors
    lda $3F; sta [PPU_ADDR]   
    lda $11; sta [PPU_ADDR]
    lda $20; sta [PPU_DATA]
    lda $10; sta [PPU_DATA]
   
    # Set scroll
    lda $00
    sta [PPU_SCROLL]
    sta [PPU_SCROLL]

    # Set Main Sprite to tile 1
    lda $1; sta [$201]
    ldx $04
    # Set Follow Sprites to tile 2
__sprite_loop
    inx
    lda $2; sta [shadow_oam+X]
    inx
    inx
    inx
    bzc (sprite_loop)
    
    # Activate Background
    lda %000_11_11_0
    sta [PPU_MASK]

    # Enable ppu interrupts
    lda %1_0_0_0_0_0_00; sta [PPU_CTRL]

__forever
    jmp [forever]

_nmi
    # Perform OAM Sprite DMA
    lda $0; sta [OAM_ADDR]
    lda $2; sta [OAM_DMA]

    inc <ball_hist_pointer>
    ldx <ball_hist_pointer>
    lda <ball_x>; sta [ball_hist_x+X]
    lda <ball_y>; sta [ball_hist_y+X]

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
    lda [ball_hist_y+X]; sta [shadow_oam+Y]
    iny
    iny
    iny
    lda [ball_hist_x+X]; sta [shadow_oam+Y]
    iny
    bzc (ball_loop)
__movement
    jsr [controller_read]
    lda $0
      sta <ball_dx>
      sta <ball_dy>
    ___tUP
    lda <controller_UP>
    beq (tDOWN)
      lda -2; sta <ball_dy>
    ___tDOWN
    lda <controller_DOWN>
    beq (tLEFT)
      lda 2; sta <ball_dy>
    ___tLEFT
    lda <controller_LEFT>
    beq (tRIGHT)
      lda -2; sta <ball_dx>
    ___tRIGHT
    lda <controller_RIGHT>
    beq (tDONE)
      lda 2; sta <ball_dx>
    ___tDONE
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
    lda $01; sta [JOY1]
    lsr A
    sta [JOY1]
    # loop 8 times to grab each button (bit 0)
    ldx 7
    __loop
      lda [JOY1]; and 1
      sta <controller_RIGHT+X>
    dec X; bpl (loop)
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
