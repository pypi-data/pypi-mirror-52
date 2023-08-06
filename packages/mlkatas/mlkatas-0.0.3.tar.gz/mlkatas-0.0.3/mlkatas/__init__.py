"""Utility functions for Machine Learning"""
import seaborn as sns
from .plot import (
    plot_planar_data,
    plot_decision_boundary,
    plot_multiclass,
    plot_multiclass_decision_boundary,
    plot_loss_acc,
    plot_loss_mae
)

from .utils import (
    make_multiclass,
    vectorize_sequences
)
