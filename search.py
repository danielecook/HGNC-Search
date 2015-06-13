#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow, ICON_WEB, web
import sqlite3
import urllib2

log = None

resolve_url = {"hgnc_id": "http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id={gene}",
                "entrez_id" : "http://www.ncbi.nlm.nih.gov/gene/{gene}",
                "ucsc_id": "http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position={gene}",
                "omim_id": "http://www.omim.org/entry/{gene}",
                "refseq_accession" : "http://www.ncbi.nlm.nih.gov/refseq/?term={gene}"}

def main(wf):
    args = wf.args[0]
    #wf.add_item(row[1],row[0], arg=wormbase_url, valid=True, icon="icon.png")
    conn = sqlite3.connect('gene.db')
    # Use dictionary cursor
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    q = '''SELECT * FROM idset WHERE idset MATCH "{q}*" LIMIT 50'''.format(q=args)
    c.execute(q)
    rows = c.fetchall()
    if args in [x["symbol"] for x in rows]:
        rows = [x for x in rows if x["symbol"] == args]
    if len(rows) > 1:
        for row in rows:
            wf.add_item(row["symbol"], row["name"], arg=row["symbol"], autocomplete = row["symbol"], valid=False, icon="gene_search.png")
    if len(rows) == 1:
        row = rows[0]

        wf.add_item(row["symbol"],row["name"] + " - Open HGNC Page", copytext=row["symbol"], valid=True, icon="gene.png")

        # Location
        loc = row["location"].split("-")[0]
        wf.add_item(row["location"],"Location - Open region in UCSC Genome Browser",
                                    arg=resolve_url["ucsc_id"].format(gene=loc),
                                    copytext=row["location"],
                                    valid=True,
                                    icon="gene.png")
        for i in ["entrez_id", "ucsc_id", "omim_id", "refseq_accession"]:
            name = i.replace("_"," ").title()
            if row[i] != "":
                wf.add_item(row[i], name, arg=resolve_url[i].format(gene=row[i]), copytext=row[i], valid=True, icon="gene.png")
        
        wf.add_item(row["locus_type"],"Locus Type", copytext=row["location"], valid=True, icon="info.png")
        if row["gene_family"] != "":
            wf.add_item(row["gene_family"],"Gene Family", copytext=row["gene_family"], valid=True, icon="info.png")

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable, so all module
    # functions can access it without having to pass the Workflow
    # instance around
    log = wf.logger
    wf.run(main)

