"""
sfc_models
==========
Python package to generate Stock-Flow Consistent Models, with equations generated automatically by high-level code.

Overview
--------

The class *IterativeMachineGenerator* is used to solve the equations generated.

The high level logic is embedded within the *sfc_models.models.py* module. The bulk of the model logic is found within
the various  economic sectors (for example, government, household, business  sectors). Such sectors are
implemented by creating a subclass of the Sector class. (These sublasses are within *sfc_models.sectors*.)

In order to deal with the complexity of multi-country models, the sectors lie within a Country object, and there is a
single Model object that contains all countries.

- Model
|
|- Country A
|     |
|     |- Sector1
|     |
|     |- Sector2
|
|- Country B
      |
      |- Sector 3

The user first creates all of the sectors, and sets the associated parameters. Additionally, certain variables are set
externally ("exogenous") and must be specified at the model level.

Once all the sectors are created, the main() function is called on the Model object, and it ties all of the sectors
together, and creates the model equations. These model equations are put into a text block, which can be passed into
a IterativeMachineGenerator object to solve.

Codes and FullCodes
-------------------

All sectors have a code associated with them; for example, 'GOV' for government. Within a country, sectors can specify
relations using this code.

However, in order to be able to support multi-country models, a country code needs to be prepended to create the
*full code*. For example, the Canadian 'GOV' sector will have a full code of 'CA_GOV' if we have defined the country
code for the Canadian Country object as "CA". This makes it possible to distinguish 'US_GOV' from 'CA_GOV'.

If sectors want to have equations that link to other sectors, the linkage has to come after the Model object has
generated the full codes.


Copyright/License
-----------------

Copyright 2016 Brian Romanchuk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys

from sfc_models.utils import register_standard_logs
from sfc_models.examples.install_examples import install_examples

__all__ = ['models', 'sector', 'sector_definitions', 'utils']

class Parameters(object):
    """
    (Static) class that holds various parameters.

    These are effectively global variables, and are somewhat error-prone.

    They were created in order to clean up some parameter passing, but it is likely that they
    can be eliminated as part of code cleanup.
    """
    # Yay: refactored out of existence!
    pass




