import numpy as np

from autolens import exc
from autolens.model.inversion.util import inversion_util


class Inversion(object):
    def __init__(
        self,
        noise_map_1d,
        mapper,
        regularization,
        blurred_mapping_matrix,
        regularization_matrix,
        curvature_reg_matrix,
        pixelization_values,
    ):
        """ An inversion, which given an input image and noise-map reconstructs the image using a linear inversion, \
        including a convolution that accounts for blurring.

        The inversion uses a 2D pixelization to perform the reconstruction by mapping_util each pixelization pixel to a \
        set of image pixels via a mapper. The reconstructed pixelization is smoothed via a regularization scheme to \
        prevent over-fitting noise.

        Parameters
        -----------
        image_1d : ndarray
            Flattened 1D array of the observed image the inversion is fitting.
        noise_map_1d : ndarray
            Flattened 1D array of the noise-map used by the inversion during the fit.   
        convolver : ccd.convolution.Convolver
            The convolver used to blur the mapping_util matrix with the PSF.
        mapper : inversion.mappers.Mapper
            The mapping_util between the image-pixels (via its / sub-grid) and pixelization pixels.
        regularization : inversion.regularization.Regularization
            The regularization scheme applied to smooth the pixelization used to reconstruct the image for the \
            inversion

        Attributes
        -----------
        blurred_mapping_matrix : ndarray
            The matrix representing the blurred mappings between the image's sub-grid of pixels and the pixelization \
            pixels.
        regularization_matrix : ndarray
            The matrix defining how the pixelization's pixels are regularized with one another for smoothing (H).
        curvature_matrix : ndarray
            The curvature_matrix between each pixelization pixel and all other pixelization pixels (F).
        curvature_reg_matrix : ndarray
            The curvature_matrix + regularization matrix.
        solution_vector : ndarray
            The vector containing the reconstructed fit to the hyper_galaxies.
        """

        self.noise_map_1d = noise_map_1d
        self.mapper = mapper
        self.regularization = regularization
        self.blurred_mapping_matrix = blurred_mapping_matrix
        self.regularization_matrix = regularization_matrix
        self.curvature_reg_matrix = curvature_reg_matrix
        self.pixelization_values = pixelization_values

    @classmethod
    def from_data_1d_mapper_and_regularization(
        cls, image_1d, noise_map_1d, convolver, mapper, regularization
    ):

        blurred_mapping_matrix = convolver.convolve_mapping_matrix(
            mapping_matrix=mapper.mapping_matrix
        )

        data_vector = inversion_util.data_vector_from_blurred_mapping_matrix_and_data(
            blurred_mapping_matrix=blurred_mapping_matrix,
            image_1d=image_1d,
            noise_map_1d=noise_map_1d,
        )

        curvature_matrix = inversion_util.curvature_matrix_from_blurred_mapping_matrix(
            blurred_mapping_matrix=blurred_mapping_matrix, noise_map_1d=noise_map_1d
        )

        regularization_matrix = regularization.regularization_matrix_from_mapper(
            mapper=mapper
        )

        curvature_reg_matrix = np.add(curvature_matrix, regularization_matrix)

        try:
            pixelization_values = np.linalg.solve(curvature_reg_matrix, data_vector)
        except np.linalg.LinAlgError:
            raise exc.InversionException()

        return Inversion(
            noise_map_1d=noise_map_1d,
            mapper=mapper,
            regularization=regularization,
            blurred_mapping_matrix=blurred_mapping_matrix,
            regularization_matrix=regularization_matrix,
            curvature_reg_matrix=curvature_reg_matrix,
            pixelization_values=pixelization_values,
        )

    @property
    def reconstructed_data_2d(self):
        return self.mapper.grid.scaled_array_2d_from_array_1d(
            array_1d=np.asarray(self.reconstructed_data_1d)
        )

    @property
    def reconstructed_data_1d(self):
        return inversion_util.reconstructed_data_vector_from_blurred_mapping_matrix_and_solution_vector(
            blurred_mapping_matrix=self.blurred_mapping_matrix,
            solution_vector=self.pixelization_values,
        )

    @property
    def pixelization_errors_with_covariance(self):
        return np.linalg.inv(self.curvature_reg_matrix)

    @property
    def pixelization_errors(self):
        return np.diagonal(self.pixelization_errors_with_covariance)

    @property
    def pixelization_residual_map(self):
        return inversion_util.pixelization_residual_map_from_pixelization_values_and_reconstructed_data_1d(
            pixelization_values=self.pixelization_values,
            reconstructed_data_1d=self.reconstructed_data_1d,
            sub_mask_1d_index_to_mask_1d_index=self.mapper.grid.sub_mask_1d_index_to_mask_1d_index,
            pixelization_1d_index_to_all_sub_mask_1d_indexes=self.mapper.pixelization_1d_index_to_all_sub_mask_1d_indexes,
        )

    @property
    def pixelization_normalized_residual_map(self):
        return inversion_util.pixelization_normalized_residual_map_from_pixelization_values_and_reconstructed_data_1d(
            pixelization_values=self.pixelization_values,
            reconstructed_data_1d=self.reconstructed_data_1d,
            noise_map_1d=self.noise_map_1d,
            sub_mask_1d_index_to_mask_1d_index=self.mapper.grid.sub_mask_1d_index_to_mask_1d_index,
            pixelization_1d_index_to_all_sub_mask_1d_indexes=self.mapper.pixelization_1d_index_to_all_sub_mask_1d_indexes,
        )

    @property
    def pixelization_chi_squared_map(self):
        return inversion_util.pixelization_chi_squared_map_from_pixelization_values_and_reconstructed_data_1d(
            pixelization_values=self.pixelization_values,
            reconstructed_data_1d=self.reconstructed_data_1d,
            noise_map_1d=self.noise_map_1d,
            sub_mask_1d_index_to_mask_1d_index=self.mapper.grid.sub_mask_1d_index_to_mask_1d_index,
            pixelization_1d_index_to_all_sub_mask_1d_indexes=self.mapper.pixelization_1d_index_to_all_sub_mask_1d_indexes,
        )

    @property
    def regularization_term(self):
        """ Compute the regularization term of an inversion. This term represents the sum of the difference in flux \
        between every pair of neighboring pixels. This is computed as:

        s_T * H * s = solution_vector.T * regularization_matrix * solution_vector

        The term is referred to as *G_l* in Warren & Dye 2003, Nightingale & Dye 2015.

        The above works include the regularization_matrix coefficient (lambda) in this calculation. In PyAutoLens, \
        this is already in the regularization matrix and thus implicitly included in the matrix multiplication.
        """
        return np.matmul(
            self.pixelization_values.T,
            np.matmul(self.regularization_matrix, self.pixelization_values),
        )

    @property
    def log_det_curvature_reg_matrix_term(self):
        return self.log_determinant_of_matrix_cholesky(self.curvature_reg_matrix)

    @property
    def log_det_regularization_matrix_term(self):
        return self.log_determinant_of_matrix_cholesky(self.regularization_matrix)

    @staticmethod
    def log_determinant_of_matrix_cholesky(matrix):
        """There are two terms in the inversion's Bayesian likelihood function which require the log determinant of \
        a matrix. These are (Nightingale & Dye 2015, Nightingale, Dye and Massey 2018):

        ln[det(F + H)] = ln[det(curvature_reg_matrix)]
        ln[det(H)]     = ln[det(regularization_matrix)]

        The curvature_reg_matrix is positive-definite, which means the above log determinants can be computed \
        efficiently (compared to using np.det) by using a Cholesky decomposition first and summing the log of each \
        diagonal term.

        Parameters
        -----------
        matrix : ndarray
            The positive-definite matrix the log determinant is computed for.
        """
        try:
            return 2.0 * np.sum(np.log(np.diag(np.linalg.cholesky(matrix))))
        except np.linalg.LinAlgError:
            raise exc.InversionException()
