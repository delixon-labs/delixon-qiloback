"""qiloback-cli (pip wrapper) — lazy loader for the native CLI binary.

Public surface is intentionally one function: :func:`cli.main`. Pip's
project.scripts entry-point wires it up so ``qiloback ...`` invokes
the native binary fetched on first run.
"""
