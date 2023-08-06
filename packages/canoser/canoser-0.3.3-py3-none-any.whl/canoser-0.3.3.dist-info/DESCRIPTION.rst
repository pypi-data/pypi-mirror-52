A python implementation of the canonical serialization for the Libra network.

Canonical serialization guarantees byte consistency when serializing an in-memory
data structure. It is useful for situations where two parties want to efficiently compare
data structures they independently maintain. It happens in consensus where
independent validators need to agree on the state they independently compute. A cryptographic
hash of the serialized data structure is what ultimately gets compared. In order for
this to work, the serialization of the same data structures must be identical when computed
by independent validators potentially running different implementations
of the same spec in different languages.

