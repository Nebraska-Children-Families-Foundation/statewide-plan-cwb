"""
core/models.py
This file acts as an entry point for all models in the `core` application.
Individual model categories are organized into separate modules within this
application. Refer to the respective modules for specific model implementations.
"""

# Importing models from submodules
from .standardization.models import *  # Handles models for standardizing dropdowns and selections
from .measurement.models import *      # Models related to performance measurements
from .alignment.models import *        # Models for alignment with external stakeholders
from .plan_actors.models import *      # Models for actors involved in the plan
from .plan_work.models import *        # Models for the core working aspects of the plan
from .relationships.models import *    # Models for handling relationships between different entities
