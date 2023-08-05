# Acrolib

General utilities for writing motion planning algorithms at [ACRO](https://iiw.kuleuven.be/onderzoek/acro).
This library is aimed at miscellaneous functions and classes that cannot be grouped in a larger package.

## Dynamic Programming

Solve a specific type of Deterministic Markov Decision Process.
It uses a value function that must be minimized instead of maximized.
It assumes a sequential linear graph structure.

## Quaternion

Extension to the [pyquaternion](http://kieranwynn.github.io/pyquaternion/) package.

## Sampling

A sampler class to generate uniform random or deterministic samples.
Deterministic samples are generated using a [Halton Sequence](https://en.wikipedia.org/wiki/Halton_sequence).