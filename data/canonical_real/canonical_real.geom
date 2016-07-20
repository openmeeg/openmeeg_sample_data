# Domain Description 1.1

MeshFile "../canonical/canonical.vtp"

Interfaces 3

Interface Cortex: cortex
Interface Skull: skull
Interface Scalp: scalp

Domains 4

Domain Brain: -Cortex
Domain Skull: Cortex -Skull
Domain Scalp: Skull -Scalp
Domain Air: Scalp

