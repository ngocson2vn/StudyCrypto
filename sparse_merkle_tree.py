from collections import OrderedDict

from eth_utils.crypto import keccak
import json

class SparseMerkleTree(object):
    class TreeSizeExceededException(Exception):
        """there are too many leaves for the tree to build"""

    def __init__(self, depth=64, leaves={}):
        self.depth = depth
        if len(leaves) > 2 ** depth:
            raise self.TreeSizeExceededException(
                'tree with depth {} cannot have {} leaves'.format(
                    depth, len(leaves)
                )
            )

        # Sort the transaction dict by index.
        self.leaves = OrderedDict(sorted(leaves.items(), key=lambda t: t[0]))
        self.default_nodes = self.create_default_nodes(self.depth)
        if leaves:
            self.tree = self.create_tree(
                self.leaves, self.depth, self.default_nodes
            )
            self.root = self.tree[-1][0]
        else:
            self.tree = []
            self.root = self.default_nodes[self.depth]

    def create_default_nodes(self, depth):
        # Default nodes are the nodes whose children are both empty nodes at
        # each level.
        default_hash = keccak(b'\x00' * 32)
        default_nodes = [default_hash]
        for level in range(1, depth + 1):
            prev_default = default_nodes[level - 1]
            h = prev_default * 2
            # print(level, prev_default.hex(), "=>", h.hex())
            default_nodes.append(keccak(h))
        return default_nodes

    def create_tree(self, ordered_leaves, depth, default_nodes):
        tree = [ordered_leaves]
        tree_level = ordered_leaves
        for level in range(depth):
            next_level = {}
            for index, value in tree_level.items():
                if index % 2 == 0:
                    co_index = index + 1
                    if co_index in tree_level:
                        next_level[index // 2] = keccak(
                            value + tree_level[co_index]
                        )
                    else:
                        next_level[index // 2] = keccak(
                            value + default_nodes[level]
                        )
                else:
                    # If the node is a right node, check if its left sibling is
                    # a default node.
                    co_index = index - 1
                    if co_index not in tree_level:
                        next_level[index // 2] = keccak(
                            default_nodes[level] + value
                        )
            tree_level = next_level
            tree.append(tree_level)
        return tree

    def create_merkle_proof(self, uid):
        # Generate a merkle proof for a leaf with provided index.
        # First `depth/8` bytes of the proof are necessary for checking if
        # we are at a default-node
        index = uid
        proof = b''
        proofbits = 0

        # Edge case of tree being empty
        if len(self.tree) == 0:
            return b'\x00\x00\x00\x00\x00\x00\x00\x00'

        for level in range(self.depth):
            sibling_index = index + 1 if index % 2 == 0 else index - 1
            index = index // 2
            if sibling_index in self.tree[level]:
                proof += self.tree[level][sibling_index]
                proofbits += 2 ** level

        print(proofbits, "=>", proof)
        proof_bytes = proofbits.to_bytes(8, byteorder='big')
        return proof_bytes + proof

    def verify(self, uid, proof):
        ''' Checks if the proof for the leaf at `uid` is valid'''
        # assert (len(proof) -8 % 32) == 0
        assert len(proof) <= 2056

        proofbits = int.from_bytes((proof[0:8]), byteorder='big')
        index = uid
        p = 8
        if index in self.leaves:
            computed_hash = self.leaves[index]
        # in case the tx is not included, computed_hash is the default leaf
        else:
            computed_hash = self.default_nodes[-1]

        for d in range(self.depth):
            if proofbits % 2 == 0:
                proof_element = self.default_nodes[d]
            else:
                proof_element = proof[p : p + 32]
                p += 32
            if index % 2 == 0:
                computed_hash = keccak(computed_hash + proof_element)
            else:
                computed_hash = keccak(proof_element + computed_hash)
            proofbits = proofbits // 2
            index = index // 2

        print("computed_hash:", computed_hash)
        return computed_hash == self.root

# =====================================================================
smt = SparseMerkleTree(depth=64, leaves={})
default_nodes = smt.create_default_nodes(smt.depth)
smt.default_nodes = default_nodes

# print("\n===========================================")
# for level in range(smt.depth + 1):
#     print(level, default_nodes[level].hex())

leaves = {}
for index in range(1, 9):
    value = chr(96 + index).encode('utf-8')
    seed = keccak(value).hex()[:16]
    slot = int(seed, 16)
    leaves[slot] = value

leaves = OrderedDict(sorted(leaves.items(), key=lambda t: t[0]))
smt.leaves = leaves
print(leaves)

tree = smt.create_tree(leaves, smt.depth, default_nodes)
smt.tree = tree
smt.root = smt.tree[-1][0]

print("\n======================================================================================")
for level in range(smt.depth + 1):
    node = dict(tree[level].items())
    for k in node.keys():
        node[k] = node[k].hex()
    print(level, "=>", json.dumps(node, indent=2))
print(smt.root)

print("\n======================================================================================")
uid = 811411239818187526
print("uid:", uid)

proof = smt.create_merkle_proof(uid)
print("proof:", proof)

print("\n======================================================================================")
result = smt.verify(uid, proof)
print("result:", result)
