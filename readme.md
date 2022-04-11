# CapyASM

![link](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Cattle_tyrant_%28Machetornis_rixosa%29_on_Capybara.jpg/640px-Cattle_tyrant_%28Machetornis_rixosa%29_on_Capybara.jpg)

**CapyASM** is a 6502-family assembler written in Python built as a learning exercise. Its syntax, particularly in regards to addressing modes, differs from the typical 65xx syntax, with the goal of trying to make the instructions more explicit and easy to understand.

The following cpus are currently supported:

* **MOS 6502**
* **RC 2A03** (nes)
* **WDC 65c02**
* **HuC6280** (pc-engine)

> Note: This assembler is very much a WIP, I do not recommend using it in serious projects.

## Examples

The `examples` folder contains source code for several NES roms, these are being used to test the assembler.

## Usage

`python3 capyasm.py -i input.asm -o output.asm`

## Addressing Modes

In CapyASM the type of addressing to be used is always written explicitly, avoiding ambiguity. Immediate values are written without decoration, memory/absolute values are written between `[]` brackets, zero page is written between `<>` brackets and relative addressing is written between `()` brackets. Commands that take multiple arguments are separated by `:` symbols, long versions of data (16-bit immediate and 24-bit absolute) are prefixed with a `#` symbol.

* **Implied** - `RTS`
* **Registers** - `PSH A | PSH X | PSH Y | PSH P`
* **Immediate** - `LDA 20`
* **Relative** - `BRA (label)`
* **Absolute** - `LDA [$2000]`
* **Zero Page** - `LDA <$20>`
* **Indirect** - `JMP [[$1000]]`
* **Absolute Indexed** - `LDA [$1000+x]`
* **Zero Page Indexed** - `LDA <$10+x>`
* **Indexed Indirect** - `LDA [<$10+x>]`
* **Indirect Indexed** - `LDA [<$10>+y]`
* **Zero Page Relative** (65c02) - `BBR4 <$20>:(label)`
* **Block Move** (HuC6280)- `TIA [$2000]:[$3000]:#$1000`

## Data types

* `29` - Decimal
* `$29` - Hexadecimal
* `%11110000` - Binary
* `'Hello World'` - ASCII
* `"Hello World"` - ASCII (zero-terminated)
* `(@2)` - Relative Instruction Position, `@0` is current instruction, `@1` the next instruction, etc. 

## Assembler Commands

* `byte $xx,$xx,(...)` - Inserts 8-bit data
* `word $xxxx,$xxxx,(...)`   - Inserts 16-bit data (little-endian) 
* `bin "file.bin"`     - Inserts a binary file
* `asm "file.asm"`     - Inserts an assembly file
* `org [$xx]`          - Sets the Program Counter
* `pad $xx|pad $[xx]`  - Adds zeros to the file, either a set amount or until a certain PC is reached
* `var $xx`            - Define variable
* `macro name $xx,$xx` - Define Macro
* `cpu 6502`           - Set the CPU to use

## Aliases

In addition to the traditional opcode mnemonics, CapyASM also provides some alternative mnemonics for certain instructions:

* `bzc` - Branch on zero clear
* `bzs` - Branch on zero set
* `bnc` - Branch on negative clear
* `bns` - Branch on negative set
* `xor` - Exclusive-Or
* `inc A/X/Y` - Increment register
* `dec A/X/Y` - Decrement register
* `bbc0` - Branch on Bit Clear
* `tcb` - Test and Clear Bit 

## Labels

Labels are defined using a `_` prefix. Labels have namespaces that are determined by the amount of `_` symbols in their name, for example:

```
_reset
  (...) ;do things
__loop
  jmp loop
  
_nmi
  (...) ;do things
__loop
  bne loop
  
; Both `_reset` and `_nmi` have a `__loop` label inside them
```

## Macros

Macros are defined with the symbol `macro` and terminated with `endmacro`. The contents of a macro are code with opcional content to be replaced by arguments written between curly braces. Here is an example macro for writing a byte to memory:

```
macro wrb
    lda {0}
    sta {1}
endmacro

    wrb $20,[$2000]
```
