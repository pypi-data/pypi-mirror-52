from unittest import TestCase

from sfc_models.models import Model, Country
from sfc_models.sector_definitions import *


def kill_spaces(s):
    """
    remove spaces from a string; makes testing easier as white space conventions may change in equations
    :param s:
    :return:
    """
    s = s.replace(' ', '')
    return s


class TestHouseHold(TestCase):
    def test_GenerateEquations_alpha(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        hh = Household(can, 'HH', 'Household', alpha_fin=0.2, alpha_income=0.9)
        hh._GenerateEquations()
        self.assertEqual(hh.EquationBlock['AlphaFin'].RHS(), '0.2000')
        self.assertEqual(hh.EquationBlock['AlphaIncome'].RHS(), '0.9000')

class TestMultiSupply(TestCase):
    # Changed behaviour
    # def test_constructor_nosupply(self):
    #     mod = Model()
    #     can = Country(mod, 'Canada', 'Eh')
    #     with self.assertRaises(utils.LogicError):
    #         bus= FixedMarginBusinessMultiOutput(can, 'Business', 'BUS', market_list=[])


    def test_ctor_default(self):
        mod = Model()
        can = Country(mod, 'CA', 'Canada', currency='LOC')
        marca = Market(can, 'GOOD', 'market')
        us = Country(mod, 'US', 'US', currency='LOC')
        marus = Market(us, 'GOOD', 'market')
        bus = FixedMarginBusinessMultiOutput(can, 'BUS', 'Business', market_list=[marca, marus])
        bus2 = FixedMarginBusinessMultiOutput(us, 'BUS', 'Business', market_list=[marca, marus],
                                              profit_margin=.1)
        self.assertIn('SUP_GOOD', bus.EquationBlock.Equations)
        self.assertIn('SUP_US_GOOD', bus.EquationBlock.Equations)
        marus.AddSupplier(bus2, 'allocation_equation')
        marus.AddSupplier(bus)
        #marus.SupplyAllocation = [[[bus2, 'allocation_equation'],], bus]
        mod._GenerateFullSectorCodes()
        marus._GenerateEquations()
        self.assertFalse(marus.ShareParent(bus))
        self.assertEqual('US_GOOD__SUP_CA_BUS', bus.EquationBlock['SUP_US_GOOD'].RHS())
        self.assertEqual('US_GOOD__SUP_US_BUS', bus2.EquationBlock['SUP_GOOD'].RHS())
        bus2._GenerateEquations()
        self.assertEqual('0.900*SUP', bus2.EquationBlock['DEM_LAB'].RHS())
        self.assertEqual('SUP_CA_GOOD+SUP_GOOD', bus2.EquationBlock['SUP'].RHS())

class TestDoNothingGovernment(TestCase):
    def test_GenerateEquations(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        gov = ConsolidatedGovernment(can, 'GOV', 'Government')
        gov._GenerateEquations()
        self.assertEqual(gov.EquationBlock['DEM_GOOD'].RHS(), '0.0')

    def test_missing_tax(self):
        """
        Test that we can run without TaxFlow without errors.
        :return:
        """
        mod = Model()
        can = Country(mod, 'CA')
        ConsolidatedGovernment(can, 'GOV')
        mod.EquationSolver.MaxTime = 1
        mod.main()


class TestTreasury(TestCase):
    def test_GenerateEquations(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        gov = Treasury(can, 'GOV', 'Government')
        gov._GenerateEquations()
        self.assertEqual(gov.EquationBlock['DEM_GOOD'].RHS(), '0.0')

    def test_missing_tax(self):
        """
        Just make sure we can build the moddel without throwing an error.
        :return:
        """
        mod = Model()
        can = Country(mod, 'CA')
        tre = Treasury(can, 'TRE')
        mod.EquationSolver.MaxTime = 1
        mod.main()


class TestCentralBank(TestCase):
    def test_GenerateEquations(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        tre = Treasury(can, 'TRE', 'Treasury')
        cb = CentralBank(can, 'CB', 'Central Bank', tre)
        mod._GenerateFullSectorCodes()
        cb._GenerateEquations()
        self.assertEqual(cb.Treasury, tre)

    def test_name(self):
        mod = Model()
        ca = Country(mod, 'CA')
        cb = CentralBank(ca, 'CB')
        self.assertIn('CB', cb.LongName)
        self.assertIn('CA', cb.LongName)


class TestTaxFlow(TestCase):
    def test_GenerateEquations(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        tf = TaxFlow(can, 'Tax', taxrate=.1, taxes_paid_to='GOV')  # Supply side for the win!
        self.assertTrue('T' in tf.EquationBlock.Equations)
        self.assertTrue('TaxRate' in tf.EquationBlock.Equations)
        hh = Household(can, 'HH', 'Household')
        gov = ConsolidatedGovernment(can, 'GOV', 'Gummint')
        mod._GenerateFullSectorCodes()
        tf._GenerateEquations()
        self.assertEqual('0.1000', tf.EquationBlock['TaxRate'].RHS())
        self.assertEqual('Tax__TaxRate*HH__INC', tf.EquationBlock['T'].RHS().replace(' ', ''))
        self.assertIn('-T',hh.EquationBlock['F'].RHS())
        self.assertEqual('Tax__TaxRate*HH__INC', hh.EquationBlock['T'].RHS())
        self.assertEqual('LAG_F+T', gov.EquationBlock['F'].RHS())
        self.assertEqual('Tax__T', gov.EquationBlock['T'].RHS())

    def test_GenerateEquationsSpecialised(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        tf = TaxFlow(can, 'Tax', 'Taxation Flows', .1)
        self.assertTrue('T' in tf.EquationBlock.Equations)
        self.assertTrue('TaxRate' in tf.EquationBlock.Equations)
        hh = Household(can, 'HH', 'Household')
        hh.AddVariable('TaxRate', 'Sector level tax rate', '0,2')
        gov = ConsolidatedGovernment(can, 'GOV', 'Gummint')
        mod._GenerateFullSectorCodes()
        tf._GenerateEquations()
        self.assertEqual('0.1000', tf.EquationBlock['TaxRate'].RHS())
        self.assertEqual('HH__TaxRate*HH__INC', tf.EquationBlock['T'].RHS().replace(' ', ''))
        self.assertIn('-T', hh.EquationBlock['F'].RHS())
        self.assertEqual('HH__TaxRate*HH__INC', hh.EquationBlock['T'].RHS())
        # self.assertEqual(['+T', ], gov.CashFlows)
        self.assertEqual('Tax__T', gov.EquationBlock['T'].RHS())


class TestFixedMarginBusiness(TestCase):
    def test_ctor_default(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        bus = FixedMarginBusiness(can, 'BUS')
        self.assertEqual(0., bus.ProfitMargin)
        mar = Market(can, 'GOOD', 'market')
        mod._GenerateFullSectorCodes()
        bus._GenerateEquations()
        self.assertEqual('GOOD__SUP_GOOD', bus.EquationBlock['DEM_LAB'].RHS().replace(' ', ''))

    def test_GenerateEquations(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        bus = FixedMarginBusiness(can, 'BUS', 'Business', profit_margin=0.1)
        mar = Market(can, 'GOOD', 'market')
        mod._GenerateFullSectorCodes()
        bus._GenerateEquations()
        self.assertEqual('0.900*GOOD__SUP_GOOD', bus.EquationBlock['DEM_LAB'].RHS().replace(' ', ''))

    def test_no_market(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        bus = FixedMarginBusiness(can, 'BUS', 'Business')
        with self.assertRaises(Warning):
            bus._GenerateEquations()

class TestCapitalists(TestCase):
    def test_dividend(self):
        mod = Model()
        can = Country(mod, 'CA', 'Canada')
        us = Country(mod, 'US', 'US of A')
        bus = FixedMarginBusiness(can, 'BUS', 'Business')
        mar = Market(can, 'GOOD', 'market')
        cap = Capitalists(can, 'CAP', 'Capitalists', .4)
        mod._GenerateFullSectorCodes()
        bus._GenerateEquations()
        self.assertEqual('CA_BUS__PROF', cap.EquationBlock['DIV'].RHS())

    def test_generate_eqn(self):
        mod = Model()
        ca = Country(mod, 'CA')
        cap = Capitalists(ca, 'CAP')
        cap.AlphaIncome = 0.99
        cap.AlphaFin = 0.11
        cap._GenerateEquations()
        self.assertEqual('0.9900', cap.EquationBlock['AlphaIncome'].RHS())
        self.assertEqual('0.1100', cap.EquationBlock['AlphaFin'].RHS())


class TestMoneyMarket(TestCase):
    def test_all(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        gov = ConsolidatedGovernment(can, 'GOV', 'Government')
        hou = Household(can, 'HH', 'Household', .5)
        hou2 = Household(can, 'HH2', 'Household2', .5)
        mm = MoneyMarket(can)
        mod._GenerateFullSectorCodes()
        mod._GenerateEquations()
        # Supply = Demand
        self.assertEqual('GOV__SUP_MON', mm.EquationBlock['SUP_MON'].RHS())
        # Demand = Demand of two sectors
        self.assertEqual('HH__DEM_MON+HH2__DEM_MON', mm.EquationBlock['DEM_MON'].RHS().replace(' ', ''))
        # At the sector level, demand = F
        self.assertEqual('HH__F', hou.EquationBlock['DEM_MON'].RHS())
        self.assertEqual('HH2__F', hou2.EquationBlock['DEM_MON'].RHS())


class TestDepositMarket(TestCase):
    def test_all(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        gov = ConsolidatedGovernment(can, 'GOV', 'Government')
        hou = Household(can, 'HH', 'Household', .5)
        dummy = Sector(can, 'DUM', 'Dummy')
        mm = MoneyMarket(can)
        dep = DepositMarket(can)
        # Need to add demand functions in household sector
        mod._GenerateFullSectorCodes()
        hou.AddVariable('DEM_MON', 'Demand for Money', '0.5 * ' + hou.GetVariableName('F'))
        hou.AddVariable('DEM_DEP', 'Demand for Deposits', '0.5 * ' + hou.GetVariableName('F'))
        mod._GenerateEquations()
        # Supply = Demand
        self.assertEqual('GOV__SUP_DEP', dep.EquationBlock['SUP_DEP'].RHS())
        # Demand = Demand of two sectors
        self.assertEqual('HH__DEM_DEP', dep.EquationBlock['DEM_DEP'].RHS().replace(' ', ''))
        # At the sector level, demand = F
        self.assertEqual('0.5*HH__F', kill_spaces(hou.EquationBlock['DEM_MON'].RHS()))
        self.assertEqual('0.5*HH__F', kill_spaces(hou.EquationBlock['DEM_DEP'].RHS()))
        # Make sure the dummy does not have cash flows
        self.assertEqual('LAG_F', dummy.EquationBlock['F'].RHS())
        # Household has a deposit interest cash flow
        self.assertIn('INTDEP', hou.EquationBlock['F'].RHS())
