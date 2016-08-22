# Copyright (C) 2015 The python-opentimestamps developers
#
# This file is part of python-opentimestamps.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

import unittest

from opentimestamps.core.op import *
from opentimestamps.op import *

class Test_cat_sha256(unittest.TestCase):
    def test(self):
        left = BytesCommitment(b'foo')
        right = BytesCommitment(b'bar')

        sha256_op = cat_sha256(left, right)

        self.assertEqual(left.next_op.result, b'foobar')
        self.assertEqual(left.next_op.__class__, OpAppend)
        self.assertEqual(right.next_op.result, b'foobar')
        self.assertEqual(right.next_op.__class__, OpPrepend)

        self.assertEqual(sha256_op.result, bytes.fromhex('c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2'))


        righter = BytesCommitment(b'baz')
        sha256_op2 = cat_sha256(sha256_op, righter)

        self.assertEqual(sha256_op.next_op.result, bytes.fromhex('c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2') + b'baz')
        self.assertEqual(sha256_op.next_op.__class__, OpAppend)
        self.assertEqual(righter.next_op.result, bytes.fromhex('c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2') + b'baz')
        self.assertEqual(righter.next_op.__class__, OpPrepend)

        # Everything should lead to the same final commitment
        for op in (left, right, sha256_op, righter, sha256_op2):
            self.assertEqual(op.final_commitment(), bytes.fromhex('23388b16c66f1fa37ef14af8eb081712d570813e2afb8c8ae86efa726f3b7276'))

class Test_make_merkle_tree(unittest.TestCase):
    def test(self):
        def T(n, expected_merkle_root):
            roots = [BytesCommitment(bytes([i])) for i in range(n)]
            tip = make_merkle_tree(roots)

            self.assertEqual(tip.result, expected_merkle_root)

            for root in roots:
                self.assertEqual(root.final_commitment(), expected_merkle_root)

        # Returned unchanged!
        T(1, bytes.fromhex('00'))

        # Manually calculated w/ pen-and-paper
        T(2, bytes.fromhex('b413f47d13ee2fe6c845b2ee141af81de858df4ec549a58b7970bb96645bc8d2'))
        T(3, bytes.fromhex('e6aa639123d8aac95d13d365ec3779dade4b49c083a8fed97d7bfc0d89bb6a5e'))
        T(4, bytes.fromhex('7699a4fdd6b8b6908a344f73b8f05c8e1400f7253f544602c442ff5c65504b24'))
        T(5, bytes.fromhex('aaa9609d0c949fee22c1c941a4432f32dc1c2de939e4af25207f0dc62df0dbd8'))
        T(6, bytes.fromhex('ebdb4245f648b7e77b60f4f8a99a6d0529d1d372f98f35478b3284f16da93c06'))
        T(7, bytes.fromhex('ba4603a311279dea32e8958bfb660c86237157bf79e6bfee857803e811d91b8f'))
