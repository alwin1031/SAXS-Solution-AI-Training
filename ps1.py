import requests
from Bio import SeqIO
from io import StringIO
import random
import os

# Define the UniProt search query
query = 'length:[250 TO 300] AND reviewed:true'  # 'reviewed:true' filters for Swiss-Prot entries

# UniProt API endpoint
url = 'https://rest.uniprot.org/uniprotkb/search'

# Set up the parameters
params = {
    'query': query,
    'format': 'fasta',
    'size': 500  # Maximum number of results per request
}

# Send the request to UniProt API
response = requests.get(url, params=params)

if response.ok:
    fasta_data = response.text
    # Parse the FASTA data
    sequences = list(SeqIO.parse(StringIO(fasta_data), 'fasta'))

    if len(sequences) < 10:
        print("Not enough sequences found.")
    else:
        # Randomly select ten sequences
        selected_sequences = random.sample(sequences, 10)

        # Create directories for fasta and pdb files
        os.makedirs('fasta_files', exist_ok=True)
        os.makedirs('pdb_files', exist_ok=True)

        for seq_record in selected_sequences:
            # Get the UniProt accession from the sequence ID
            # The sequence ID looks like: sp|P12345|PROT_HUMAN
            # We can split it to get the accession number
            uniprot_id = seq_record.id.split('|')[1]

            # Save each sequence to a separate fasta file
            fasta_filename = f'fasta_files/{uniprot_id}.fasta'
            with open(fasta_filename, 'w') as fasta_handle:
                SeqIO.write(seq_record, fasta_handle, 'fasta')

            print(f"Saved FASTA file: {fasta_filename}")

            # Attempt to download the AlphaFold PDB file
            pdb_url = f'https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb'

            pdb_response = requests.get(pdb_url)

            if pdb_response.ok:
                pdb_filename = f'pdb_files/{uniprot_id}.pdb'
                with open(pdb_filename, 'w') as pdb_handle:
                    pdb_handle.write(pdb_response.text)
                print(f"Downloaded PDB file: {pdb_filename}")
            else:
                print(f"AlphaFold PDB file not available for {uniprot_id}.")

else:
    print("Error fetching data from UniProt.")
    print("Status code:", response.status_code)
    print("Response:", response.text)
