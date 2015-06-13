import urllib2
import StringIO
import sqlite3
import os

# Remove database if it exists
if os.path.exists("gene.db"):
    os.remove("gene.db")

conn = sqlite3.connect('gene.db')

URL = "ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/tsv/hgnc_complete_set.txt"

# Download hgnc database and split
response = urllib2.urlopen(URL)
lines = [x.split("\t") for x in response.read().splitlines()][1:]

conn.text_factory = str

c = conn.cursor()

# Create table
c.execute('''CREATE VIRTUAL TABLE idset USING
             fts3(hgnc_id,
              symbol,
              name,
              locus_group,
              locus_type,
              status,
              location,
              location_sortable,
              alias_symbol,
              alias_name,
              prev_symbol,
              prev_name,
              gene_family,
              gene_family_id,
              date_approved_reserved,
              date_symbol_changed,
              date_name_changed,
              date_modified,
              entrez_id,
              ensembl_gene_id,
              vega_id,
              ucsc_id,
              ena,
              refseq_accession,
              ccds_id,
              uniprot_ids,
              pubmed_id,
              mgd_id,
              rgd_id,
              lsdb,
              cosmic,
              omim_id,
              mirbase,
              homeodb,
              snornabase,
              bioparadigms_slc,
              orphanet,
              pseudogene_org,
              horde_id,
              merops,
              imgt,
              iuphar,
              kznf_gene_catalog,
              mamit_trnadb,
              cd,
              lncrnadb,
              enzyme_id,
              intermediate_filament_db)''')

# Insert genes
c.executemany('INSERT INTO idset VALUES ({questions})'.format(questions = ",".join(["?"]*48)), lines)
conn.commit()
c.close()