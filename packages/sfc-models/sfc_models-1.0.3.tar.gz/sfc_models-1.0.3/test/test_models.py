from unittest import TestCase

from sfc_models.models import *
from sfc_models.sector import Sector
from sfc_models.sector_definitions import Household, ConsolidatedGovernment


def kill_spaces(s):
    """
    remove spaces from a string; makes testing easier as white space conventions may change in equations
    :param s:
    :return:
    """
    s = s.replace(' ', '')
    return s


class TestEntity(TestCase):
    def test_ctor(self):
        EconomicObject.ID = 0
        a = EconomicObject()
        self.assertEqual(a.ID, 0)
        b = EconomicObject(a)
        self.assertEqual(b.ID, 1)
        self.assertEqual(b.Parent.ID, 0)

    def test_root(self):
        a = EconomicObject()
        b = EconomicObject(a)
        c = EconomicObject(b)
        self.assertEqual(a, a.GetModel())
        self.assertEqual(a, b.GetModel())
        self.assertEqual(a, c.GetModel())


class Stub(object):
    """
    Use the stub_fun to count how many times a method has been called.
    Used for testing the iteration in the Model class; the output depends upon the sector,
    which are tested separately.
    """

    def __init__(self):
        self.Count = 0

    def stub_fun(self):
        self.Count += 1

    def stub_return(self):
        self.Count += 1
        return [(str(self.Count), 'a', 'b')]


class TestModel(TestCase):
    def test_GenerateFullCodes_1(self):
        mod = Model()
        country = Country(mod, 'US', 'USA!')
        household = Sector(country, 'HH', 'Household')
        mod._GenerateFullSectorCodes()
        self.assertEqual(household.FullCode, 'HH')

    def test_GenerateFullCodes_2(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        can = Country(mod, 'Eh?', 'Canada')
        household = Sector(us, 'HH', 'Household')
        can_hh = Sector(can, 'HH', 'Household')
        mod._GenerateFullSectorCodes()
        self.assertEqual(household.FullCode, 'US_HH')
        self.assertEqual(can_hh.FullCode, 'Eh?_HH')

    def test_LookupSector(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        can = Country(mod, 'Eh?', 'Canada')
        household = Sector(us, 'HH', 'Household')
        can_hh = Sector(can, 'HH', 'Household')
        mod._GenerateFullSectorCodes()
        self.assertEqual(household, mod.LookupSector('US_HH'))
        self.assertEqual(can_hh, mod.LookupSector('Eh?_HH'))
        with self.assertRaises(KeyError):
            mod.LookupSector('HH')

    def test_AddExogenous(self):
        mod = Model()
        # Does not validate that the sector exists (until we call ProcessExogenous)
        mod.AddExogenous('code', 'varname', 'val')
        self.assertEqual([('code', 'varname', 'val')], mod.Exogenous)

    def test_AddExogenous_list(self):
        mod = Model()
        # Does not validate that the sector exists (until we call ProcessExogenous)
        val = [0, 1, 2]
        mod.AddExogenous('code', 'varname', val)
        self.assertEqual([('code', 'varname', repr(val))], mod.Exogenous)

    def test_AddExogenous_tuple(self):
        mod = Model()
        val = (0, 1, 2)
        mod.AddExogenous('code', 'varname', val)
        self.assertEqual([('code', 'varname', repr(val))], mod.Exogenous)

    def test_AddInitialCondition(self):
        mod = Model()
        # Does not validate that the sector exists until processing
        mod.AddInitialCondition('code', 'varname', 0.1)
        self.assertEqual([('code', 'varname', str(0.1))], mod.InitialConditions)
        with self.assertRaises(ValueError):
            mod.AddInitialCondition('code2', 'varname2', 'kablooie!')

    def test_GenerateInitialCond(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        household = Sector(us, 'HH', 'Household')
        household.AddVariable('foo', 'desc', 'x')
        mod._GenerateFullSectorCodes()
        mod.InitialConditions = [('HH', 'foo', '0.1')]
        out = mod._GenerateInitialConditions()
        self.assertEqual([('HH__foo(0)', '0.1', 'Initial Condition')], out)

    def test_GenerateInitialCondFail(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        household = Sector(us, 'HH', 'Household')
        mod._GenerateFullSectorCodes()
        mod.InitialConditions = [('HH', 'FooFoo', '0.1')]
        with self.assertRaises(KeyError):
            out = mod._GenerateInitialConditions()

    def test_ProcessExogenous(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        household = Sector(us, 'HH', 'Household')
        household.AddVariable('foo', 'desc', 'x')
        mod._GenerateFullSectorCodes()
        mod.Exogenous = [('HH', 'foo', 'TEST')]
        mod._ProcessExogenous()
        self.assertEqual('EXOGENOUSTEST', household.EquationBlock['foo'].RHS())

    def test_GetSectors(self):
        mod = Model()
        self.assertEqual(0, len(mod.GetSectors()))
        us = Country(mod, 'US', 'USA')
        self.assertEqual(0, len(mod.GetSectors()))
        household = Sector(us, 'HH', 'Household')
        self.assertEqual(1, len(mod.GetSectors()))
        hh2 = Sector(us, 'HH2', 'Household2')
        self.assertEqual(2, len(mod.GetSectors()))
        ca = Country(mod, 'code', 'country')
        hh3 = Sector(ca, 'sec3', 'sec3')
        secs = mod.GetSectors()
        self.assertEqual(3, len(secs))
        self.assertIn(household, secs)
        self.assertIn(hh2, secs)
        self.assertIn(hh3, secs)

    def test_Fixaliases(self):
        mod = Model()
        c = Country(mod, 'co', 'co')
        sec1 = Sector(c, 'sec1', 'sec1')
        sec1.AddVariable('x', 'eqn x', '')
        varname = sec1.GetVariableName('x')
        ID = "{0}".format(sec1.ID)
        self.assertIn(ID, varname)
        sec2 = Sector(c, 'sec2', 'sec2')
        sec2.AddVariable('two_x', 'Test variable', '2 * {0}'.format(varname))
        self.assertEqual('2*' + varname, kill_spaces(sec2.EquationBlock['two_x'].RHS()))
        mod._GenerateFullSectorCodes()
        mod._FixAliases()
        self.assertEqual('2*sec1__x', kill_spaces(sec2.EquationBlock['two_x'].RHS()))

    def test_fix_aliases_2(self):
        mod = Model()
        c = Country(mod, 'co', 'co')
        sec1 = Sector(c, 'sec1', 'sec1')
        sec1.AddVariable('x', 'eqn x', '')
        varname = sec1.GetVariableName('x')
        # The ID is the key part of the alias
        self.assertIn('{0}'.format(sec1.ID), varname)
        sec2 = Sector(c, 'sec2', 'sec2')
        mod.RegisterCashFlow(sec1, sec2, 'x')
        mod._GenerateRegisteredCashFlows()
        self.assertIn('-' + varname, sec1.EquationBlock['F'].RHS())
        self.assertIn(varname, sec2.EquationBlock['F'].RHS())
        mod._GenerateFullSectorCodes()
        mod._FixAliases()
        self.assertIn('-sec1__x', sec1.EquationBlock['F'].RHS())
        self.assertEqual('LAG_F+sec1__x', kill_spaces(sec2.EquationBlock['F'].RHS()))

    def test_ForceExogenous2(self):
        mod = Model()
        us = Country(mod, 'US', 'USA')
        household = Sector(us, 'HH', 'Household')
        mod._GenerateFullSectorCodes()
        mod.Exogenous = [('HH', 'Foo', 'TEST')]
        with self.assertRaises(KeyError):
            mod._ProcessExogenous()

    def test_GenerateEquations(self):
        # Just count the number if times the stub is called
        stub = Stub()
        mod = Model()
        us = Country(mod, 'US', 'USA')
        h1 = Sector(us, 'HH', 'Household')
        h2 = Sector(us, 'CAP', 'Capitalists')
        h1._GenerateEquations = stub.stub_fun
        h2._GenerateEquations = stub.stub_fun
        mod._GenerateEquations()
        self.assertEqual(2, stub.Count)

    def test_CreateFinalFunctions(self):
        stub = Stub()
        mod = Model()
        us = Country(mod, 'US', 'USA')
        h1 = Sector(us, 'HH', 'Household')
        h2 = Sector(us, 'H2', 'Household2')
        h1._CreateFinalEquations = stub.stub_return
        h2._CreateFinalEquations = stub.stub_return
        out = mod._CreateFinalEquations()
        out = out.split('\n')
        self.assertTrue('1' in out[0])
        self.assertTrue('2' in out[1])

    def test_CreateEquationEmpty(self):
        mod = Model()
        with self.assertRaises(Warning):
            mod._CreateFinalEquations()

    def test_Main_empty_state(self):
        mod = Model()
        self.assertEqual('Construction', mod.State)
        mod.main()
        self.assertEqual('Finished Running', mod.State)

    def test_FinalEquationFormating(self):
        eq = [('x', 'y + 1', 'comment_x'),
              ('y', 'EXOGENOUS 20', 'comment_y'),
              ('z', 'd', 'comment_z')]
        mod = Model()
        out = mod._FinalEquationFormatting(eq)
        # Remove spaces; what matters is the content
        out = out.replace(' ', '').split('\n')
        target = ['x=y+1#comment_x', 'z=d#comment_z', '', '#ExogenousVariables', '', 'y=20#comment_y',
                  '', 'MaxTime=100', 'Err_Tolerance=1e-6']
        self.assertEqual(target, out)

    def test_dumpequations(self):
        # Since dump format will change, keep this as a very loose test. We can tighten the testing
        # on Sector.Dump() later
        mod = Model()
        country = Country(mod, 'US', 'USA! USA!')
        household = Sector(country, 'HH', 'Household')
        hh_dump = household.Dump()
        mod_dump = mod.DumpEquations()
        self.assertEqual(hh_dump, mod_dump)

    def test_GetTimeSeries(self):
        mod = Model()
        mod.TimeSeriesCutoff = None
        mod.EquationSolver.TimeSeries = {'t': [0, 1, 2]}
        with self.assertRaises(KeyError):
            mod.GetTimeSeries('q')
        with self.assertRaises(KeyError):
            mod.GetTimeSeries('q', cutoff=1)
        self.assertEqual([0, 1, 2], mod.GetTimeSeries('t'))
        self.assertEqual([0, 1], mod.GetTimeSeries('t', cutoff=1))
        mod.TimeSeriesCutoff = 1
        self.assertEqual([0, 1], mod.GetTimeSeries('t'))
        # Passed parameter overrides default .GetTimeSeries member.
        self.assertEqual([0, ], mod.GetTimeSeries('t', cutoff=0))

    def test_GetTimeSeriesPop(self):
        mod = Model()
        mod.EquationSolver.TimeSeries = {'t': [0, 1, 2]}
        mod.TimeSeriesSupressTimeZero = True
        self.assertEqual([1, 2], mod.GetTimeSeries('t'))

    def test_GetItem(self):
        mod = Model()
        ca = Country(mod, 'CA', 'CA')
        self.assertIn(ca, mod)

    def test_CashFlowCrossCurrencyFail(self):
        mod = Model()
        ca = Country(mod, 'CA', 'Canada')
        us = Country(mod, 'US', 'U.S.')
        sec_ca = Sector(ca, 'HH', 'household')
        sec_ca.AddVariable('GIFT', 'Gifts', '5.')
        sec_us = Sector(us, 'HH', 'hh')
        # We can register this; we might add an ExternalSector later.
        mod.RegisterCashFlow(sec_ca, sec_us, 'GIFT')
        with self.assertRaises(LogicError):
            mod._GenerateRegisteredCashFlows()


class TestCountry(TestCase):
    def test_AddSector(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        gov = ConsolidatedGovernment(can, 'GOV', 'Government')
        self.assertEqual(can.SectorList[0].ID, gov.ID)

    def test_LookupSector(self):
        mod = Model()
        can = Country(mod, 'Eh', 'Canada')
        gov = ConsolidatedGovernment(can, 'GOV', 'Government')
        hh = Household(can, 'HH', 'Household', .9)
        self.assertEqual(can.LookupSector('HH').ID, hh.ID)
        self.assertEqual(can.LookupSector('GOV').ID, gov.ID)
        with self.assertRaises(KeyError):
            can.LookupSector('Smurf')

    def test_LookupSectorByCode(self):
        mod = Model()
        can = Country(mod, 'CA', 'Canada')
        hh = Sector(can, 'Code', 'desc')
        self.assertEqual(hh, can.LookupSector(hh.ID))

    def test_getitem(self):
        # Hits both Model and Country GetItem
        mod = Model()
        can = Country(mod, 'CA', 'Can')
        gov = ConsolidatedGovernment(can, 'GOV', 'Gov')
        us = Country(mod, 'US', 'US')
        with self.assertRaises(KeyError):
            mod['x']
        with self.assertRaises(KeyError):
            can['x']
        self.assertEqual(gov, mod['CA']['GOV'])

    def test_contains(self):
        mod = Model()
        can = Country(mod, 'CA', 'Can')
        gov = ConsolidatedGovernment(can, 'GOV', 'Gov')
        self.assertIn(gov, can)

    def test_AddCountryFail(self):
        mod = Model()
        c1 = Country(mod, 'c', 'c')
        with self.assertRaises(LogicError):
            Country(mod, 'c', 'c')

    def test_AddSectorFail(self):
        mod = Model()
        c = Country(mod, 'C', 'C')
        Sector(c, code='S', long_name='s')
        with self.assertRaises(LogicError):
            Sector(c, code='S', long_name='try 2')

class TestRegisterCashFlows(TestCase):
    def get_objects(self):
        mod = Model()
        co = Country(mod, 'code', 'name')
        sec1 = Sector(co, 'SEC1', 'Sector1')
        sec2 = Sector(co, 'SEC2', 'Sector2')
        return mod, sec1, sec2

    # Do not validate that variable exists when registering; only needs to exist when registered cash flows
    # are processed
    # def test_fail(self):
    #     mod, sec1, sec2 = self.get_objects()
    #     with self.assertRaises( KeyError):
    #         mod.RegisterCashFlow(sec1, sec2, 'DIV')

    def test_OK(self):
        mod, sec1, sec2 = self.get_objects()
        sec1.AddVariable('DIV', 'desc', '$1')
        mod.RegisterCashFlow(sec1, sec2, 'DIV')
        mod._GenerateFullSectorCodes()
        mod._GenerateEquations()
        mod._GenerateRegisteredCashFlows()
        self.assertEqual('LAG_F+SEC1__DIV', kill_spaces(sec2.EquationBlock['F'].RHS()))
        self.assertEqual('LAG_F-SEC1__DIV', kill_spaces(sec1.EquationBlock['F'].RHS()))


class TestCurrencyZone(TestCase):
    def test_create1(self):
        mod = Model()
        self.assertEqual(0, len(mod.CurrencyZoneList))
        ca = Country(mod, 'CA', 'Name')
        self.assertEqual(1, len(mod.CurrencyZoneList))
        us = Country(mod, 'US', 'Name')
        self.assertEqual(2, len(mod.CurrencyZoneList))

    def test_create2(self):
        mod = Model()
        self.assertEqual(0, len(mod.CurrencyZoneList))
        ca = Country(mod, 'CA', 'Name', currency='RMB')
        self.assertEqual(1, len(mod.CurrencyZoneList))
        us = Country(mod, 'US', 'Name', currency='RMB')
        self.assertEqual(1, len(mod.CurrencyZoneList))
        self.assertEqual('RMB', mod.CurrencyZoneList[0].Currency)

    def test_get_sectors(self):
        mod = Model()
        ca = Country(mod, 'CA', 'Name', currency='CAD')
        ca_h = Sector(ca, 'HH', 'Sec')
        us = Country(mod, 'US', 'Name', currency='RMB')
        us_h = Sector(us, 'HH', 'name')
        china = Country(mod, 'China', 'Name', currency='RMB')
        china_h = Sector(china, 'HH', 'name')
        self.assertEqual([ca_h,], ca_h.CurrencyZone.GetSectors())
        print(china_h.ID)
        for x in us_h.CurrencyZone.GetSectors():
            print(x.ID)
        self.assertEqual([us_h, china_h], us_h.CurrencyZone.GetSectors())

    def test_lookup_sector(self):
        mod = Model()
        ca = Country(mod, 'CA', 'Name', currency='CAD')
        ca_h = Sector(ca, 'HH', 'Sec')
        us = Country(mod, 'US', 'Name', currency='CAD')
        us_h = Sector(us, 'HH', 'name')
        us_gov = Sector(us, "GOV", 'name')
        czone = ca_h.CurrencyZone
        self.assertEqual(us_gov, czone.LookupSector('GOV'))
        # No hits
        with self.assertRaises(LogicError):
            czone.LookupSector('JJ')
        # Multiple hits
        with self.assertRaises(LogicError):
            czone.LookupSector('HH')




