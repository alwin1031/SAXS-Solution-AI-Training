# SAXS-Solution-AI-Training

This guide explains how to use the provided Python script to:

1. **Randomly select ten protein sequences** of length between 250 and 300 amino acids from the UniProt database.
2. **Save each selected sequence in a separate FASTA file** with a `.fasta` extension.
3. **Download the corresponding AlphaFold predicted PDB models** (if available) and save them with a `.pdb` extension.

By the end of this guide, you'll have a set of FASTA files and PDB files for your selected protein sequences.


## Prerequisites

Before running the script, ensure you have the following:

- **Python 3.x** installed on your system.
- **Biopython** library installed. If not, install it using:

  ```bash
  pip install biopython
  ```

## Script Overview

The script performs the following steps:

1. **Queries the UniProt database** to find protein sequences that meet the specified criteria (length between 250 and 300 amino acids and reviewed entries).
2. **Randomly selects ten sequences** from the retrieved list.
3. **Creates directories** to store the output files (`fasta_files` and `pdb_files`).
4. **Saves each sequence** in a separate FASTA file within the `fasta_files` directory.
5. **Attempts to download the AlphaFold predicted PDB model** for each selected sequence and saves it in the `pdb_files` directory.


## Instructions

### 1. Run the Script

Open a terminal or command prompt, navigate to the directory containing the script, and run:

```bash
python download_proteins_and_pdbs.py
```

### 2. Understand the Output

As the script runs, it will display messages indicating its progress:

- **Saved FASTA file:** Indicates that a protein sequence has been saved.
- **Downloaded PDB file:** Indicates that the corresponding AlphaFold PDB model has been downloaded.
- **AlphaFold PDB file not available:** Indicates that a PDB model was not found for the sequence.

Example output:

```
Saved FASTA file: fasta_files/P12345.fasta
Downloaded PDB file: pdb_files/P12345.pdb
Saved FASTA file: fasta_files/Q67890.fasta
AlphaFold PDB file not available for Q67890.
...
```

### 3. Check the Output Files

After execution, the script creates two directories:

- **`fasta_files`**: Contains individual `.fasta` files for each selected protein sequence.
- **`pdb_files`**: Contains `.pdb` files for sequences with available AlphaFold models.



## Customization and Advanced Usage

### Modifying the Search Criteria

You can adjust the `query` variable in the script to change the search parameters. For example:

- **Filter by organism** (e.g., human):

  ```python
  query = 'length:[250 TO 300] AND reviewed:true AND organism:"Homo sapiens (Human) [9606]"'
  ```

- **Exclude certain proteins**:

  ```python
  query = 'length:[250 TO 300] AND reviewed:true NOT keyword:"Membrane [KW-0472]"'
  ```

Refer to the [UniProt Query Syntax](https://www.uniprot.org/help/text-search) for more options.


### Increasing the Number of Sequences

To select more than ten sequences, modify:

- **Sample size**:

  ```python
  selected_sequences = random.sample(sequences, desired_number)
  ```

- **Ensure sufficient sequences are fetched** by increasing the `size` parameter (maximum 500 per request):

  ```python
  params = {
      'query': query,
      'format': 'fasta',
      'size': 500  # Adjust if necessary
  }
  ```

## Troubleshooting

### Common Issues and Solutions

- **`Not enough sequences found.`**

  - **Solution:** Adjust your query to be less restrictive or ensure the `size` parameter is sufficient to fetch enough sequences.

- **`Error fetching data from UniProt.`**

  - **Solution:** Check your internet connection. If the problem persists, verify the UniProt API endpoint and parameters.

- **ModuleNotFoundError: No module named 'Bio'**

  - **Solution:** Install Biopython:

    ```bash
    pip install biopython
    ```

- **Permission Denied Errors**

  - **Solution:** Ensure you have write permissions in the directory where the script is executed.



## Additional Notes

- **AlphaFold Model Availability**

  Not all proteins have an available AlphaFold predicted structure. The script checks for the presence of the PDB file and notifies you if it's unavailable.

- **Random Selection**

  The sequences are randomly selected each time the script runs. To reproduce the same selection, you can set a random seed at the beginning of the script:

  ```python
  random.seed(42)  # Replace 42 with any integer
  ```

- **File Naming Convention**

  Files are named using the UniProt accession number (e.g., `P12345.fasta`), ensuring uniqueness and easy cross-reference between FASTA and PDB files.



## Conclusion

By following this guide, you can:

- Efficiently download protein sequences of interest.
- Obtain corresponding AlphaFold predicted structures.
- Customize the script to suit specific research needs.

This tool can be invaluable for bioinformatics analyses, structural biology studies, and educational purposes.



## Contact and Support

If you encounter issues not addressed in this guide or have suggestions for improvements, feel free to reach out to the bioinformatics community or consult the documentation for the libraries and databases used.

- **UniProt Help:** [https://www.uniprot.org/help/](https://www.uniprot.org/help/)
- **AlphaFold Database:** [https://alphafold.ebi.ac.uk/](https://alphafold.ebi.ac.uk/)
- **Biopython Documentation:** [https://biopython.org/wiki/Documentation](https://biopython.org/wiki/Documentation)

Happy coding and exploring protein structures!
