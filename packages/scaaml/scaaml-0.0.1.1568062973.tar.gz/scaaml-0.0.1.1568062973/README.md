# SCAAML - Side Channel Attacks Assisted by Machine Learning

## Background

SCAAML showcases the use of Machine Learning assist in Side-channel attacks
against cryptography hardware, in an automated fashion.

SCAAML paper: <coming soon>

## Training Models

See ./notebooks/EndToEndAttack.ipynb for an example of training a model to
learn to discern the key byte from the trace.

## Running Attacks

See ./notebooks/AttackOnly.ipynb for an example of training a model to
learn to discern the key byte from the trace.

## Results

In short, this can be trained to learn to discern the correct byte for
the TinyAES implementation with 100% accuracy, given a small handful of traces
measured from the chip while using the same key.

More comprehensive details coming soon.
