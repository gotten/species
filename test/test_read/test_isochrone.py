import os
import shutil
import urllib.request

import pytest
import numpy as np

import species
from species.util import test_util


class TestIsochrone:

    def setup_class(self):
        self.limit = 1e-8
        self.test_path = os.path.dirname(__file__) + '/'

        filename = 'model.AMES-Cond-2000.M-0.0.NaCo.Vega'

        url = 'https://people.phys.ethz.ch/~stolkert/species/model.AMES-Cond-2000.M-0.0.NaCo.Vega'

        urllib.request.urlretrieve(url, filename)

    def teardown_class(self):
        os.remove('species_database.hdf5')
        os.remove('species_config.ini')
        os.remove('model.AMES-Cond-2000.M-0.0.NaCo.Vega')
        shutil.rmtree('data/')

    def test_species_init(self):
        test_util.create_config('./')
        species.SpeciesInit()

    def test_read_isochrone(self):
        database = species.Database()
        database.add_isochrones('model.AMES-Cond-2000.M-0.0.NaCo.Vega', 'ames-cond_isochrone')

        database.add_model('ames-cond',
                           wavel_range=(1., 5.),
                           spec_res=100.,
                           teff_range=(2000., 2500))

        read_isochrone = species.ReadIsochrone('ames-cond_isochrone')
        assert read_isochrone.tag == 'ames-cond_isochrone'

    def test_get_isochrone(self):
        read_isochrone = species.ReadIsochrone('ames-cond_isochrone')

        isochrone_box = read_isochrone.get_isochrone(100.,
                                                     np.linspace(10., 100., 10),
                                                     ('J', 'H'),
                                                     'J')

        assert isochrone_box.color.shape == (10, )
        assert isochrone_box.magnitude.shape == (10, )

        assert np.sum(isochrone_box.color) == pytest.approx(3.85706098401751,
                                                            rel=self.limit, abs=0.)

        assert np.sum(isochrone_box.magnitude) == pytest.approx(110.53956764868532,
                                                                rel=self.limit, abs=0.)

        assert np.sum(isochrone_box.teff) == pytest.approx(23007.25934497323,
                                                           rel=self.limit, abs=0.)

        assert np.sum(isochrone_box.logg) == pytest.approx(47.48793769423847,
                                                           rel=self.limit, abs=0.)

    def test_get_color_magnitude(self):
        read_isochrone = species.ReadIsochrone('ames-cond_isochrone')

        colormag_box = read_isochrone.get_color_magnitude(100.,
                                                          np.linspace(35., 45., 10),
                                                          'ames-cond',
                                                          ('MKO/NSFCam.J', 'MKO/NSFCam.H'),
                                                          'MKO/NSFCam.J')

        assert colormag_box.object_type == 'model'
        assert colormag_box.color.shape == (10, )
        assert colormag_box.magnitude.shape == (10, )

        assert np.sum(colormag_box.color) == pytest.approx(2.519677745822591,
                                                           rel=self.limit, abs=0.)

        assert np.sum(colormag_box.magnitude) == pytest.approx(109.59727599872247,
                                                               rel=self.limit, abs=0.)

        assert np.sum(colormag_box.sptype)  == pytest.approx(400., rel=self.limit, abs=0.)

    def test_get_color_color(self):
        read_isochrone = species.ReadIsochrone('ames-cond_isochrone')

        colorcolor_box = read_isochrone.get_color_color(100.,
                                                        np.linspace(35., 45., 10),
                                                        'ames-cond',
                                                        (('MKO/NSFCam.J', 'MKO/NSFCam.H'),
                                                         ('MKO/NSFCam.H', 'MKO/NSFCam.Ks')))

        assert colorcolor_box.object_type == 'model'
        assert colorcolor_box.color1.shape == (10, )
        assert colorcolor_box.color2.shape == (10, )

        assert np.sum(colorcolor_box.color1) == pytest.approx(2.519677745822591,
                                                              rel=self.limit, abs=0.)

        assert np.sum(colorcolor_box.color2) == pytest.approx(3.3467959032673775,
                                                              rel=self.limit, abs=0.)

        assert np.sum(colorcolor_box.sptype) == pytest.approx(400., rel=self.limit, abs=0.)
