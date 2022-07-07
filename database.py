import pandas as pd
import argparse
df = pd.read_csv ('clean-data.csv') #import clean dataset
df.drop(df.columns[3], axis=1, inplace=True) #dropping the organism column from the dataframe  
df.drop(df.columns[1], axis = 1, inplace = True) #dropping the locus column from the dataframe

df.columns = ['miRNA', 'Gene_Pred_Score', 'Associated_Gene', 'Associated_Disease', 'Disease_Pred_Score']
M_df = df[['miRNA', 'Associated_Gene', 'Associated_Disease', 'Gene_Pred_Score', 'Disease_Pred_Score']] #creating a dataframe for miRNA and associated genes and diseases 
M_df.drop_duplicates(inplace = True) #dropping all duplicates in the miRNA dataframe 


df.columns = ['Associated_miRNA', 'Gene_Pred_Score', 'Associated_Gene', 'Disease', 'Disease_Pred_Score']
D_df = df[['Disease', 'Associated_Gene', 'Associated_miRNA', 'Gene_Pred_Score', 'Disease_Pred_Score']] #creating a dataframe for diseases and their associated genes and miRNAs 
D_df.drop_duplicates(inplace = True) #dropping all duplicates in the disease dataframe 


#Creating arguments for the command line interface 
parser = argparse.ArgumentParser(description = "Search through database") #The parser is used to search through the database
parser.add_argument("-search_miRNA", help = "search for available miRNAs", type = str.lower) #argument to search for available miRNAs 
parser.add_argument("-search_disease", help = "search for available diseases", type = str.lower) #argument to search for available diseases 
parser.add_argument("-miRNA", help="Search for specific miRNAs and their associated diseases", type = str.lower)#argument to search for specific miRNAs and their associated genes and diseases 
parser.add_argument("-disease", help="Search for spcecific diseases and their associated miRNAs", type = str.lower) #argument to search for specific diseases and their associated genes and diseases
parser.add_argument("-score", help = "Type True to view both prediction scores and False to view without", type = str.lower, choices = ['true', 'false']) #arugment which allows you to choose whether to include scores or not 
parser.add_argument("-Gconfidence", help = "Enter a gene confidence score to filter down associations (between 0 and 100)", type = float) #argument to filter output by gene predicition scores 
parser.add_argument("-Dconfidence", help = "Enter a disease confidence score to filter down associations (between 0 and 100)", type = float) #argument to filter output by disease prediction scores
args = parser.parse_args()


#miRNA search
if args.search_miRNA is not None:                                    #if the user uses the search_miRNA argument
    if M_df['miRNA'].str.contains(args.search_miRNA).any():            #if the string entered is in the miRNA column of the dataframe
        miRNA_df = M_df[M_df['miRNA'].str.contains(args.search_miRNA)]   #create dataframe with only miRNAs matching that string
        m_df = miRNA_df[['miRNA']]                                    # create a dataframe with only the miRNA column
        m_df.drop_duplicates(inplace = True)                         #drop all the duplicates 
        print(m_df.to_string(index = False))                         #print that dataframe 
    else:
        print('InputError: The string entered is not an miRNA found in this database')  
        #if the string does not match any entries in the database print this error message 


#disease search
if args.search_disease is not None:                                   #if the user uses the search_disease argument 
    if D_df['Disease'].str.contains(args.search_disease).any():         #is the string entered matches entries in the disease column of the dataframe 
        disease_df = D_df[D_df['Disease'].str.contains(args.search_disease)]  #create a dataframe with only matches to the inputed string
        d_df = disease_df[['Disease']]                                #create a dataframe with only the disease column
        d_df.drop_duplicates(inplace = True)                          #drop all the duplicates in the dataframe 
        print(d_df.to_string(index=False))                            #print that dataframe 
    else:
        print('InputError: The string entered is not a disease found in this database')
        #if the string does not match any entries in the database print this error message


#if the arguments miRNA and gene confidence score are inputed and the score argument is true 
if args.miRNA is not None and args.score == 'true' and args.Gconfidence is not None:
    m_d_df = M_df[(M_df['miRNA'] == args.miRNA) & (M_df['Gene_Pred_Score'] >= args.Gconfidence)] #filter the dataframe to contain the inputed miRNA and Gconfidence score that is equal or greater than the inputed argument
    if m_d_df.empty and 80 <= args.Gconfidence <= 100 and M_df['miRNA'].str.contains(args.miRNA).any(): #if the dataframe is empty and Gconfidence argument is between 80 and 100 and the original dataframe contains the inputed miRNA print the error message below
        print('EmptyDataFrame: There are no matches to your current search with the associated confidence score, please filter using a lower value')
    else:    #otherwise print the dataframe 
        print(m_d_df.to_string(index=False))
    if not 80 <= args.Gconfidence <= 100: #if the confidence score is not between 80 and 100 print the error message below 
        print("ValueError: Confidence integer out of range, please choose a number between 0 and 100")
    if ~M_df['miRNA'].str.contains(args.miRNA).any(): #if the original dataframe does not contain the inputed miRNA print the error message below 
        print('InputError: argument -miRNA: the miRNA entered is not found in this database please check the spelling or use -search_miRNA to view available miRNAs')


# if the arguments miRNA and disease confidence score are inputed and the score argument is true
if args.miRNA is not None and args.score == 'true' and args.Dconfidence is not None:
    m_d_df = M_df[(M_df['miRNA'] == args.miRNA) & (M_df['Disease_Pred_Score'] >= args.Dconfidence)] #filter the dataframe to contain the inputed miRNA and Dconfidence score that is equal or greater than the inputed argument 
    if m_d_df.empty and 80 <= args.Dconfidence <= 100 and M_df['miRNA'].str.contains(args.miRNA).any(): #if the dataframe is empty and Dconfidence argument is between 80 and 100 and the original dataframe contains the inputed miRNA print the error message below 
        print('EmptyDataFrame: There are no matches to your current search with the associated confidence score, please filter using a lower value')
    else: #otherwise print the dataframe 
        print(m_d_df.to_string(index=False))
    if not 80 <= args.Dconfidence <= 100: #if the confidence score is not between 80 and 100 print the error message below
        print("ValueError: Confidence integer out of range, please choose a number between 0 and 100")
    if ~M_df['miRNA'].str.contains(args.miRNA).any(): #if the original dataframe does not contain the inputed miRNA print the error message below 
        print('InputError: argument -miRNA: the miRNA entered is not found in this database please check the spelling or use -search_miRNA to view available miRNAs')


#if the miRNA argument is inputed and the score argument inputed is 'false'
if args.miRNA is not None and args.score == 'false': 
    m_d_df = M_df[(M_df['miRNA'] == args.miRNA)] #create a dataframe only containing matches to the inputed miRNA 
    if ~M_df['miRNA'].str.contains(args.miRNA).any(): #if the miRNA dataframe does not contain the inputed miRNA print the error message below 
        print('InputError: argument -miRNA: the miRNA entered is not found in this database please check the spelling or use -search_miRNA to view available miRNAs')
    else: #otherwise print the dataframe 
        print(m_d_df[['miRNA', 'Associated_Gene', 'Associated_Disease']].to_string(index=False))


#if the only the arguments miRNA and score are inputed and the inputed score is 'true'        
if args.miRNA is not None and args.score == 'true' and args.Gconfidence is None and args.Dconfidence is None: 
    m_d_df = M_df[(M_df['miRNA'] == args.miRNA)] #create a dataframe only containing matches to the inputed miRNA 
    if ~M_df['miRNA'].str.contains(args.miRNA).any(): #if the miRNA dataframe does not contain the inputed miRNA print the error message below
        print('InputError: argument -miRNA: the miRNA entered is not found in this database please check the spelling or use -search_miRNA to view available miRNAs')
    else: #otherwise print the dataframe 
        print(m_d_df.to_string(index=False))


#if the user does not include score argument when trying to filter down miRNAs by prediction scores print an error message explaining the required arguments 
if args.miRNA is not None and args.Gconfidence is not None and args.score is None:
    print('ArgumentError: To filter down diseases by confidence scores the following arguments are required: -miRNA -score -Gconfidence')
if args.miRNA is not None and args.Dconfidence is not None and args.score is None:
    print('ArgumentError: To filter down diseases by confidence scores the following arguments are required: -miRNA -score -Dconfidence')



#if the argumetns disease and gene cconfidence are included and the score argument inputed is 'true'
if args.disease is not None and args.score == 'true' and args.Gconfidence is not None:
    d_m_df = D_df[(D_df['Disease'] == args.disease) & (D_df['Gene_Pred_Score'] > args.Gconfidence)] #filter the dataframe to contain the inputed disease and Gconfidence score that is equal or greater than the inputed argument
    if d_m_df.empty and 80 <= args.Gconfidence <= 100 and D_df['Disease'].str.contains(args.disease).any(): #if the dataframe is empty and Gconfidence argument is between 80 and 100 and the original dataframe contains the inputed miRNA print the error message below
        print('EmptyDataFrame: There are no matches to your current search with the associated confidence score, please filter using a lower value')
    else: #otherwise print the dataframe
        print(d_m_df.to_string(index=False))
    if not 80 <= args.Gconfidence <= 100: #if the inputed Gconfidence score is not between 80 and 100 print the error message below 
        print("ValueError: Confidence integer out of range, please choose a number between 80 and 100")
    if ~D_df['Disease'].str.contains(args.disease).any(): #if the inputed disease is not found in the disease dataframe print the below error message 
        print('InputError: argument -disease: the disease entered is not found in this database please check the spelling or use -search_disease to view available diseases')


#if the arguments disease and gene cconfidence are included and the score argument inputed is 'true'
if args.disease is not None and args.score == 'true' and args.Dconfidence is not None:
    d_m_df = D_df[(D_df['Disease'] == args.disease) & (D_df['Disease_Pred_Score'] >= args.Dconfidence)] #filter the dataframe to contain the inputed disease and Dconfidence score that is equal or greater than the inputed argument
    if d_m_df.empty and 80 <= args.Dconfidence <= 100 and D_df['Disease'].str.contains(args.disease).any(): #if the dataframe is empty and Gconfidence argument is between 80 and 100 and the original dataframe contains the inputed miRNA print the error message below
        print('EmptyDataFrame: There are no matches to your current search with the associated confidence score, please filter using a lower value')
    else: #print the dataframe 
        print(d_m_df.to_string(index=False))
    if not 80 <= args.Dconfidence <= 100: #if the inputed disease confidence score is not between 80 and 100 print the error message below 
        print("ValueError: Confidence integer out of range, please choose a number between 80 and 100")
    if ~D_df['Disease'].str.contains(args.disease).any(): #if the inputed disease is not found in the disease dataframe print the below error message
        print('InputError: argument -disease: the disease entered is not found in this database please check the spelling or use -search_disease to view available diseases')


#if the disease argument is inputed and the score argument inputed is 'false'
if args.disease is not None and args.score == 'false': 
    d_m_df = D_df[(D_df['Disease'] == args.disease)] #create a dataframe only containing matches to the inputed disease 
    if ~D_df['Disease'].str.contains(args.disease).any(): #if the disease dataframe does not contain the inputed disease print the error message below 
        print('InputError: argument -disease: the disease entered is not found in this database please check the spelling or use -search_disease to view available disease')
    else: #otherwise print the dataframe 
        print(d_m_df[['Disease', 'Associated_Gene', 'Associated_miRNA']].to_string(index=False))


#if the only the arguments disease and score are inputed and the inputed score is 'true'        
if args.disease is not None and args.score == 'true' and args.Gconfidence is None and args.Dconfidence is None: 
    d_m_df = D_df[(D_df['Disease'] == args.disease)] #create a dataframe only containing matches to the inputed disease 
    if ~D_df['Disease'].str.contains(args.disease).any(): #if the disease dataframe does not contain the inputed disease print the error message below
        print('InputError: argument -disease: the disease entered is not found in this database please check the spelling or use -search_disease to view available diseases')
    else: #otherwise print the dataframe 
        print(d_m_df.to_string(index=False))

#if the user does not include score argument when trying to filter down diseases by prediction scores print an error message explaining the required arguments
if args.disease is not None and args.Gconfidence is not None and args.score is None:
    print('ArgumentError: To filter down diseases by confidence scores the following arguments are required: -disease -score -Gconfidence')
if args.disease is not None and args.Dconfidence is not None and args.score is None:
    print('ArgumentError: To filter down diseases by confidence scores the following arguments are required: -disease -score -Dconfidence')
        