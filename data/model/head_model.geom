# Domain Description 1.1

Interfaces 3

Interface Skull: "skull.tri"
Interface Cortex: "brain.tri"
Interface Head: "head.tri"

Domains 4

Domain Scalp: Skull -Head
Domain Brain: -Cortex
Domain Air: Head
Domain Skull: Cortex -Skull
