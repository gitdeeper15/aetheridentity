"""Minimal independent simulator of replicated state S (§8 of SPECIFICATION.md).

S is a flat list of admitted records. Admission is sequential. No
concurrency, no causal delivery, no fork resolution.
"""

from __future__ import annotations

from aetheridentity.records import AnyRecord, record_hash
from aetheridentity.signer import Signer


class Simulator:
    """Replicated state S as a flat list of records."""

    def __init__(self, signer: Signer) -> None:
        self._signer = signer
        self._records: list[AnyRecord] = []
        self._hashes: set[str] = set()

    def admit(self, record: AnyRecord) -> bool:
        """Admit a record. Returns True if admitted, False if duplicate.

        Raises:
            ValueError: if the record's signature does not verify.
        """
        # 1. Structural validation is the responsibility of the record class
        #    (its __post_init__). A malformed record cannot be constructed.
        # 2. Signature verification.
        if record.signature:
            from aetheridentity.records import canonical_bytes

            if not self._signer.verify(canonical_bytes(record), record.signature, b""):
                raise ValueError("signature verification failed")

        # 3. Deduplication by canonical hash.
        h = record_hash(record)
        if h in self._hashes:
            return False
        self._hashes.add(h)
        self._records.append(record)
        return True

    def records(self) -> list[AnyRecord]:
        """Return a copy of S. The caller cannot mutate internal state."""
        return list(self._records)

    def __len__(self) -> int:
        return len(self._records)
