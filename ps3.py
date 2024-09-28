import numpy as np
import mrcfile

def compute_saxs_profile(mrc_filename, dat_filename, out_filename):
    """
    Computes the SAXS profile from an MRC electron density map and writes
    the output to .dat and .out files.

    Parameters:
    mrc_filename (str): Path to the input MRC file.
    dat_filename (str): Path to the output .dat file.
    out_filename (str): Path to the output .out file.
    """

    # Read the electron density map from the MRC file
    with mrcfile.open(mrc_filename, permissive=True) as mrc:
        density = mrc.data.astype(np.float32)
        voxel_size = mrc.voxel_size.x  # Assuming isotropic voxels
        nx, ny, nz = density.shape

    # Compute the 3D Fourier transform of the electron density
    Fq = np.fft.fftn(density)
    Fq = np.fft.fftshift(Fq)  # Shift zero frequency to the center

    # Compute the scattering intensity I(q) = |F(q)|^2
    Iq_3d = np.abs(Fq) ** 2

    # Create the q-grid
    kx = np.fft.fftfreq(nx, d=voxel_size)
    ky = np.fft.fftfreq(ny, d=voxel_size)
    kz = np.fft.fftfreq(nz, d=voxel_size)
    kx = np.fft.fftshift(kx)
    ky = np.fft.fftshift(ky)
    kz = np.fft.fftshift(kz)

    # Convert frequencies to q-values (Å⁻¹)
    qx = 2 * np.pi * kx
    qy = 2 * np.pi * ky
    qz = 2 * np.pi * kz

    # Generate the q-grid
    qx_grid, qy_grid, qz_grid = np.meshgrid(qx, qy, qz, indexing='ij')
    q_grid = np.sqrt(qx_grid ** 2 + qy_grid ** 2 + qz_grid ** 2)

    # Flatten the arrays for binning
    q_flat = q_grid.flatten()
    Iq_flat = Iq_3d.flatten()

    # Define q-bins
    num_bins = 1000
    q_bins = np.linspace(q_flat.min(), q_flat.max(), num_bins + 1)

    # Bin the intensities using numpy histogram
    Iq_sum, _ = np.histogram(q_flat, bins=q_bins, weights=Iq_flat)
    counts, _ = np.histogram(q_flat, bins=q_bins)
    q_bin_centers = 0.5 * (q_bins[:-1] + q_bins[1:])

    # Compute the average intensity in each bin
    with np.errstate(divide='ignore', invalid='ignore'):
        Iq_avg = np.true_divide(Iq_sum, counts)
        Iq_avg[~np.isfinite(Iq_avg)] = 0  # Replace NaN and inf with zero

    # Write the binned data to the .dat file
    with open(dat_filename, 'w') as dat_file:
        for q_value, intensity in zip(q_bin_centers, Iq_avg):
            if intensity > 0:
                dat_file.write(f"{q_value:.6e} {intensity:.6e}\n")

    # Write summary information to the .out file
    with open(out_filename, 'w') as out_file:
        out_file.write(f"Computed SAXS profile from {mrc_filename}\n")
        out_file.write(f"Voxel size: {voxel_size} Å\n")
        out_file.write(f"Density map dimensions: {nx} x {ny} x {nz}\n")
        out_file.write(f"Number of q-bins: {num_bins}\n")
        out_file.write(f"q-range: {q_flat.min():.6e} to {q_flat.max():.6e} Å⁻¹\n")

if __name__ == "__main__":
    # Replace these filenames with your actual file paths
    mrc_filename = 'input.mrc'
    dat_filename = 'output.dat'
    out_filename = 'output.out'
    compute_saxs_profile(mrc_filename, dat_filename, out_filename)
