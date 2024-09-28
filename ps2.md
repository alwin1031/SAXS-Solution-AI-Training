
# **PDB to MRC Batch Converter: User Guide**

### **Table of Contents**
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Preparing Your Data](#preparing-your-data)
5. [Using the Script](#using-the-script)
    - [Script Overview](#script-overview)
    - [Running the Script](#running-the-script)
    - [Command-Line Arguments](#command-line-arguments)
6. [Output Management](#output-management)
7. [Visualization of MRC Files](#visualization-of-mrc-files)
8. [Troubleshooting](#troubleshooting)
9. [Customization](#customization)
10. [Additional Resources](#additional-resources)



### **Introduction**

The **PDB to MRC Batch Converter** is a Python-based tool designed to automate the conversion of multiple Protein Data Bank (PDB) files into Macromolecular Crystallographic (MRC) format files. This conversion is particularly useful for generating electron density maps from molecular structures, facilitating further analysis and visualization in various molecular modeling and crystallography applications.



### **Prerequisites**

Before using the script, ensure that your system meets the following requirements:

- **Operating System:** Windows, macOS, or Linux
- **Python:** Version 3.6 or higher
- **Python Libraries:**
  - `Biopython`
  - `NumPy`
  - `mrcfile`



### **Installation**

1. **Install Python:**

   - If you haven't installed Python yet, download it from the [official website](https://www.python.org/downloads/) and follow the installation instructions for your operating system.

2. **Install Required Python Libraries:**

   Open your terminal or command prompt and execute the following command to install the necessary libraries:

   ```bash
   pip install biopython numpy mrcfile
   ```

   > **Note:** If you encounter permission issues, you might need to use `pip3` instead of `pip`, or add the `--user` flag:

   ```bash
   pip3 install --user biopython numpy mrcfile
   ```

3. **Download the Script:**

   Save the provided Python script (from our previous conversation) as `pdb_to_mrc_batch.py` in a directory of your choice.



### **Preparing Your Data**

1. **Organize PDB Files:**

   - Create a dedicated folder (e.g., `pdb_files`) and place all your `.pdb` files within this folder. Ensure that all files you intend to convert have the `.pdb` extension and are correctly formatted.

2. **Determine Output Directory:**

   - Decide where you want the converted `.mrc` files to be saved. By default, the script creates an `output_mrc` folder in the same directory as the script. You can specify a different output folder if desired.



### **Using the Script**

#### **Script Overview**

The `pdb_to_mrc_batch.py` script automates the conversion process by:

- Parsing each PDB file to extract atomic coordinates and element types.
- Generating an electron density map using Gaussian distributions for each atom.
- Saving the resulting density map in MRC file format.
- Handling multiple files in a specified input folder with error reporting.

#### **Running the Script**

1. **Open Terminal or Command Prompt:**

   - Navigate to the directory containing the `pdb_to_mrc_batch.py` script.

2. **Execute the Script:**

   Use the following command structure to run the script:

   ```bash
   python pdb_to_mrc_batch.py <input_folder> [output_folder]
   ```

   - Replace `<input_folder>` with the path to your folder containing PDB files.
   - `[output_folder]` is optional. If not specified, the script defaults to `output_mrc`.

   **Examples:**

   - **Using Default Output Folder:**

     ```bash
     python pdb_to_mrc_batch.py pdb_files
     ```

     - **Input Folder:** `pdb_files`
     - **Output Folder:** `output_mrc`

   - **Specifying a Custom Output Folder:**

     ```bash
     python pdb_to_mrc_batch.py pdb_files mrc_output
     ```

     - **Input Folder:** `pdb_files`
     - **Output Folder:** `mrc_output`

#### **Command-Line Arguments**

- **Positional Arguments:**

  1. `<input_folder>`: **(Required)** Path to the folder containing `.pdb` files to be converted.
  2. `[output_folder]`: **(Optional)** Path to the folder where `.mrc` files will be saved. Defaults to `output_mrc` if not provided.



### **Output Management**

- **Output Folder Creation:**

  - If the specified output folder does not exist, the script automatically creates it.
  
- **Naming Convention:**

  - Each output MRC file retains the base name of its corresponding PDB file, changing only the extension from `.pdb` to `.mrc`.
  
    - **Example:**
      - `protein1.pdb` → `protein1.mrc`

- **File Location:**

  - All converted `.mrc` files are saved in the specified output folder.



### **Visualization of MRC Files**

After conversion, you can visualize the generated MRC files using various molecular visualization tools:

1. **UCSF Chimera or ChimeraX:**

   - **Usage:**
     - Open both the original PDB file and the corresponding MRC file.
     - Overlay the electron density map onto the molecular structure for comprehensive analysis.

2. **PyMOL:**

   - **Usage:**
     - Use plugins or built-in functions to load and visualize MRC files alongside PDB structures.

3. **Other Tools:**

   - Tools like **VMD**, **Coot**, and **Jmol** may also support MRC file visualization with appropriate plugins or configurations.



### **Troubleshooting**

If the script doesn't process all PDB files as expected, consider the following steps:

1. **Verify PDB File Integrity:**

   - Ensure that all PDB files are correctly formatted and free from corruption.
   - Open suspicious files in a text editor or visualization tool to check for anomalies.

2. **Check for Hidden or Non-PDB Files:**

   - The script filters files based on the `.pdb` extension (case-insensitive). Ensure that the input folder contains only valid `.pdb` files.

3. **Review Error Messages:**

   - The script includes error handling that reports issues with specific files without halting the entire process.
   - Common errors include parsing issues, memory constraints, or unrecognized elements.

   **Example Error Message:**

   ```
   Error processing protein2.pdb: Unable to allocate array with shape (1000, 1000, 1000) and data type float32
   ```

4. **Adjust Grid Spacing for Large Molecules:**

   - Large molecules with high-resolution grids may cause memory errors.
   - Increase the `grid_spacing` parameter in the script to reduce the grid size and memory usage.

   ```python
   grid_spacing = 2.0  # Example: Increased from 1.0 to 2.0 Angstroms
   ```

5. **Add Missing Elements:**

   - If your PDB files contain elements not listed in the `element_sigma` dictionary, the script uses a default sigma value.
   - To improve accuracy, add the missing elements with appropriate sigma values.

   ```python
   element_sigma = {
       'H': 0.25,
       'C': 0.35,
       'N': 0.35,
       'O': 0.35,
       'S': 0.50,
       'P': 0.50,
       'Fe': 0.45,   # Example addition
       'Mg': 0.45,   # Example addition
       # Add more elements as needed
   }
   ```

6. **Ensure Sufficient Permissions:**

   - Confirm that you have read permissions for the input folder and write permissions for the output folder.

7. **Monitor System Resources:**

   - High memory usage can impede script execution, especially with large datasets. Monitor your system's RAM usage and close unnecessary applications if needed.



### **Customization**

Feel free to modify the script to better suit your specific needs. Here are some areas you might consider customizing:

1. **Grid Spacing and Padding:**

   - **Grid Spacing (`grid_spacing`):** Determines the resolution of the electron density map.
     - **Smaller Values:** Higher resolution, larger file size.
     - **Larger Values:** Lower resolution, smaller file size.

   - **Padding (`padding`):** Controls the space around the molecule in the density map.
     - **Increase Padding:** More space around the molecule.
     - **Decrease Padding:** Less space, potentially cutting off parts of the molecule.

   ```python
   grid_spacing = 1.0   # Adjust as needed
   padding = 5.0        # Adjust as needed
   ```

2. **Element Standard Deviations (`element_sigma`):**

   - Modify or extend the `element_sigma` dictionary to include additional elements or adjust sigma values for better accuracy.

   ```python
   element_sigma = {
       'H': 0.25,
       'C': 0.35,
       'N': 0.35,
       'O': 0.35,
       'S': 0.50,
       'P': 0.50,
       # Add more elements as needed
   }
   ```

3. **Output File Naming:**

   - Customize how output files are named if you prefer a different naming convention.

4. **Enhance Error Handling:**

   - Implement more sophisticated error logging (e.g., writing errors to a log file) for easier debugging.

5. **Parallel Processing:**

   - For large datasets, consider modifying the script to process multiple files in parallel to speed up the conversion process.



### **Additional Resources**

- **Biopython Documentation:** [https://biopython.org/wiki/Documentation](https://biopython.org/wiki/Documentation)
- **mrcfile Library Documentation:** [https://mrcfile.readthedocs.io/en/latest/](https://mrcfile.readthedocs.io/en/latest/)
- **UCSF ChimeraX:** [https://www.cgl.ucsf.edu/chimerax/](https://www.cgl.ucsf.edu/chimerax/)
- **PyMOL:** [https://pymol.org/2/](https://pymol.org/2/)



### **Final Remarks**

The **PDB to MRC Batch Converter** is a powerful tool to streamline the process of generating electron density maps from molecular structures. By following this guide, you should be able to efficiently convert your PDB files to MRC format, enabling enhanced visualization and analysis in your research or projects.

If you encounter any issues not covered in this guide or have suggestions for further improvements, feel free to reach out or consult the additional resources provided.

Happy converting!
