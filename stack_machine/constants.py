from collections import namedtuple

from enum import Enum


class TokenKind(Enum):
    """
    refer to - https://github.com/cslarsen/stack-machine

    OPCODE  EXPLANATION
    NOP     do nothing
    ADD     pop a, pop b, push a + b
    SUB     pop a, pop b, push a - b
    AND     pop a, pop b, push a & b
    OR      pop a, pop b, push a | b
    XOR     pop a, pop b, push a ^ b
    NOT     pop a, push !a
    PUSH    push next value
    DUP     duplicate value on stack
    DROP    remove top of stack
    # LOAD    pop a, push value read from address a
    # STOR    pop a, pop b, write b to address a
    """
    EOF    = 0xFF
    NOP    = 0x00
    ADD    = 0x01
    SUB    = 0x02
    AND    = 0x03
    OR     = 0x04
    XOR    = 0x05
    NOT    = 0x06
    PUSH   = 0x07
    DUP    = 0x08
    DROP   = 0x09
    IDENT  = 0x0A
    NUMBER = 0x0B


Token = namedtuple('Token', 'kind value')
