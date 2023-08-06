"""
chapter6.py
==========

Models from Chapter 6 of [G&L 2012].

- Model REG = Regional Model (Country divided into North and South regions.)

[G&L 2012] "Monetary Economics: An Integrated Approach to credit, Money, Income, Production
and Wealth; Second Edition", by Wynne Godley and Marc Lavoie, Palgrave Macmillan, 2012.
ISBN 978-0-230-30184-9


Copyright 2017 Brian Romanchuk

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

from sfc_models.gl_book import GL_book_model
from sfc_models.objects import *


class REG(GL_book_model):
    """
    Implements Model REG from Chapter 6 of G&L. REG = "Regional."

    This could have been attempted with two countries (which have the same
    currency), but there's only a single central bank and Treasury. Splitting
    into two countries would mean that we would need to aggregate two different
    government sectors.
    """

    def build_model(self):
        country = self.Country
        # As before, there's only one copy of the governmental sectors
        tre = Treasury(country, 'TRE', 'Treasury')
        cb = CentralBank(country, 'CB', 'Central Bank', treasury=tre)
        # Now we split
        hh_n = Household(country, 'HH_N', 'Household - North', alpha_income=.6, alpha_fin=.4,
                         labour_name='LAB_N', consumption_good_name='GOOD_N')

        hh_s = Household(country, 'HH_S', 'Household - South', alpha_income=.7, alpha_fin=.3,
                         labour_name='LAB_S', consumption_good_name='GOOD_S')

        goods_n = Market(country, 'GOOD_N', 'Goods market - North')
        goods_s = Market(country, 'GOOD_S', 'Goods market - South')
        goods_n.AddVariable('MU', 'Propensity to import', '0.18781')
        goods_s.AddVariable('MU', 'Propensity to import', '0.18781')

        # A literally non-profit business sector
        bus_n = FixedMarginBusinessMultiOutput(country, 'BUS_N', market_list=[goods_n, goods_s],
                                               profit_margin=0.0, labour_input_name='LAB_N')
        bus_s = FixedMarginBusinessMultiOutput(country, 'BUS_S', market_list=[goods_n, goods_s],
                                               profit_margin=0.0, labour_input_name='LAB_S')
        # Create the linkages between sectors - tax flow, markets - labour ('LAB'), goods ('GOOD')
        tax = TaxFlow(country, 'TF', 'TaxFlow', taxrate=.2, taxes_paid_to='TRE')
        labour_s = Market(country, 'LAB_S', 'Labour market')
        labour_n = Market(country, 'LAB_N', 'Labour market')

        mm = MoneyMarket(country, issuer_short_code='CB')
        dep = DepositMarket(country, issuer_short_code='TRE')
        # Create the goods demand function
        Y_N = hh_n.GetVariableName('INC')
        Y_S = hh_s.GetVariableName('INC')
        goods_n.AddSupplier(bus_s, 'MU*{0}'.format(Y_N))
        goods_n.AddSupplier(bus_n)
        goods_s.AddSupplier(bus_s)
        goods_s.AddSupplier(bus_n, 'MU*{0}'.format(Y_S))

        # Create the demand for deposits.  ('MON' is the residual asset.)
        hh_n.AddVariable('L0', 'lambda_0: share of bills in wealth', '0.635')
        hh_n.AddVariable('L1', 'lambda_1: parameter related to interest rate', '5.')
        hh_n.AddVariable('L2', 'lambda_2: parameter related to disposable income', '.01')
        # Generate the equation. Need to get the name of the interest rate variable
        r = dep.GetVariableName('r')
        # The format() call will replace '{0}' with the contents of the 'r' variable.
        eqn = 'L0 + L1 * {0} - L2 * (AfterTax/F)'.format(r)
        hh_n.GenerateAssetWeighting([('DEP', eqn)], 'MON')
        # Create the demand for deposits.  ('MON' is the residual asset.)
        hh_s.AddVariable('L0', 'lambda_0: share of bills in wealth', '0.67')
        hh_s.AddVariable('L1', 'lambda_1: parameter related to interest rate', '6.')
        hh_s.AddVariable('L2', 'lambda_2: parameter related to disposable income', '.07')
        # Generate the equation. Need to get the name of the interest rate variable
        r = dep.GetVariableName('r')
        # The format() call will replace '{0}' with the contents of the 'r' variable.
        eqn = 'L0 + L1 * {0} - L2 * (AfterTax/F)'.format(r)
        hh_s.GenerateAssetWeighting([('DEP', eqn)], 'MON')

        # Add a decorative equation: Government Fiscal Balance
        # = Primary Balance - Interest expense + Central Bank Dividend (= interest
        # received by the central bank).
        tre.AddVariable('FISCBAL', 'Fiscal Balance', 'PRIM_BAL - INTDEP + CB__INTDEP')
        tre.SetEquationRightHandSide('DEM_GOOD', 'DEM_GOOD_N + DEM_GOOD_S')
        tre.AddVariable('DEM_GOOD_N', 'Demand for goods in the North', '')
        tre.AddVariable('DEM_GOOD_S', 'Demand for goods in the South', '')

        if self.UseBookExogenous:
            # Need to set the exogenous variable - Government demand for Goods ("G" in economist symbology)
            tre.SetExogenous('DEM_GOOD_N', '[20.,] * 105')
            tre.SetExogenous('DEM_GOOD_S', '[20.,] * 105')
            dep.SetExogenous('r', '[.025,]*105')
            goods_s.SetExogenous('MU', [0.18781] * 5 + [0.20781] * 105)
            # NOTE:
            # Initial conditions are only partial; there may be issues with some
            # variables.
            self.Model.AddInitialCondition('HH_N', 'AfterTax', 86.486)
            self.Model.AddInitialCondition('HH_S', 'AfterTax', 86.486)
            self.Model.AddInitialCondition('HH_N', 'F', 86.486)
            self.Model.AddInitialCondition('HH_N', 'DEM_DEP', 64.865)
            self.Model.AddInitialCondition('HH_S', 'F', 86.486)
            self.Model.AddInitialCondition('HH_S', 'DEM_DEP', 64.865)
            self.Model.AddInitialCondition('TRE', 'F', 2. * -86.486)
            self.Model.AddGlobalEquation('t', 'decorated time axis', '1955. + k')
        return self.Model

    # noinspection PyPep8,PyPep8,PyPep8,PyPep8,PyPep8
    def expected_output(self):
        """
        Expected output for the model (using default input).
        Based on EViews output using code from Gennaro Zezza (from sfcmodels.net)

        NOTE: A spreadsheet at sfcmodels.net gives different output; income is changing during the
        same period as the rate change.

        We ignore value at t=0
        :return: list
        """
        out = [
            ('t', [None, 1956., 1957., 1958., ]),
            ('TRE__DEM_GOOD', [None, 40., 40., 40., 40.]),  # G
            ('DEP__r', [0.025, ] * 10),
            ('HH_N__WGT_DEP', [None,  0.75, 0.75, 0.75, 0.75, ]),
            # Weight of deposits (bills)
            ('HH_N__AfterTax',
             '86.49\t86.49\t86.49\t86.49\t86.49\t88.27\t88.57\t88.79\t88.96\t89.09\t89.19\t89.26\t89.31\t89.35'),
            # YD
            # ('TRE_T', ),  # T
            ('HH_N__DEM_GOOD_N',
             'None\t86.48667\t86.48656\t86.48655\t86.48654\t87.55877\t88.02118\t88.37395\t88.64268\t88.84701\t89.00206'),
            ('HH_N__SUP_LAB_N',
             'None\t106.4866\t106.4866\t106.4866\t106.4865\t108.7204\t109.0749\t109.3441\t109.5482\t109.7027\t109.8192\t109.9068\t109.9724\t110.0213\t110.0575\t110.0841\t110.1035'),
            ('HH_S__AfterTax',
             '86.48666\t86.48656\t86.48655\t86.48654\t86.48654\t84.37456\t84.20819\t84.07316\t83.96609\t83.88098\t83.81313\t83.75889\t83.7154\t83.68043\t83.65222\t83.62939\t83.61085\t83.59574\t83.58338\t83.57325\t83.5649\t83.55801\t83.5523\t83.54755\t83.5436\t83.54028\t83.53751\t83.53517\t83.5332\t83.53154\t83.53013\t83.52893'),
            ('HH_N__DEM_MON',
             'None\t21.62\t21.62\t21.62\t21.62\t21.81\t21.95\t22.05\t22.13\t22.19\t22.23\t22.26\t22.29'),
            # high-powered money (H)
        ]
        return out


class REG2(GL_book_model): # pragma: no cover
    """
    Implements Model REG from Chapter 6 of G&L. REG = "Regional."

    This version of REG splits the model into three "countries."
    - Central government sector
    - Region (Province) #1 - The North
    - Region (Province) #2 - The South

    Ignores any existing model that is passed in; the entire Model object is built
    from scratch.
    """

    def build_country(self, model, paramz):
        """
        Builds a country object.
        :param model: Model
        :param paramz: dict
        :return: None
        """
        country_name = paramz['Country Name']
        country = Region(model, code=paramz['Country'], long_name=country_name)
        self.Country = country
        hh = Household(country, code='HH', long_name='Household ' + country_name)
        goods = Market(country, 'GOOD', 'Goods market ' + country_name)
        bus = FixedMarginBusinessMultiOutput(country, 'BUS', 'Business Sector', market_list=[goods, ])
        goods.AddSupplier(bus)
        goods.AddVariable('MU', 'Propensity to import', paramz['mu'])
        labour = Market(country, 'LAB', 'Labour market: ' + country_name)

        # Create the goods demand function

        # I normally would not commit a file in a half-finished state, but I want to make sure
        # that I upload a lot of key changes to GitHub. The work in this class should have been
        # done in a different branch; oops.

        # Create the demand for deposits.  ('MON' is the residual asset.)
        hh.AddVariable('L0', 'lambda_0: share of bills in wealth', paramz['L0'])
        hh.AddVariable('L1', 'lambda_1: parameter related to interest rate', paramz['L1'])
        hh.AddVariable('L2', 'lambda_2: parameter related to disposable income', paramz['L2'])
        # Generate the equation. Need to get the name of the interest rate variable
        r = model['GOV']['DEP'].GetVariableName('r')
        # The format() call will replace '{0}' with the contents of the 'r' variable.
        eqn = 'L0 + L1 * {0} - L2 * (AfterTax/F)'.format(r)
        hh.GenerateAssetWeighting([('DEP', eqn)], 'MON')

    def other_country(self, country):
        if country == 'N':
            return 'S'
        return 'N'

    def generate_supply_allocation(self, mod, country):
        Y = mod[country]['HH'].GetVariableName('INC')
        other = self.other_country(country)
        market = mod[country]['GOOD']
        market.AddSupplier(mod[other]['BUS'], 'MU*{0}'.format(Y))
        mod[other]['BUS'].AddMarket(market)

    def build_model(self):
        """

        :return: Model
        """
        model = Model()
        central_gov = Region(model, code='GOV', long_name='Central Government Sector')
        tre = Treasury(central_gov, 'TRE', 'Treasury')
        cb = CentralBank(central_gov, 'CB', 'Central Bank', tre)
        mm = MoneyMarket(central_gov,issuer_short_code='CB')
        dep = DepositMarket(central_gov, issuer_short_code='TRE')
        tax = TaxFlow(central_gov, 'TF', 'TaxFlow', taxrate=.2, taxes_paid_to='TRE')
        tre.SetEquationRightHandSide('DEM_GOOD','DEM_N_GOOD + DEM_S_GOOD')
        tre.AddVariable('DEM_N_GOOD', 'Demand for goods in the North', '')
        tre.AddVariable('DEM_S_GOOD', 'Demand for goods in the South', '')

        paramz = {
            'Country': 'N',
            'Country Name': 'North',
            'alpha_income': .6,
            'alpha_fin': .4,
            'mu': '0.18761',
            'L0': '0.635',
            'L1': '5.',
            'L2': '.01',
        }
        self.build_country(model, paramz)
        paramz = {
            'Country': 'S',
            'Country Name': 'South',
            'alpha_income': .7,
            'alpha_fin': .3,
            'mu': '0.18761',
            'L0': '0.67',
            'L1': '6.',
            'L2': '.07',
        }
        self.build_country(model, paramz)
        self.generate_supply_allocation(model, 'N')
        self.generate_supply_allocation(model, 'S')
        self.Model = model
        if self.UseBookExogenous:
            # Need to set the exogenous variable - Government demand for Goods ("G" in economist symbology)
            tre.SetExogenous('DEM_N_GOOD', '[20.,] * 105')
            tre.SetExogenous('DEM_S_GOOD', '[20.,] * 105')
            dep.SetExogenous('r', '[.025,]*105')
            model['S']['GOOD'].SetExogenous('MU', [0.18781] * 5 + [0.20781] * 105)
            # NOTE:
            # Initial conditions are only partial; there may be issues with some
            # variables.
            self.Model.AddInitialCondition('N_HH', 'AfterTax', 86.486)
            self.Model.AddInitialCondition('S_HH', 'AfterTax', 86.486)
            self.Model.AddInitialCondition('N_HH', 'F', 86.486)
            self.Model.AddInitialCondition('N_HH', 'DEM_DEP', 64.865)
            self.Model.AddInitialCondition('S_HH', 'F', 86.486)
            self.Model.AddInitialCondition('S_HH', 'DEM_DEP', 64.865)
            self.Model.AddInitialCondition('GOV_TRE', 'F', 2. * -86.486)
            self.Model.AddGlobalEquation('t', 'decorated time axis', '1955. + k')
        return self.Model

    # noinspection PyPep8,PyPep8,PyPep8,PyPep8,PyPep8
    def expected_output(self):
        """
        Expected output for the model (using default input).
        Based on EViews output using code from Gennaro Zezza (from sfcmodels.net)

        NOTE: A spreadsheet at sfcmodels.net gives different output; income is changing during the
        same period as the rate change.

        We ignore value at t=0
        :return: list
        """
        out = [
            ('t', [None, 1956., 1957., 1958., ]),
            ('GOV_TRE__DEM_GOOD', [None, 40., 40., 40., 40.]),  # G
            ('GOV_DEP__r', [0.025, ] * 10),
            ('N_HH__WGT_DEP', [None, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, ]),
            # Weight of deposits (bills)
            ('N_HH__AfterTax',
             '86.49\t86.49\t86.49\t86.49\t86.49\t88.27\t88.57\t88.79\t88.96\t89.09\t89.19\t89.26\t89.31\t89.35'),
            # YD
            # ('TRE_T', ),  # T
            ('N_HH__DEM_GOOD',
             'None\t86.48667\t86.48656\t86.48655\t86.48654\t87.55877\t88.02118\t88.37395\t88.64268\t88.84701\t89.00206'),
            ('N_HH__SUP_LAB',
             'None\t106.4866\t106.4866\t106.4866\t106.4865\t108.7204\t109.0749\t109.3441\t109.5482\t109.7027\t109.8192\t109.9068\t109.9724\t110.0213\t110.0575\t110.0841\t110.1035'),
            ('S_HH__AfterTax',
             '86.48666\t86.48656\t86.48655\t86.48654\t86.48654\t84.37456\t84.20819\t84.07316\t83.96609\t83.88098\t83.81313\t83.75889\t83.7154\t83.68043\t83.65222\t83.62939\t83.61085\t83.59574\t83.58338\t83.57325\t83.5649\t83.55801\t83.5523\t83.54755\t83.5436\t83.54028\t83.53751\t83.53517\t83.5332\t83.53154\t83.53013\t83.52893'),
            ('N_HH__DEM_MON',
             'None\t21.62\t21.62\t21.62\t21.62\t21.81\t21.95\t22.05\t22.13\t22.19\t22.23\t22.26\t22.29'),
            # high-powered money (H)
        ]
        return out


class OPENG(GL_book_model): # pragma: no cover
    """
    Implements Model OPENG from Chapter 6 of G&L. OPENG = "Open, with G adjustment"

    Ignores any existing model that is passed in; the entire Model object is built
    from scratch.

    NOTE: Still under development.
    """

    def build_country(self, model, paramz):
        """
        Builds a country object.
        :param model: Model
        :param paramz: dict
        :return: None
        """
        country_name = paramz['Country Name']
        country = Country(model, code=paramz['Country'], long_name=country_name)
        self.Country = country
        tre = Treasury(country, 'TRE', 'Treasury')
        cb = GoldStandardCentralBank(country, 'CB', 'Central Bank', tre)
        mm = MoneyMarket(country)
        dep = DepositMarket(country)
        tax = TaxFlow(country, 'TF', 'TaxFlow', .2)

        hh = Household(country, code='HH', long_name='Household ' + country_name)
        goods = Market(country, 'GOOD', 'Goods market ' + country_name)
        bus = FixedMarginBusinessMultiOutput(country, 'BUS', 'Business Sector', [goods, ])
        goods.AddSupplier(bus)
        goods.AddVariable('MU', 'Propensity to import', paramz['mu'])
        labour = Market(country, 'LAB', 'Labour market: ' + country_name)

        # Create the goods demand function

        # I normally would not commit a file in a half-finished state, but I want to make sure
        # that I upload a lot of key changes to GitHub. The work in this class should have been
        # done in a different branch; oops.

        # Create the demand for deposits.  ('MON' is the residual asset.)
        hh.AddVariable('L0', 'lambda_0: share of bills in wealth', paramz['L0'])
        hh.AddVariable('L1', 'lambda_1: parameter related to interest rate', paramz['L1'])
        hh.AddVariable('L2', 'lambda_2: parameter related to disposable income', paramz['L2'])
        # Generate the equation. Need to get the name of the interest rate variable
        r = dep.GetVariableName('r')
        # The format() call will replace '{0}' with the contents of the 'r' variable.
        eqn = 'L0 + L1 * {0} - L2 * (AfterTax/F)'.format(r)
        hh.GenerateAssetWeighting([('DEP', eqn)], 'MON')

    def other_country(self, country):
        if country == 'N':
            return 'S'
        return 'N'

    def generate_supply_allocation(self, mod, country):
        Y = mod[country]['HH'].GetVariableName('INC')
        other = self.other_country(country)
        market = mod[country]['GOOD']
        market.AddSupplier(mod[other]['BUS'], 'MU*{0}'.format(Y))
        mod[other]['BUS'].AddMarket(market)

    def build_model(self):
        """

        :return: Model
        """
        model = Model()
        ExternalSector(model)
        paramz = {
            'Country': 'N',
            'Country Name': 'North',
            'alpha_income': .6,
            'alpha_fin': .4,
            'mu': '0.18761',
            'L0': '0.635',
            'L1': '5.',
            'L2': '.01',
        }
        self.build_country(model, paramz)
        paramz = {
            'Country': 'S',
            'Country Name': 'South',
            'alpha_income': .7,
            'alpha_fin': .3,
            'mu': '0.18761',
            'L0': '0.67',
            'L1': '6.',
            'L2': '.07',
        }
        self.build_country(model, paramz)
        self.generate_supply_allocation(model, 'N')
        self.generate_supply_allocation(model, 'S')
        self.Model = model
        if self.UseBookExogenous:
            # Need to set the exogenous variable - Government demand for Goods ("G" in economist symbology)
            model['N']['TRE'].SetExogenous('DEM_GOOD', '[20.,] * 105')
            model['S']['TRE'].SetExogenous('DEM_GOOD', '[20.,] * 105')
            model['N']['DEP'].SetExogenous('r', '[.025,]*105')
            model['S']['DEP'].SetExogenous('r', '[.025,]*105')
            model['S']['GOOD'].SetExogenous('MU', [0.18781] * 5 + [0.20781] * 105)
            # NOTE:
            # Initial conditions are only partial; there may be issues with some
            # variables.
            self.Model.AddInitialCondition('N_HH', 'AfterTax', 86.486)
            self.Model.AddInitialCondition('S_HH', 'AfterTax', 86.486)
            self.Model.AddInitialCondition('N_HH', 'F', 86.486)
            self.Model.AddInitialCondition('N_HH', 'DEM_DEP', 64.865)
            self.Model.AddInitialCondition('S_HH', 'F', 86.486)
            self.Model.AddInitialCondition('S_HH', 'DEM_DEP', 64.865)
            self.Model.AddInitialCondition('N_TRE', 'F', -86.486)
            self.Model.AddInitialCondition('S_TRE', 'F', -86.486)
            self.Model.AddGlobalEquation('t', 'decorated time axis', '1955. + k')
        return self.Model

    # noinspection PyPep8,PyPep8,PyPep8,PyPep8,PyPep8
    def expected_output(self):
        """
        Expected output for the model (using default input).
        Based on EViews output using code from Gennaro Zezza (from sfcmodels.net)

        NOTE: A spreadsheet at sfcmodels.net gives different output; income is changing during the
        same period as the rate change.

        We ignore value at t=0
        :return: list
        """
        out = [
            ('t', [None, 1956., 1957., 1958., ]),
            ('GOV_TRE__DEM_GOOD', [None, 40., 40., 40., 40.]),  # G
            ('GOV_DEP__r', [0.025, ] * 10),
            ('N_HH__WGT_DEP', [None, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, ]),
            # Weight of deposits (bills)
            ('N_HH__AfterTax',
             '86.49\t86.49\t86.49\t86.49\t86.49\t88.27\t88.57\t88.79\t88.96\t89.09\t89.19\t89.26\t89.31\t89.35'),
            # YD
            # ('TRE_T', ),  # T
            ('N_HH__DEM_GOOD',
             'None\t86.48667\t86.48656\t86.48655\t86.48654\t87.55877\t88.02118\t88.37395\t88.64268\t88.84701\t89.00206'),
            ('N_HH__SUP_LAB',
             'None\t106.4866\t106.4866\t106.4866\t106.4865\t108.7204\t109.0749\t109.3441\t109.5482\t109.7027\t109.8192\t109.9068\t109.9724\t110.0213\t110.0575\t110.0841\t110.1035'),
            ('S_HH__AfterTax',
             '86.48666\t86.48656\t86.48655\t86.48654\t86.48654\t84.37456\t84.20819\t84.07316\t83.96609\t83.88098\t83.81313\t83.75889\t83.7154\t83.68043\t83.65222\t83.62939\t83.61085\t83.59574\t83.58338\t83.57325\t83.5649\t83.55801\t83.5523\t83.54755\t83.5436\t83.54028\t83.53751\t83.53517\t83.5332\t83.53154\t83.53013\t83.52893'),
            ('N_HH__DEM_MON',
             'None\t21.62\t21.62\t21.62\t21.62\t21.81\t21.95\t22.05\t22.13\t22.19\t22.23\t22.26\t22.29'),
            # high-powered money (H)
        ]
        return out