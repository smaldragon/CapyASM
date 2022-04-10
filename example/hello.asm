; 32-byte iNES header
    byte 'NES',$1a
    byte 2             ; 32kb prg rom
    byte 2             ; 16Kb chr rom
    byte %00000001
    byte %00000000
    byte 0
    byte 0,0,0,0,0,0,0

    cpu 2a03

macro wrb
    lda {0}
    sta {1}
endmacro

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
    stx [PPU_CTRL]
    stx [PPU_MASK]
    stx [$4010]

    bit [PPU_STATUS]

__vblankwait1
    bit [PPU_STATUS]
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

__vblankwait2
    bit [PPU_STATUS]
    bpl (vblankwait2)

    ; Define Palette Colors
    wrb $3F,[PPU_ADDR]   
    wrb $00,[PPU_ADDR]
    wrb $15,[PPU_DATA]
    wrb $20,[PPU_DATA]
    
    ; Define Cursor Position
    wrb $21,[PPU_ADDR]
    wrb $AA,[PPU_ADDR]
    
    ; Write text
    wrb 1,[PPU_DATA] ; H
    wrb 2,[PPU_DATA] ; E
    wrb 3,[PPU_DATA] ; L
    sta   [PPU_DATA] ; L
    wrb 4,[PPU_DATA] ; O
    wrb 0,[PPU_DATA] ; ' '
    wrb 5,[PPU_DATA] ; W
    wrb 4,[PPU_DATA] ; O
    wrb 6,[PPU_DATA] ; R
    wrb 3,[PPU_DATA] ; L
    wrb 7,[PPU_DATA] ; D
    wrb 8,[PPU_DATA] ; heart

    ; Set scroll
    lda $00
    sta [PPU_SCROLL]
    sta [PPU_SCROLL]

    ; Activate Background
    lda %000_11_11_0
    sta [PPU_MASK]

__forever
    jmp [forever]

; Vectors
    pad [$FFFA]
    word reset
    word reset
    word reset

; Chr ROM
    org [0]
    pad 16
    ; H
    byte %00000000,%01100011,%01100011,%01100011,%01111111,%01111111,%01100011,%01100011
    pad 8
    ; E
    byte %00000000,%01111111,%01111111,%01100000,%01111110,%01100000,%01111111,%01111111
    pad 8
    ; L
    byte %00000000,%01100000,%01100000,%01100000,%01100000,%01100000,%01111111,%01111111
    pad 8
    ; O
    byte %00000000,%01111111,%01111111,%01100011,%01100011,%01100011,%01111111,%01111111
    pad 8
    ; W
    byte %00000000,%01100011,%01100011,%01100011,%01100011,%01111111,%01111111,%01100011
    pad 8
    ; R
    byte %00000000,%01111111,%01100011,%01100011,%01111110,%01111110,%01100011,%01100011
    pad 8
    ; D
    byte %00000000,%01111100,%01111111,%01100011,%01100011,%01100011,%01111111,%01111100
    pad 8
    ; HEART
    byte %00000000,%00110110,%01111111,%01111111,%01111111,%00111110,%00011100,%00001000
    pad 8
    pad [$4000]