from unittest import TestCase
import doctest

import sfc_models.sector
from sfc_models.models import Model, Country
from sfc_models.sector import Sector, Market
from sfc_models.sector_definitions import Household
from sfc_models.utils import LogicError
from test.test_models import kill_spaces

def load_tests(loader, tests, ignore):
    """
    Load doctests, so unittest discovery can find them.
    """
    tests.addTests(doctest.DocTestSuite(sfc_models.sector))
    return tests


class TestSector(TestCase):
    def test_ctor_chain(self):
        mod = Model()
        country = Country(mod, 'US', 'USA! USA!')
        household = Sector(country, 'HH', 'Household')
        self.assertEqual(household.Parent.Code, 'US')
        self.assertEqual(household.Parent.Parent.Code, '')

    def test_HasNoF(self):
        mod = Model()
        country = Country(mod, 'code', 'name')
        sec = Sector(country, 'Code', 'Name', has_F=False)
        self.assertNotIn('F', sec.GetVariables())

    def test_BadUnderBars(self):
        mod = Model()
        country = Country(mod, 'US', 'US')
        sec = Sector(country, 'B__A__D', 'Bad')
        sec.AddVariable('foo', 'desc', 'x')
        sec2 = Sector(country, 'OK', 'OK sector')
        mod._GenerateFullSectorCodes()
        with self.assertRaises(ValueError):
            sec.GetVariableName('foo')
        with self.assertRaises(ValueError):
            sec2.AddVariable('b__ad', 'desc', 'x')
        # Force it in..
        # Do not go through the constructor, in case the EquationBlock
        # enforces the naming convention
        sec2.EquationBlock.Equations['b__ad'] = 'Dummy'
        with self.assertRaises(ValueError):
            sec2.GetVariableName('b__ad')

    def test_GetVariables(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        # Need to block the automatic creation of F, INC
        can_hh = Sector(can, 'HH', 'Household', has_F=False)
        can_hh.AddVariable('y', 'Vertical axis', '2.0')
        can_hh.AddVariable('x', 'Horizontal axis', 'y - t')
        self.assertEqual(can_hh.GetVariables(), ['x', 'y'])

    def test_GetVariableName_1(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        household = Household(us, 'HH', 'Household', .9)
        mod._GenerateFullSectorCodes()
        household._GenerateEquations()
        self.assertEqual(household.GetVariableName('AlphaFin'), 'HH__AlphaFin')

    def test_GetVariableName_2(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        household = Household(us, 'HH', 'Household', .9)
        ID = household.ID
        target = '_{0}__{1}'.format(ID, 'AlphaFin')
        self.assertEqual(target, household.GetVariableName('AlphaFin'))

    def test_GetVariableName_3(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        hh = Sector(us, 'HH', 'Household')
        mod._GenerateFullSectorCodes()
        with self.assertRaises(KeyError):
            hh.GetVariableName('Kaboom')

    def test_AddCashFlow(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.AddCashFlow('A', 'H_A', 'Desc A')
        s.AddCashFlow('- B', 'H_B', 'Desc B')
        s.AddCashFlow(' - C', 'H_C', 'Desc C')
        self.assertEqual('LAG_F+A-B-C', s.EquationBlock['F'].RHS())

    def test_AddCashFlow_2(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.AddCashFlow('A', 'equation', 'Desc A')
        s.AddCashFlow('', 'equation', 'desc')
        with self.assertRaises(ValueError):
            s.AddCashFlow('-', 'B', 'Desc B')
        with self.assertRaises(ValueError):
            s.AddCashFlow('+', 'X', 'Desc C')
        self.assertEqual('LAG_F+A', s.EquationBlock['F'].RHS())
        self.assertEqual('equation', s.EquationBlock['A'].RHS())

    def test_AddCashFlow_3(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.AddVariable('X', 'desc', '')
        s.AddCashFlow('X', 'equation', 'Desc A')
        self.assertEqual('equation', s.EquationBlock['X'].RHS())

    def test_AddCashFlow_bad(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.AddVariable('X', 'desc', '')
        with self.assertRaises(NotImplementedError):
            # Must be a simple variable as the cash flow
            s.AddCashFlow('f(X)', 'equation', 'Desc A')

    def test_AddInitialConditions(self):
        mod = Model()
        us = Country(mod, 'US', 'desc')
        s = Sector(us, 'HH', 'desc', has_F=False)
        s.AddVariable('x', 'desc','1.0')
        s.AddInitialCondition('x', '10.0')
        targ = [(s.ID, 'x', '10.0'), ]
        self.assertEqual(targ, mod.InitialConditions)

    def test_GenerateIncomeEquations(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        self.assertEqual('LAG_F', s.EquationBlock['F'].RHS())
        self.assertEqual('F(k-1)', s.EquationBlock['LAG_F'].RHS())

    def test_GenerateIncomeEquations_2(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.AddCashFlow('X', 'eq')
        self.assertEqual('LAG_F+X', s.EquationBlock['F'].RHS())
        self.assertEqual('F(k-1)', s.EquationBlock['LAG_F'].RHS())

    def test_GenerateIncomeEquations_3(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.AddCashFlow('X', 'eq')
        s.AddCashFlow('Y', 'eq2')
        self.assertEqual('LAG_F+X+Y', s.EquationBlock['F'].RHS())
        self.assertEqual('F(k-1)', s.EquationBlock['LAG_F'].RHS())

    def test_GenerateFinalEquations(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household', has_F=False)
        mod._GenerateFullSectorCodes()
        # Can no longer directly inject data into the Sector object
        s.AddVariableFromEquation('x=a+1 # foo')
        s.AddVariableFromEquation('a=cat')
        out = s._CreateFinalEquations()
        # Since F has an empty equation, does not appear.
        targ = [('HH__a', 'cat', '[a] '), ('HH__x', 'HH__a+1', '[x] foo')]
        # Kill spacing in equations
        out = [(x[0], x[1].replace(' ', ''), x[2]) for x in out]
        self.assertEqual(targ, out)

    def test_GenerateAssetWeightings_1(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.GenerateAssetWeighting((), 'MON')
        self.assertEqual('1.0', s.EquationBlock['WGT_MON'].RHS())
        self.assertEqual('F*WGT_MON', kill_spaces(s.EquationBlock['DEM_MON'].RHS()))

    def test_IncomeEquation(self):
        mod = Model()
        us = Country(mod, 'US', 'US')
        hh = Sector(us, 'HH', 'HH')
        hh.AddCashFlow('x', eqn='2.0', is_income=True)
        mod._GenerateFullSectorCodes()
        self.assertEqual('x', hh.EquationBlock['INC'].RHS())

    def test_IncomeEquation_2(self):
        mod = Model()
        us = Country(mod, 'US', 'US')
        hh = Sector(us, 'HH', 'HH', has_F=True)
        hh.AddCashFlow('x', eqn='2.0', is_income=False)
        mod._GenerateFullSectorCodes()
        self.assertEqual('0.0', hh.EquationBlock['INC'].RHS())

    def test_GenerateAssetWeightings_2(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.GenerateAssetWeighting([('BOND', '0.5'), ], 'MON')
        self.assertEqual('0.5', s.EquationBlock['WGT_BOND'].RHS())
        self.assertEqual('F*WGT_BOND', kill_spaces(s.EquationBlock['DEM_BOND'].RHS()))
        self.assertEqual('1.0-WGT_BOND', kill_spaces(s.EquationBlock['WGT_MON'].RHS()))
        self.assertEqual('F*WGT_MON', kill_spaces(s.EquationBlock['DEM_MON'].RHS()))

    def test_GenerateAssetWeightingAbsolute(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        with self.assertRaises(NotImplementedError):
            s.GenerateAssetWeighting([('BOND', '0.5'), ], 'MON',
                                     is_absolute_weighting=True)

    def test_SetExogenous(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.SetExogenous('varname', 'val')
        self.assertEqual([(s, 'varname', 'val'), ], mod.Exogenous)

    def test_setRHS(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        s = Sector(us, 'HH', 'Household')
        s.AddVariable('foo', 'variable foo', 'x')
        self.assertEqual('x', s.EquationBlock['foo'].RHS())
        s.SetEquationRightHandSide('foo', 'y')
        self.assertEqual('y', s.EquationBlock['foo'].RHS())
        with self.assertRaises(KeyError):
            s.SetEquationRightHandSide('LittleBunnyFooFoo', 'z')

    def test_AddTerm(self):
        mod = Model()
        us = Country(mod, 'US', 'USA! USA!')
        s = Sector(us, 'SEC', 'Desc')
        s.AddVariable('SUP_GOOD', 'Supply of goods', '')
        s.AddTermToEquation('SUP_GOOD', 'Kaboom')
        self.assertEqual('Kaboom', s.EquationBlock['SUP_GOOD'].RHS())

    def test_AddTerm_KeyError(self):
        mod = Model()
        us = Country(mod, 'US', 'USA! USA!')
        s = Sector(us, 'SEC', 'Desc')
        with self.assertRaises(KeyError):
            s.AddTermToEquation('SUP', 'x')

    def test_IsSharedCurrencyZone(self):
        mod = Model()
        ca = Country(mod, 'CA', 'Name', currency='CAD')
        ca_h = Sector(ca, 'HH', 'Sec')
        us = Country(mod, 'US', 'Name', currency='RMB')
        us_h = Sector(us, 'HH', 'name')
        china = Country(mod, 'China', 'Name', currency='RMB')
        china_h = Sector(china, 'HH', 'name')
        self.assertFalse(ca_h.IsSharedCurrencyZone(us_h))
        self.assertFalse(us_h.IsSharedCurrencyZone(ca_h))
        self.assertTrue(us_h.IsSharedCurrencyZone(china_h))

class TestMarket(TestCase):
    def test_GenerateEquations(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        hh = Sector(can, 'HH', 'Household')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB', 'desc 2', '')
        mod._GenerateFullSectorCodes()
        mar._GenerateEquations()
        self.assertIn('-DEM_LAB', bus.EquationBlock['F'].RHS())
        self.assertEqual('x', bus.EquationBlock['DEM_LAB'].RHS())
        self.assertEqual('LAG_F+SUP_LAB', hh.EquationBlock['F'].RHS())
        # self.assertEqual('BUS_DEM_LAB', hh.Equations['SUP_LAB'].strip())
        self.assertEqual('SUP_LAB', mar.EquationBlock['SUP_HH'].RHS())
        self.assertEqual('LAB__SUP_HH', hh.EquationBlock['SUP_LAB'].RHS().strip())

    def test_GenerateEquations_no_supply(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        bus.AddVariable('DEM_LAB', 'desc', '')
        mod._GenerateFullSectorCodes()
        with self.assertRaises(ValueError):
            mar._GenerateEquations()

    def test_GenerateEquations_2_supply_fail(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        hh = Sector(can, 'HH', 'Household')
        hh2 = Sector(can, 'HH2', 'Household')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB', 'desc 2', '')
        hh2.AddVariable('SUP_LAB', 'desc 2', '')
        mod._GenerateFullSectorCodes()
        with self.assertRaises(LogicError):
            mar._GenerateEquations()

    def test_GenerateEquations_2_supply(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        hh = Sector(can, 'HH', 'Household')
        hh2 = Sector(can, 'HH2', 'Household')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB', 'desc 2', '')
        hh2.AddVariable('SUP_LAB', 'desc 2', '')
        mod._GenerateFullSectorCodes()
        mar.AddSupplier(hh2)
        mar.AddSupplier(hh, 'SUP_LAB/2')
        # mar.SupplyAllocation = [[(hh, 'SUP_LAB/2')], hh2]
        mar._GenerateEquations()
        self.assertEqual('SUP_LAB/2', mar.EquationBlock['SUP_HH'].RHS())
        self.assertEqual('SUP_LAB-SUP_HH', kill_spaces(mar.EquationBlock['SUP_HH2'].RHS()))
        self.assertEqual('LAB__SUP_HH', hh.EquationBlock['SUP_LAB'].RHS())
        self.assertEqual('LAB__SUP_HH2', hh2.EquationBlock['SUP_LAB'].RHS())

    def test_GenerateEquations_insert_supply(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        hh = Sector(can, 'HH', 'Household')
        hh2 = Sector(can, 'HH2', 'Household')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB_WRONG_CODE', 'desc 2', '')
        hh2.AddVariable('SUP_LAB_WRONG_CODE', 'desc 2', '')
        mod._GenerateFullSectorCodes()
        mar.AddSupplier(hh2)
        mar.AddSupplier(hh, 'SUP_LAB/2')
        # mar.SupplyAllocation = [[(hh, 'SUP_LAB/2')], hh2]
        mar._GenerateEquations()
        self.assertEqual('SUP_LAB/2', mar.EquationBlock['SUP_HH'].RHS())
        self.assertEqual('SUP_LAB-SUP_HH', kill_spaces(mar.EquationBlock['SUP_HH2'].RHS()))
        self.assertEqual('LAB__SUP_HH', hh.EquationBlock['SUP_LAB'].RHS())
        self.assertEqual('LAB__SUP_HH2', hh2.EquationBlock['SUP_LAB'].RHS())

    def test_GenerateEquations_2_supply_multicountry(self):
        mod = Model()
        # Have to have the same currency for this test
        can = Country(mod, 'CA', 'Canada, Eh?', currency='LOC')
        US = Country(mod, 'US', 'USA! USA!', currency='LOC')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        hh = Sector(can, 'HH', 'Household')
        # Somehow, Americans are supplying labour in Canada...
        hh2 = Sector(US, 'HH2', 'Household')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB', 'desc 2', '')
        hh2.AddVariable('SUP_CA_LAB', 'desc 2', '')
        mod._GenerateFullSectorCodes()
        mar.AddSupplier(hh, 'SUP_LAB/2')
        mar.AddSupplier(hh2)
        # mar.SupplyAllocation = [[(hh, 'SUP_LAB/2')], hh2]
        mar._GenerateEquations()
        self.assertEqual('SUP_LAB/2', mar.EquationBlock['SUP_CA_HH'].RHS())
        self.assertEqual('SUP_LAB-SUP_CA_HH', kill_spaces(mar.EquationBlock['SUP_US_HH2'].RHS()))
        self.assertEqual('CA_LAB__SUP_CA_HH', hh.EquationBlock['SUP_LAB'].RHS())
        self.assertIn('SUP_LAB', hh.EquationBlock['F'].RHS())
        self.assertEqual('CA_LAB__SUP_US_HH2', hh2.EquationBlock['SUP_CA_LAB'].RHS())
        self.assertIn('SUP_CA_LAB', hh2.EquationBlock['F'].RHS())

    def test_GenerateEquations_2_supply_multicountry_2(self):
        mod = Model()
        can = Country(mod, 'CA', 'Canada, Eh?')
        US = Country(mod, 'US', 'USA! USA!')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        hh = Sector(can, 'HH', 'Household')
        hh2 = Sector(can, 'HH2', 'Household')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB', 'desc 2', '')
        hh2.AddVariable('SUP_LAB', 'desc 2', '')
        mod._GenerateFullSectorCodes()
        mar.AddSupplier(hh2)
        mar.AddSupplier(hh, 'SUP_LAB/2')
        #nmar.SupplyAllocation = [[(hh, 'SUP_LAB/2')], hh2]
        mar._GenerateEquations()
        self.assertEqual('SUP_LAB/2', mar.EquationBlock['SUP_CA_HH'].RHS())
        self.assertEqual('SUP_LAB-SUP_CA_HH', mar.EquationBlock['SUP_CA_HH2'].RHS())
        self.assertEqual('CA_LAB__SUP_CA_HH', hh.EquationBlock['SUP_LAB'].RHS())
        self.assertIn('SUP_LAB', hh.EquationBlock['F'].RHS())
        self.assertEqual('CA_LAB__SUP_CA_HH2', hh2.EquationBlock['SUP_LAB'].RHS())
        self.assertIn('SUP_LAB', hh2.EquationBlock['F'].RHS())

    def test_GenerateEquations_2_supply_multicountry_3(self):
        mod = Model()
        # Need to stay in the same currency zone
        can = Country(mod, 'CA', 'Canada, Eh?', currency='LOC')
        US = Country(mod, 'US', 'USA! USA!', currency='LOC')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        hh = Sector(can, 'HH', 'Household')
        # Somehow, Americans are supplying labour in Canada...
        hh2 = Sector(US, 'HH2', 'Household')
        hh3 = Sector(US, 'HH3', 'Household#3')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB', 'desc 2', '')
        hh2.AddVariable('SUP_CA_LAB', 'desc 2', '')
        hh3.AddVariable('SUP_CA_LAB', 'desc 2', '')
        mod._GenerateFullSectorCodes()
        #mar.SupplyAllocation = [[(hh, 'SUP_LAB/2'), (hh3, '0.')], hh2]
        mar.AddSupplier(hh2)
        mar.AddSupplier(hh, 'SUP_LAB/2')
        mar.AddSupplier(hh3, '0.')
        mar._GenerateEquations()
        self.assertEqual('SUP_LAB/2', mar.EquationBlock['SUP_CA_HH'].RHS())
        self.assertEqual('SUP_LAB-SUP_CA_HH-SUP_US_HH3', kill_spaces(mar.EquationBlock['SUP_US_HH2'].RHS()))
        self.assertEqual('CA_LAB__SUP_CA_HH', hh.EquationBlock['SUP_LAB'].RHS())
        self.assertIn('SUP_LAB', hh.EquationBlock['F'].RHS())
        self.assertEqual('CA_LAB__SUP_US_HH2', hh2.EquationBlock['SUP_CA_LAB'].RHS())
        self.assertIn('SUP_CA_LAB', hh2.EquationBlock['F'].RHS())
        self.assertIn('SUP_CA_LAB', hh3.EquationBlock['F'].RHS())

    def test_GenerateTermsLowLevel(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        mar = Market(can, 'LAB', 'Market')
        bus = Sector(can, 'BUS', 'Business')
        bus.AddVariable('DEM_LAB', 'desc', '')
        mod._GenerateFullSectorCodes()
        mar._GenerateTermsLowLevel('DEM', 'Demand')
        self.assertIn('-DEM_LAB', bus.EquationBlock['F'].RHS())
        self.assertEqual('0.0', bus.EquationBlock['DEM_LAB'].RHS())

    def test_GenerateTermsLowLevel_3(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        mar = Market(can, 'LAB', 'Market')
        with self.assertRaises(LogicError):
            mar._GenerateTermsLowLevel('Blam!', 'desc')
