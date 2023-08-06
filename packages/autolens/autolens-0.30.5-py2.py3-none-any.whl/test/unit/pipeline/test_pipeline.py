import builtins
import numpy as np
import pytest

import autofit as af
import autolens as al
from autolens import exc


class MockAnalysis(object):
    def __init__(self, number_galaxies, shape, value):
        self.number_galaxies = number_galaxies
        self.shape = shape
        self.value = value

    # noinspection PyUnusedLocal
    def galaxy_images_for_model(self, model):
        return self.number_galaxies * [np.full(self.shape, self.value)]


class MockMask(object):
    pass


class Optimizer(object):
    def __init__(self, phase_name="dummy_phase"):
        self.phase_name = phase_name
        self.phase_path = ""


class DummyPhaseImaging(af.AbstractPhase):
    def make_result(self, result, analysis):
        pass

    def __init__(self, phase_name, phase_tag="", phase_path=None):
        super().__init__(phase_name, phase_tag=phase_tag)
        self.data = None
        self.positions = None
        self.results = None
        self.phase_name = phase_name
        self.phase_tag = phase_tag
        self.phase_path = phase_path or phase_name
        self.mask = None

        self.optimizer = Optimizer(phase_name)

    def run(self, data, results, mask=None, positions=None):
        self.data = data
        self.results = results
        self.mask = mask
        self.positions = positions
        self.assert_and_save_pickle()
        return af.Result(af.ModelInstance(), 1)


class MockCCDData(object):
    pass


class MockFile(object):
    def __init__(self):
        self.text = None
        self.filename = None

    def write(self, text):
        self.text = text

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


@pytest.fixture(name="mock_files", autouse=True)
def make_mock_file(monkeypatch):
    files = []

    def mock_open(filename, flag, *args, **kwargs):
        assert flag in ("w+", "w+b", "a")
        file = MockFile()
        file.filename = filename
        files.append(file)
        return file

    monkeypatch.setattr(builtins, "open", mock_open)
    yield files


class TestMetaData(object):
    def test_files(self, mock_files):
        pipeline = al.PipelineImaging(
            "pipeline_name",
            DummyPhaseImaging(phase_name="phase_name", phase_path="phase_path"),
        )
        pipeline.run(MockCCDData(), data_name="data_name")

        assert (
            mock_files[1].text
            == "pipeline=pipeline_name\nphase=phase_name\ndata=data_name"
        )

        assert "phase_name///optimizer.pickle" in mock_files[2].filename


class TestPassMask(object):
    def test_pass_mask(self):
        mask = MockMask()
        phase_1 = DummyPhaseImaging("one")
        phase_2 = DummyPhaseImaging("two")
        pipeline = al.PipelineImaging("", phase_1, phase_2)
        pipeline.run(data=MockCCDData(), mask=mask)

        assert phase_1.mask is mask
        assert phase_2.mask is mask


class TestPassPositions(object):
    def test_pass_positions(self):
        positions = [[[1.0, 1.0], [2.0, 2.0]]]
        phase_1 = DummyPhaseImaging("one")
        phase_2 = DummyPhaseImaging("two")
        pipeline = al.PipelineImaging("", phase_1, phase_2)
        pipeline.run(data=MockCCDData(), positions=positions)

        assert phase_1.positions == positions
        assert phase_2.positions == positions


class TestPipelineImaging(object):
    def test_run_pipeline(self):
        phase_1 = DummyPhaseImaging("one")
        phase_2 = DummyPhaseImaging("two")

        pipeline = al.PipelineImaging("", phase_1, phase_2)

        pipeline.run(MockCCDData())

        assert len(phase_2.results) == 2

    def test_addition(self):
        phase_1 = DummyPhaseImaging("one")
        phase_2 = DummyPhaseImaging("two")
        phase_3 = DummyPhaseImaging("three")

        pipeline1 = al.PipelineImaging("", phase_1, phase_2)
        pipeline2 = al.PipelineImaging("", phase_3)

        assert (phase_1, phase_2, phase_3) == (pipeline1 + pipeline2).phases

    def test__hyper_mode_on__must_receive_mask(self):
        phase_1 = DummyPhaseImaging("one")
        phase_2 = DummyPhaseImaging("two")

        pipeline = al.PipelineImaging("", phase_1, phase_2, hyper_mode=False)

        pipeline.run(MockCCDData())

        pipeline = al.PipelineImaging("", phase_1, phase_2, hyper_mode=True)

        with pytest.raises(exc.PhaseException):
            pipeline.run(MockCCDData())

        pipeline.run(data=MockCCDData, mask=1.0)


class DummyPhasePositions(af.AbstractPhase):
    def make_result(self, result, analysis):
        pass

    def __init__(self, phase_name):
        super().__init__(phase_name)
        self.positions = None
        self.results = None
        self.pixel_scale = None
        self.phase_name = phase_name
        self.phase_tag = ""
        self.phase_path = phase_name
        self.optimizer = Optimizer(phase_name)

    def run(self, positions, pixel_scale, results):
        self.positions = positions
        self.pixel_scale = pixel_scale
        self.results = results
        return af.Result(af.ModelInstance(), 1)


class TestPipelinePositions(object):
    def test_run_pipeline(self):
        phase_1 = DummyPhasePositions(phase_name="one")
        phase_2 = DummyPhasePositions(phase_name="two")
        pipeline = al.PipelinePositions("", phase_1, phase_2)

        pipeline.run(None, None)

        assert len(phase_2.results) == 2

    def test_addition(self):
        phase_1 = DummyPhasePositions("one")
        phase_2 = DummyPhasePositions("two")
        phase_3 = DummyPhasePositions("three")

        pipeline1 = al.PipelinePositions("", phase_1, phase_2)
        pipeline2 = al.PipelinePositions("", phase_3)

        assert (phase_1, phase_2, phase_3) == (pipeline1 + pipeline2).phases
