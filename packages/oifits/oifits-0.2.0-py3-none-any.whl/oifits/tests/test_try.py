from oifits.read import OIParser


def test_everything_works():
    a = OIParser.read("src/oifits/tests/test.oifits")
    oidata = a.data
    wav = oidata.wavelength["WAVELENGTH_NAME"].eff_wave[0]
    assert wav == 0.0013189458986744285


def test_file_opens():
    a = OIParser.read("src/oifits/tests/test.oifits")
    assert True
