import struct
from typing import Dict, Tuple, List

class DawgNode:
    def __init__(self):
        self.children: Dict[str, DawgNode] = {}
        self.is_word: bool = False

    def add_child(self, char: str, node: "DawgNode") -> None:
        self.children[char] = node

    def get_child(self, char: str) -> "DawgNode":
        return self.children.get(char)

    def serialize(self) -> bytes:
        """Convert the DAWG node into a binary format."""
        children_serialized = b"".join(
            char.encode("utf-8") + struct.pack(">I", len(child.serialize())) + child.serialize()
            for char, child in self.children.items()
        )

        is_word_byte = struct.pack(">B", 1 if self.is_word else 0)
        children_count = struct.pack(">I", len(self.children))

        return is_word_byte + children_count + children_serialized

    @staticmethod
    def deserialize(buffer: bytes, offset: int = 0) -> Tuple["DawgNode", int]:
        """Reconstruct a DAWG node from a binary format."""
        node = DawgNode()

        node.is_word = struct.unpack(">B", buffer[offset:offset + 1])[0] == 1
        offset += 1

        children_count = struct.unpack(">I", buffer[offset:offset + 4])[0]
        offset += 4

        for _ in range(children_count):
            char = buffer[offset:offset + 1].decode("utf-8")
            offset += 1

            child_length = struct.unpack(">I", buffer[offset:offset + 4])[0]
            offset += 4

            child_node, new_offset = DawgNode.deserialize(buffer, offset)
            node.add_child(char, child_node)
            offset = new_offset

        return node, offset


class DAWG:
    def __init__(self):
        self.root = DawgNode()

    def insert(self, word: str) -> None:
        """Insert a word into the DAWG."""
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.add_child(char, DawgNode())
            current_node = current_node.get_child(char)
        current_node.is_word = True

    def is_valid_word(self, word: str) -> bool:
        """Check if a word exists in the DAWG."""
        word = word.upper()
        current_node = self.root
        for char in word.upper():
            current_node = current_node.get_child(char)
            if current_node is None:
                return False
        return current_node.is_word

    def get_all_words(self) -> List[str]:
        """Retrieve all words stored in the DAWG."""
        words = []

        def collect_words(node: DawgNode, current_word: str):
            if node.is_word:
                words.append(current_word)
            for char, child in node.children.items():
                collect_words(child, current_word + char)

        collect_words(self.root, "")
        return words

    def serialize(self) -> bytes:
        """Serialize the entire DAWG into binary format."""
        return self.root.serialize()

    def deserialize(self, data: bytes) -> None:
        """Deserialize binary data to reconstruct the DAWG."""
        root, _ = DawgNode.deserialize(data)
        self.root = root