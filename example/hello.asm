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

__vblankwait2
    bit [PPUSTATUS]
    bpl (vblankwait2)

    ; Define Palette Colors
    wrb $3F,[PPUADDR]   
    wrb $00,[PPUADDR]
    wrb $15,[PPUDATA]
    wrb $20,[PPUDATA]
    
    ; Define Cursor Position
    wrb $21,[PPUADDR]
    wrb $AA,[PPUADDR]
    
    ; Write text
    wrb 1,[PPUDATA] ; H
    wrb 2,[PPUDATA] ; E
    wrb 3,[PPUDATA] ; L
    sta   [PPUDATA] ; L
    wrb 4,[PPUDATA] ; O
    wrb 0,[PPUDATA] ; ' '
    wrb 5,[PPUDATA] ; W
    wrb 4,[PPUDATA] ; O
    wrb 6,[PPUDATA] ; R
    wrb 3,[PPUDATA] ; L
    wrb 7,[PPUDATA] ; D
    wrb 8,[PPUDATA] ; heart

    ; Set scroll
    lda $00
    sta [PPUSCROLL]
    sta [PPUSCROLL]

    ; Activate Background
    lda %000_11_11_0
    sta [PPUMASK]

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