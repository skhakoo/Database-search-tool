# Database-search-tool

##Name
Local Database Search Tool 

## Description
Is a tool to look up information in a local database linking microRNAs, genes, and diseases with the associated gene prediction and disease prediction scores. Users can search the database for available miRNAs and diseases. Users can also lookup miRNAs and genes a specific disease is associated to, or diseases and genes a specific miRNA is associated to. The different associations can be filtered down using gene or disease confidence scores. 

##Installation
#run database search tool
‘python database.py 

## Usage
`python database.py

#If help is required
`python database.py -h

#Search up available miRNAs e.g., all hsa-let miRNAs
‘python database.py -search_miRNA hsa-let

#Search available diseases e.g., beginning with cardio
‘python database.py -search_disease ‘cardio’

#Look up a specific miRNA with its associated diseases and genes with prediction scores
‘python database.py -miRNA hsa-let-7a-2-3p -score true

#Look up a specific miRNA with its associated diseases and genes filtered by gene prediction score
‘Python database.py -miRNA hsa-let-7a-2-3p -score true -Gconfidence 90

#Look up a specific miRNA with its associated diseases and genes filtered by disease prediction score
‘python database.py -miRNA hsa-let-7a-2-3p -score true -Dconfidence 90

#Look up a specific miRNA with its associated diseases and genes without prediction scores
‘python database.py -miRNA hsa-let-7a-2-3p -score false

#Look up a specific disease with its associated miRNAs and genes with prediction scores
‘python database.py -disease ‘smith-magenis syndrome’ -score true

#Look up disease with their associated miRNA and genes filtered by gene prediction score
‘python database.py -disease ‘schizophrenia’ -score true -Gconfidence 90

#Look up disease with their associated miRNA and genes filtered by disease prediction score
‘python database.py -disease ‘schizophrenia’ -score true -Dconfidence 90

#Look up disease with their associated miRNA and genes without prediction scores 
‘python database.py -disease ‘cardiomyopathy dilated 1hh’ -score false
