# 65C816 Data Width

CapyAsm handles differing data widths through an explicit `lda:b`/`lda:w` syntax.

# Alternate Instruction Names

The following alternate instruction names are available:

* `bzc` - Branch Zero Clear (`bne`)
* `bzs` - Branch Zero Set (`beq`)
* `bnc` - Branch Negative Clear (`bpl`)
* `bns` - Branch Negative Set (`bmi`)
* `blt` - Branch Lesser (`bcc`)
* `bge` - Branch Greater or Equal (`bcs`)
* `clp` - Clear Processor Flags (`rep`)
* `swa` - Swap A and B Accumulator (`xba`)
* `tad` - Transfer A to Direct Register (`tcd`)
* `tas` - Transfer A to Stack Pointer (`tcs`)
* `tda` - Transfer Direct Register to A (`tdc`)
* `tsa` - Transfer Stack Pointer to A (`tsc`)


# Macro Instructions

## ADD and SUB

`add`/`sub` prefix the necessary `clc`/`sec` when performing an addition or subtraction without carry/borrow.

## Word/Multibyte Increment/Decrement

`inx:w`/`dex:w`/`inx:4`,etc, place several consecutive instructions, useful for when iterating through arrays of words.

## Long Conditional Branches

These facilitate branches longer than -127,128 bytes, for example, `beq:l [LABEL]`, is equivalent to:

```
bne 3
jmp [LABEL]
```

For the **65c816**, a relative mode is added to these using the `brl` instruction.

## 65C816 Register Width

`rep`/`sep` macros for setting register/memory width: `M8`,`M16`,`X8`,`X16`,`M8X8`,`M8X16`,`M16X8`,`M16X16`
