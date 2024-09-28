import os
import sys
from Bio.PDB import PDBParser
import numpy as np
import mrcfile

# Parameters
grid_spacing = 1.0   # Grid spacing in Angstroms
padding = 5.0        # Padding around the molecule in Angstroms

def pdb_to_mrc(pdb_filepath, mrc_filepath):
    try:
        # Parse PDB file
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure('structure', pdb_filepath)
        
        # Extract atomic coordinates and elements
        coords = []
        elements = []
        for atom in structure.get_atoms():
            coords.append(atom.get_coord())
            # Get element symbol, default to 'C' if not provided
            element = atom.element.strip() if atom.element.strip() else 'C'
            elements.append(element)
        
        if not coords:
            print(f"No atoms found in {pdb_filepath}. Skipping.")
            return
        
        coords = np.array(coords)
        
        # Compute bounding box with padding
        min_coord = coords.min(axis=0) - padding
        max_coord = coords.max(axis=0) + padding
        
        # Define grid dimensions
        grid_size = ((max_coord - min_coord) / grid_spacing).astype(int) + 1
        
        # Initialize electron density grid
        density = np.zeros(grid_size[::-1], dtype=np.float32)  # Note the reversed order for zyx
        
        # Generate grid coordinates
        x = np.linspace(min_coord[0], max_coord[0], grid_size[0])
        y = np.linspace(min_coord[1], max_coord[1], grid_size[1])
        z = np.linspace(min_coord[2], max_coord[2], grid_size[2])
        Z, Y, X = np.meshgrid(z, y, x, indexing='ij')  # Use 'ij' indexing
        
        # Define standard deviations for Gaussian functions (in Angstroms)
        element_sigma = {
            'H': 0.25,
            'C': 0.35,
            'N': 0.35,
            'O': 0.35,
            'S': 0.50,
            'P': 0.50,
            # Add more elements if needed
        }
        
        # Generate the electron density map
        print(f"Processing {os.path.basename(pdb_filepath)}...")
        for atom_coord, element in zip(coords, elements):
            sigma = element_sigma.get(element, 0.35)  # Default sigma
            # Calculate squared distances
            dist_sq = ((X - atom_coord[0])**2 +
                       (Y - atom_coord[1])**2 +
                       (Z - atom_coord[2])**2)
            # Gaussian distribution
            atom_density = np.exp(-dist_sq / (2 * sigma**2))
            density += atom_density
        
        # Save the density grid to MRC file
        with mrcfile.new(mrc_filepath, overwrite=True) as mrc:
            mrc.set_data(density)
            mrc.voxel_size = (grid_spacing, grid_spacing, grid_spacing)
            mrc.header.origin = min_coord.astype(np.float32)
            mrc.update_header_from_data()
        
        print(f"Saved electron density map to {mrc_filepath}")
    except Exception as e:
        print(f"Error processing {pdb_filepath}: {e}")

def main():
    # Check if the folder path is provided
    if len(sys.argv) < 2:
        print("Usage: python pdb_to_mrc_batch.py <input_folder> [output_folder]")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    
    # Optional output folder
    if len(sys.argv) >= 3:
        output_folder = sys.argv[2]
    else:
        output_folder = 'output_mrc'
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get list of files in the input folder
    files_in_folder = os.listdir(input_folder)
    
    # Filter for files ending with .pdb (case-insensitive)
    pdb_files = [f for f in files_in_folder if f.lower().endswith('.pdb')]
    
    if not pdb_files:
        print(f"No PDB files found in {input_folder}")
        return
    
    for pdb_file in pdb_files:
        pdb_filepath = os.path.join(input_folder, pdb_file)
        base_name = os.path.splitext(pdb_file)[0]
        mrc_filename = base_name + '.mrc'
        mrc_filepath = os.path.join(output_folder, mrc_filename)
        
        # Process each file with error handling
        pdb_to_mrc(pdb_filepath, mrc_filepath)
    
    print("All files have been processed.")

if __name__ == '__main__':
    main()
