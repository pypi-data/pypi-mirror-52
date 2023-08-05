import autolens as al
import numpy as np
import pytest

from test.unit.mock.data.mock_grids import MockPixelizationGrid


@pytest.fixture(name="three_pixels")
def make_three_pixels():
    return np.array([[0, 0], [0, 1], [1, 0]])


@pytest.fixture(name="five_pixels")
def make_five_pixels():
    return np.array([[0, 0], [0, 1], [1, 0], [1, 1], [1, 2]])


class TestMappingMatrix:
    def test__3_image_pixels__6_pixel_pixels__sub_grid_1x1(self, three_pixels):

        sub_mask_1d_index_to_pixelization_1d_index = np.array([0, 1, 2])
        sub_mask_1d_index_to_mask_1d_index = np.array([0, 1, 2])

        mapping_matrix = al.mapper_util.mapping_matrix_from_sub_mask_1d_index_to_pixelization_1d_index(
            sub_mask_1d_index_to_pixelization_1d_index=sub_mask_1d_index_to_pixelization_1d_index,
            pixels=6,
            total_mask_pixels=3,
            sub_mask_1d_index_to_mask_1d_index=sub_mask_1d_index_to_mask_1d_index,
            sub_grid_fraction=1.0,
        )

        assert (
            mapping_matrix
            == np.array(
                [
                    [1, 0, 0, 0, 0, 0],  # CCD pixel 0 maps to pix pixel 0.
                    [0, 1, 0, 0, 0, 0],  # CCD pixel 1 maps to pix pixel 1.
                    [0, 0, 1, 0, 0, 0],
                ]
            )
        ).all()  # CCD pixel 2 maps to pix pixel 2

    def test__5_image_pixels__8_pixel_pixels__sub_grid_1x1(self, five_pixels):

        sub_mask_1d_index_to_pixelization_1d_index = np.array([0, 1, 2, 7, 6])
        sub_mask_1d_index_to_mask_1d_index = np.array([0, 1, 2, 3, 4])

        mapping_matrix = al.mapper_util.mapping_matrix_from_sub_mask_1d_index_to_pixelization_1d_index(
            sub_mask_1d_index_to_pixelization_1d_index=sub_mask_1d_index_to_pixelization_1d_index,
            pixels=8,
            total_mask_pixels=5,
            sub_mask_1d_index_to_mask_1d_index=sub_mask_1d_index_to_mask_1d_index,
            sub_grid_fraction=1.0,
        )

        assert (
            mapping_matrix
            == np.array(
                [
                    [
                        1,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                    ],  # CCD image_to_pixel 0 and 3 mappers to pix pixel 0.
                    [
                        0,
                        1,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                    ],  # CCD image_to_pixel 1 and 4 mappers to pix pixel 1.
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                ]
            )
        ).all()  # CCD image_to_pixel 2 and 5 mappers to pix pixel 2

    def test__5_image_pixels__8_pixel_pixels__sub_grid_2x2__no_overlapping_pixels(
        self, five_pixels
    ):

        sub_mask_1d_index_to_pixelization_1d_index = np.array(
            [0, 1, 2, 3, 1, 2, 3, 4, 2, 3, 4, 5, 7, 0, 1, 3, 6, 7, 4, 2]
        )
        sub_mask_1d_index_to_mask_1d_index = np.array(
            [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
        )
        mapping_matrix = al.mapper_util.mapping_matrix_from_sub_mask_1d_index_to_pixelization_1d_index(
            sub_mask_1d_index_to_pixelization_1d_index=sub_mask_1d_index_to_pixelization_1d_index,
            pixels=8,
            total_mask_pixels=5,
            sub_mask_1d_index_to_mask_1d_index=sub_mask_1d_index_to_mask_1d_index,
            sub_grid_fraction=0.25,
        )

        assert (
            mapping_matrix
            == np.array(
                [
                    [0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0],
                    [0, 0.25, 0.25, 0.25, 0.25, 0, 0, 0],
                    [0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0],
                    [0.25, 0.25, 0, 0.25, 0, 0, 0, 0.25],
                    [0, 0, 0.25, 0, 0.25, 0, 0.25, 0.25],
                ]
            )
        ).all()

    def test__5_image_pixels__8_pixel_pixels__sub_grid_2x2__include_overlapping_pixels(
        self, five_pixels
    ):

        sub_mask_1d_index_to_pixelization_1d_index = np.array(
            [0, 0, 0, 1, 1, 1, 0, 0, 2, 3, 4, 5, 7, 0, 1, 3, 6, 7, 4, 2]
        )
        sub_mask_1d_index_to_mask_1d_index = np.array(
            [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
        )

        mapping_matrix = al.mapper_util.mapping_matrix_from_sub_mask_1d_index_to_pixelization_1d_index(
            sub_mask_1d_index_to_pixelization_1d_index=sub_mask_1d_index_to_pixelization_1d_index,
            pixels=8,
            total_mask_pixels=5,
            sub_mask_1d_index_to_mask_1d_index=sub_mask_1d_index_to_mask_1d_index,
            sub_grid_fraction=0.25,
        )

        assert (
            mapping_matrix
            == np.array(
                [
                    [0.75, 0.25, 0, 0, 0, 0, 0, 0],
                    [0.5, 0.5, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0.25, 0.25, 0.25, 0.25, 0, 0],
                    [0.25, 0.25, 0, 0.25, 0, 0, 0, 0.25],
                    [0, 0, 0.25, 0, 0.25, 0, 0.25, 0.25],
                ]
            )
        ).all()

    def test__3_image_pixels__6_pixel_pixels__sub_grid_4x4(self, three_pixels):

        sub_mask_1d_index_to_pixelization_1d_index = np.array(
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                0,
                1,
                2,
                3,
                4,
                5,
                0,
                1,
                2,
                3,
                4,
                5,
                0,
                1,
                2,
                3,
            ]
        )

        sub_mask_1d_index_to_mask_1d_index = np.array(
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
            ]
        )

        mapping_matrix = al.mapper_util.mapping_matrix_from_sub_mask_1d_index_to_pixelization_1d_index(
            sub_mask_1d_index_to_pixelization_1d_index=sub_mask_1d_index_to_pixelization_1d_index,
            pixels=6,
            total_mask_pixels=3,
            sub_mask_1d_index_to_mask_1d_index=sub_mask_1d_index_to_mask_1d_index,
            sub_grid_fraction=1.0 / 16.0,
        )

        assert (
            mapping_matrix
            == np.array(
                [
                    [0.75, 0.25, 0, 0, 0, 0],
                    [0, 0, 1.0, 0, 0, 0],
                    [0.1875, 0.1875, 0.1875, 0.1875, 0.125, 0.125],
                ]
            )
        ).all()
