# Campy Examples

The runnable programs in this subdirectory provide examples of how to use the library's tools in more complete programs.

The `basic/` examples highlight the usage of individual features of the `campy` library, such as the `GWindow`, various `GObject`s, some `GInteractor`s, or some utilities.

The `cs106a/` folder contains sample programs implementing some of the classic assignments from Stanford's CS106A, such as Pyramid, Breakout, and NameSurfer. Similarly, the `cs106b/` folder contains sample programs from some of the classic assignments from Stanford's CS106B and CS106X, such as NGrams, WordLadder, and Sierpinski's Triangle.

## What `examples/` is NOT

This folder is not for unit tests (those go in the top-level `tests/` folder), nor is it for demonstrating the complete feature set of a module or package. Rather, it's really just a place for standalone examples of integrating the library with some sort of larger application or assignment. This folder is also not for sandboxing the operation of a certain class or function for debugging. That sort of transient debugging code should live in some other folder (say, a top-level `sandbox/` folder) that is not tracked with version control.