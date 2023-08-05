# Python Libra Client Library

## Overview

This library implements the core client facilities for interacting with the
Libra blockchain. The intent is to demonstrate Libra's APIs without either
requiring reading extensive documentation or navigating Libra's Rust code base.

## Components

`lcs.py` implements Libra Canonical Serialization

## Requirements

`grpcio-tools` for gRPC and Protocol Buffers

`pynacl` for cryptographic operations (Curve25519, Ed25519, Sha3)

## Updating

This library includes both proto and mvir files for communicating with Libra
validators and the Libra VM, respectively. These files are borrowed from the
upstream Libra distribution and may be changed without warning. To enable easy
transition to newer versions this library includes to scripts to retrieve the
appropriate files and add them herein:

`update_programs.sh` compiles all the basic transaction Libra move scripts into
Move IR so that they can aeqgransferred to the validators when executing a
transaction.

`update_proto.sh` retrieves all the proto files for communicating to the Libra
admission control node and converts it into Python proto and gRPC libraries.
