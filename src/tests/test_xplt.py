from pathlib import Path
from pyfebio import xplt


def test_read_xplt(tmp_path):
    xplt.to_hdf5(Path(__file__).parent.joinpath("../../assets/elastic_hex20.xplt").as_posix(), tmp_path/"elastic_hex20.hdf5")


def test_read_xplt_from_installed_febio(hex8_febmesh, tmp_path):
    import h5py

    import pyfebio as feb

    my_model = feb.model.Model(mesh_=hex8_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    model_file = tmp_path / "current.feb"
    my_model.save(model_file)
    assert feb.model.run_model(model_file, silent=True) == 0
    xplt.to_hdf5(model_file.with_suffix(".xplt").as_posix(), tmp_path / "current.hdf5")
    with h5py.File(tmp_path / "current.hdf5") as f:
        assert str(f["/"].attrs["PLT_HDR_SOFTWARE"]).startswith("FEBio")
