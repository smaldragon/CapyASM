# CapyASM

![link](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Cattle_tyrant_%28Machetornis_rixosa%29_on_Capybara.jpg/640px-Cattle_tyrant_%28Machetornis_rixosa%29_on_Capybara.jpg)

**CapyASM** is a 65c02 assembler written in Python built as a learning exercise. Its syntax, particularly in regards to addressing modes, differs from the typical 65xx syntax, with the goal of trying to make the instructions more explicit and easy to understand.

> Note: This assembler is very much a WIP, I do not recommend using it in serious projects.

## Usage

`python3 capyasm.py -i input.asm -o output.asm`

## Addressing Modes

In CapyASM the type of addressing to be used is always written explicitly, avoiding ambiguity. Immediate values are written without decoration, memory/absolute values are written between `[]` brackets, zero page is written between `<>` brackets and relative addressing is written between `()` brackets. 

* **Implied** - `RTS`
* **Registers** - `PSH A | PSH X | PSH Y | PSH P`
* **Immediate** - `LDA $20`
* **Relative** - `BRA (label)`
* **Absolute** - `LDA [$2000]`
* **Zero Page** - `LDA <$20>`
* **Indirect** - `JMP [[$1000]]`
* **Absolute Indexed** - `LDA [$1000+x]`
* **Zero Page Indexed** - `LDA <$10+x>`
* **Indexed Indirect** - `LDA [<$10+x>]`
* **Indirect Indexed** - `LDA [<$10>+y]`

## Assembler Commands

* `byte $xx,$xx,(...)` - Inserts binary byte data
* `word $xxxx,$xxxx,(...)`   - Inserts binary word data
* `bin "file.bin"`     - Inserts a binary file
* `asm "file.asm"`     - Inserts an assembly file
* `org [$xx]`          - Sets the Program Counter
* `pad $xx|pad $[xx]`  - Adds zeros to the file, either a set amount or until a certain PC is reached
* `var $xx`            - Define variable
* `macro name $xx,$xx` - Define Macro

## Aliases

In addition to the traditional opcode mnemonics, CapyASM also provides some alternative mnemonics for certain instructions:

* `bcc` - Branch on carry clear
* `bcs` - Branch on carry set
* `bnc` - Branch on negative clear
* `bns` - Branch on negative set
* `xor` - Exclusive-Or
* `inc A/X/Y` - Increment register
* `dec A/X/Y` - Decrement register

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
