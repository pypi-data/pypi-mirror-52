# XLNet for TensorFlow

This is a fork of the original [XLNet repository](https://github.com/zihangdai/xlnet)
that adds package configuration so that it can be easily installed and used.
The purpose is to remove the need of cloning the repository and modifying it
locally which can be quite dirty for common tasks (e.g. training a new classifier).
A lot of code can be shared (e.g. `modeling.py`, `classifier_utils.py`) and this
fork is exactly for that.

All the credit goes to [zihangdai/xlnet](https://github.com/zihangdai/xlnet).

Please refer to the official repository for details on how to use the modules
contained in this package. Useful information can also be found
in the [XLNet paper](https://arxiv.org/abs/1906.08237).


# Release Notes

* September 5, 2019: Initial version (1.0.1)
