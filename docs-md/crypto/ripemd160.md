Module nibiru.crypto.ripemd160
==============================
Implementing SHA-256 from scratch was fun, but for RIPEMD160 I am
taking an existing implementation and made some cleanups and api changes.

ripemd.py - pure Python implementation of the RIPEMD-160 algorithm.
Bjorn Edstrom <be@bjrn.se> 16 december 2007.

Copyrights
==========

This code is a derived from an implementation by Markus Friedl which is
subject to the following license. This Python implementation is not
subject to any other license.

/*
* Copyright (c) 2001 Markus Friedl.  All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions
* are met:
* 1. Redistributions of source code must retain the above copyright
*    notice, this list of conditions and the following disclaimer.
* 2. Redistributions in binary form must reproduce the above copyright
*    notice, this list of conditions and the following disclaimer in the
*    documentation and/or other materials provided with the distribution.
*
* THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
* IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
* OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
* IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
* NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
* DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
* THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
* THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
/*
* Preneel, Bosselaers, Dobbertin, "The Cryptographic Hash Function RIPEMD-160",
* RSA Laboratories, CryptoBytes, Volume 3, Number 2, Autumn 1997,
* ftp://ftp.rsasecurity.com/pub/cryptobytes/crypto3n2.pdf
*/

Functions
---------


`F0(x, y, z)`
:


`F1(x, y, z)`
:


`F2(x, y, z)`
:


`F3(x, y, z)`
:


`F4(x, y, z)`
:


`R(a, b, c, d, e, Fj, Kj, sj, rj, X)`
:


`RMD160Final(ctx)`
:


`RMD160Transform(state, block)`
:


`RMD160Update(ctx, inp, inplen)`
:


`ROL(n, x)`
:


`ripemd160(b: bytes) ‑> bytes`
:   simple wrapper for a simpler API to this hash function, just bytes to bytes

    Args:
        b: the bytes input

Classes
-------

`RMDContext()`
:
