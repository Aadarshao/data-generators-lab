# Architecture Overview

- `src/data_generators/core`: shared abstractions and utilities
- `src/data_generators/domains`: generic domain-level generators
- `src/data_generators/scenarios`: realistic scenarios composed from domains
- `projects/`: concrete project setups using scenarios (Spark, analytics, etc.)
