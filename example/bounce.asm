# 32-byte iNES header
    .byte 'NES',$1a
    .byte 2             # 32kb prg rom
    .byte 2             # 16Kb chr rom
    .byte %00000001
    .byte %00000000
    .byte 0
    .byte 0,0,0,0,0,0,0

    .cpu 2a03

.macro wrb
    lda {0}
    sta {1}
.endmacro

    # Zero Page
    .var ball_x            $0
    .var ball_y            $1
    .var ball_dx           $2
    .var ball_dy           $3
    .var ball_hist_pointer $4
    # WRAM
    .var shadow_oam        $200
    .var ball_hist_x       $300
    .var ball_hist_y       $400

# Prg ROM
    .org [$8000]
_reset
    sei
    cld
    ldx $40
    stx [$4017]
    ldx $ff
    txs
    inx
    stx [PPU_CTRL]
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

    wrb 2,<ball_dx>
    wrb 1,<ball_dy>

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
    sta [PPU_DATA]

    # Set scroll
    lda $00
    sta [PPU_SCROLL]
    sta [PPU_SCROLL]

    # Activate Sprites
    ldx $00
__sprite_loop
    inx
    wrb $1,[shadow_oam+X]
    inx
    inx
    inx
    bzc (sprite_loop)
    
    # Activate Background
    lda %000_11_11_0
    sta [PPU_MASK]

    wrb %1_0_0_0_0_0_00,[PPU_CTRL]

__forever
    jmp [forever]

_nmi
    wrb $0,[OAM_ADDR]
    wrb $2,[OAM_DMA]     # Begin Sprite DMA

__dx
    lda <ball_dx>
    clc 
    adc <ball_x>
    sta <ball_x>
    cmp 0
    bne (next1)
    wrb 2,<ball_dx>
___next1
    cmp 250
    bne (next2)
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
    wrb -1,<ball_dy>
___next2
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
    rti

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
