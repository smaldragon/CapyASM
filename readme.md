# CapyASM

**CapyASM** is a 65c02 assembler built as a learning exercise. Its syntax, particularly in regards to addressing modes, differs from the typical 65xx syntax, with the goal of trying to make the instructions more explicit and easy to understand.

> Note: This assembler is very much a WIP, I do not recommend using it in serious projects.

## Usage

`python3 capyasm.py -i input.asm -o output.asm`

## Addressing Modes

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

## Labels

Labels are defined with a `_` prefix.
