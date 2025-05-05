# 32-byte iNES header
    .byte 'NES',$1a
    .byte 2             # 32kb prg rom
    .byte 2             # 16Kb chr rom
    .byte %00000001
    .byte %00000000
    .byte 0
    .byte 0,0,0,0,0,0,0

    .cpu 2a03



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
    lda 0
    sta <$0000+X>
    sta [$0100+X]
    sta [$0300+X]
    sta [$0400+X]
    sta [$0500+X]
    sta [$0600+X]
    sta [$0700+X]
    lda $FF
    sta [$0200+X]
    inx
    bne (clrmem)

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
    
    # Define Cursor Position
    lda $21; sta [PPU_ADDR]
    lda $AA; sta [PPU_ADDR]
    
    # Write text
    lda 1; sta [PPU_DATA] # H
    lda 2; sta [PPU_DATA] # E
    lda 3; sta [PPU_DATA] # L
           sta [PPU_DATA] # L
    lda 4; sta [PPU_DATA] # O
    lda 0; sta [PPU_DATA] # ' '
    lda 5;sta [PPU_DATA] # W
    lda 4;sta [PPU_DATA] # O
    lda 6;sta [PPU_DATA] # R
    lda 3;sta [PPU_DATA] # L
    lda 7;sta [PPU_DATA] # D
    lda 8;sta [PPU_DATA] # heart

    # Set scroll
    lda $00
    sta [PPU_SCROLL]
    sta [PPU_SCROLL]

    # Activate Background
    lda %000_11_11_0
    sta [PPU_MASK]
    lda %100_010_00
    sta [PPU_CTRL]

__forever
    jmp [forever]

__nmi
  lda 2; sta [OAM_DMA]
rti

# Vectors
    .pad [$FFFA]
    .word nmi
    .word reset
    .word reset

# Chr ROM
    .org [0]
    .pad 16
    # H
    .byte %00000000,%01100011,%01100011,%01100011,%01111111,%01111111,%01100011,%01100011
    .pad 8
    # E
    .byte %00000000,%01111111,%01111111,%01100000,%01111110,%01100000,%01111111,%01111111
    .pad 8
    # L
    .byte %00000000,%01100000,%01100000,%01100000,%01100000,%01100000,%01111111,%01111111
    .pad 8
    # O
    .byte %00000000,%01111111,%01111111,%01100011,%01100011,%01100011,%01111111,%01111111
    .pad 8
    # W
    .byte %00000000,%01100011,%01100011,%01100011,%01100011,%01111111,%01111111,%01100011
    .pad 8
    # R
    .byte %00000000,%01111111,%01100011,%01100011,%01111110,%01111110,%01100011,%01100011
    .pad 8
    # D
    .byte %00000000,%01111100,%01111111,%01100011,%01100011,%01100011,%01111111,%01111100
    .pad 8
    # HEART
    .byte %00000000,%00110110,%01111111,%01111111,%01111111,%00111110,%00011100,%00001000
    .pad 8
    .pad [$4000]