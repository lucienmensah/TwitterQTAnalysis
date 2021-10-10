# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 20:38:46 2021

@author: Lucien
"""
import pandas as pd
import sys
import re
import matplotlib.pyplot as plt
from nltk.corpus import twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords, movie_reviews
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
from datetime import date
import re, string, random
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from scipy import stats
import numpy as np
'''
x = input("Enter a file name: ")
#data needs to be a global var for plots
dataset = pd.read_csv(x)

#this gives us the numbers of nos and yeses within a certain category
#if i put something in the value_counts, it gives me a percentage
multi =  dataset['he/him'].value_counts()
num_he = multi[1]
print(multi)
multi =  dataset['she/her'].value_counts()
num_she = multi[1]
print(multi)
multi =  dataset['they/them'].value_counts()
num_they = multi[1]
print(multi)
print(num_they,num_he,num_she)
'''
#should start off with some exploratory data analysis

#control
#more specific test
#ks test
#stats tests fpr validity
trans_fn_list = ["4_17/transgender_417.csv", "4_18/transgender_4_18.csv", "4_19/transgender_4_19.csv", "4_20/transgender_4_20.csv", "4_21/transgender_4_21.csv", "4_22/transgender_4_22.csv", "4_24/transgender_4_24.csv"]
trans_df_list = [pd.read_csv(fn) for fn in trans_fn_list]
trans_concat = pd.concat(trans_df_list).reset_index(drop=True)
multi =  trans_concat['he/him'].value_counts()
trans_he = multi[1]
multi =  trans_concat['she/her'].value_counts()
trans_she = multi[1]
multi =  trans_concat['they/them'].value_counts()
trans_they = multi[1]
#multi =  trans_concat['xe/xem'].value_counts()
#num_xe = multi[1]
multi =  trans_concat['it/its'].value_counts()
trans_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(trans_they,trans_he,trans_she, trans_it)
#print("chi-squared for trans: ", stats.chisquare([trans_they,trans_he,trans_she, trans_it]))

bimbo_fn_list = ["4_17/bimbo_417.csv", "4_18/bimbo_4_18.csv", "4_19/bimbo_4_19.csv", "4_20/bimbo_4_20.csv", "4_21/bimbo_4_21.csv", "4_22/bimbo_4_22.csv", "4_24/bimbo_4_24.csv"]
bimbo_df_list = [pd.read_csv(fn) for fn in bimbo_fn_list]
bimbo_concat = pd.concat(bimbo_df_list).reset_index(drop=True)
multi =  bimbo_concat['he/him'].value_counts()
bimbo_he = multi[1]
multi =  bimbo_concat['she/her'].value_counts()
bimbo_she = multi[1]
multi =  bimbo_concat['they/them'].value_counts()
bimbo_they = multi[1]
#multi =  trans_concat['xe/xem'].value_counts()
#num_xe = multi[1]
multi =  bimbo_concat['it/its'].value_counts()
bimbo_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(bimbo_they,bimbo_he,bimbo_she,bimbo_it)
#print("chi-squared for bimbo: ", stats.chisquare([bimbo_they,bimbo_he,bimbo_she, bimbo_it]))

himbo_fn_list = ["4_17/himbo_417.csv", "4_18/himbo_4_18.csv", "4_19/himbo_4_19.csv", "4_20/himbo_4_20.csv", "4_21/himbo_4_21.csv", "4_22/himbo_4_22.csv", "4_24/himbo_4_24.csv"]
himbo_df_list = [pd.read_csv(fn) for fn in himbo_fn_list]
himbo_concat = pd.concat(himbo_df_list).reset_index(drop=True)
multi =  himbo_concat['he/him'].value_counts()
himbo_he = multi[1]
multi =  himbo_concat['she/her'].value_counts()
himbo_she = multi[1]
multi =  himbo_concat['they/them'].value_counts()
himbo_they = multi[1]
#multi =  trans_concat['xe/xem'].value_counts()
#num_xe = multi[1]
multi =  himbo_concat['it/its'].value_counts()
himbo_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(himbo_they,himbo_he,himbo_she, himbo_it)
#print("chi-squared for himbo: ", stats.chisquare([himbo_they,himbo_he,himbo_she, himbo_it]))

thembo_fn_list = ["4_17/thembo_417.csv", "4_18/thembo_4_18.csv", "4_19/thembo_4_19.csv", "4_20/thembo_4_20.csv", "4_21/thembo_4_21.csv", "4_22/thembo_4_22.csv", "4_24/thembo_4_24.csv"]
thembo_df_list = [pd.read_csv(fn) for fn in thembo_fn_list]
thembo_concat = pd.concat(thembo_df_list).reset_index(drop=True)
multi =  thembo_concat['he/him'].value_counts()
them_he = multi[1]
multi =  thembo_concat['she/her'].value_counts()
them_she = multi[1]
multi =  thembo_concat['they/them'].value_counts()
them_they = multi[1]
#multi =  thembo_concat['xe/xem'].value_counts()
#them_xe = multi[1]
multi =  thembo_concat['it/its'].value_counts()
them_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(them_they,them_he,them_she, them_it)
#print("chi-squared for thembo: ", stats.chisquare([them_they,them_he,them_she, them_it]))
'''
them_counts = np.array([them_they,them_he,them_she, them_it])
trans_counts = np.array([trans_they,trans_he,trans_she, trans_it])
trans_counts_scaled = ((trans_counts * them_counts.sum()) / trans_counts.sum())
print(them_counts)
print(trans_counts)
print(trans_counts_scaled)
print("chi-squared for thembo compared to transgender: ", stats.chisquare(them_counts, f_exp=trans_counts_scaled))


print("chi-squared for thembo compared to transgender with ddof: ", stats.chisquare(them_counts, f_exp=trans_counts_scaled,  ddof=[0,-1,-2]))
'''
theybie_fn_list = ["4_17/theybie_417.csv", "4_18/theybie_4_18.csv", "4_19/theybie_4_19.csv", "4_20/theybie_4_20.csv", "4_21/theybie_4_21.csv", "4_22/theybie_4_22.csv", "4_24/theybie_4_24.csv"]
theybie_df_list = [pd.read_csv(fn) for fn in theybie_fn_list]
theybie_concat = pd.concat(theybie_df_list).reset_index(drop=True)
multi =  theybie_concat['he/him'].value_counts()
num_he = multi[1]
multi =  theybie_concat['she/her'].value_counts()
num_she = multi[1]
multi =  theybie_concat['they/them'].value_counts()
num_they = multi[1]
#multi =  theybie_concat['xe/xem'].value_counts()
#num_xe = multi[1]
multi =  theybie_concat['it/its'].value_counts()
num_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(num_they,num_he,num_she, num_it)
#print("chi-squared for theybie: ", stats.chisquare([num_they,num_he,num_she, num_xe, num_it]))

gentlethem_fn_list = ["4_17/gentlethem_417.csv", "4_18/gentlethem_4_18.csv", "4_19/gentlethem_4_19.csv", "4_20/gentlethem_4_20.csv", "4_21/gentlethem_4_21.csv", "4_22/gentlethem_4_22.csv", "4_24/gentlethem_4_24.csv"]
gentlethem_df_list = [pd.read_csv(fn) for fn in gentlethem_fn_list]
gentthem_concat = pd.concat(gentlethem_df_list).reset_index(drop=True)
multi =  gentthem_concat['he/him'].value_counts()
gentthem_he = multi[1]
multi =  gentthem_concat['she/her'].value_counts()
gentthem_she = multi[1]
multi =  gentthem_concat['they/them'].value_counts()
gentthem_they = multi[1]
#multi =  gentle_concat['xe/xem'].value_counts()
#num_xe = multi[1]
multi =  gentthem_concat['it/its'].value_counts()
gentthem_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(gentthem_they,gentthem_he,gentthem_she, gentthem_it)
#print("chi-squared for gentlethem: ", stats.chisquare([num_they,num_he,num_she, num_xe, num_it]))

gentle_fn_list = ["4_19/gentlemen_4_19.csv", "4_20/gentlemen_4_20.csv", "4_21/gentlemen_4_21.csv", "4_22/gentlemen_4_22.csv", "4_24/gentlemen_4_24.csv"]
gentle_df_list = [pd.read_csv(fn) for fn in gentle_fn_list] 
gentle_concat = pd.concat(gentle_df_list).reset_index(drop=True)
multi =  gentle_concat['he/him'].value_counts()
gent_he = multi[1]
multi =  gentle_concat['she/her'].value_counts()
gent_she = multi[1]
multi =  gentle_concat['they/them'].value_counts()
gent_they = multi[1]
#multi =  ladies_concat['xe/xem'].value_counts()
#num_xe = multi[1]
gent_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(gent_they,gent_he, gent_she, gent_it)


theydies_fn_list = ["4_17/theydies_417.csv", "4_18/theydies_4_18.csv", "4_19/theydies_4_19.csv", "4_20/theydies_4_20.csv", "4_21/theydies_4_21.csv", "4_22/theydies_4_22.csv", "4_24/theydies_4_24.csv"]
theydies_df_list = [pd.read_csv(fn) for fn in theydies_fn_list] 
theydies_concat = pd.concat(theydies_df_list).reset_index(drop=True)
multi =  theydies_concat['he/him'].value_counts()
theyd_he = multi[1]
multi =  theydies_concat['she/her'].value_counts()
theyd_she = multi[1]
multi =  theydies_concat['they/them'].value_counts()
num_they = multi[1]
multi =  theydies_concat['xe/xem'].value_counts()
num_xe = multi[1]
multi =  theydies_concat['it/its'].value_counts()
num_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(num_they,theyd_he, theyd_she, num_xe, num_it)
#print("chi-squared for theydies: ", stats.chisquare([num_they,num_he,num_she, num_xe, num_it]))

ladies_fn_list = ["4_19/ladies_4_19.csv", "4_20/ladies_4_20.csv", "4_21/ladies_4_21.csv", "4_22/ladies_4_22.csv", "4_24/ladies_4_24.csv"]
ladies_df_list = [pd.read_csv(fn) for fn in ladies_fn_list] 
ladies_concat = pd.concat(ladies_df_list).reset_index(drop=True)
multi =  ladies_concat['he/him'].value_counts()
lad_he = multi[1]
multi =  ladies_concat['she/her'].value_counts()
lad_she = multi[1]
multi =  ladies_concat['they/them'].value_counts()
lad_they = multi[1]
#multi =  ladies_concat['xe/xem'].value_counts()
#num_xe = multi[1]
multi =  ladies_concat['it/its'].value_counts()
lad_it = multi[1]
#multi =  concatenated['ze/zir'].value_counts()
#num_ze = multi[1]
#print(lad_they,lad_he, lad_she, lad_it)
#print("chi-squared for ladies: ", stats.chisquare([lad_they, lad_he,lad_she, lad_it]))

#could use T-test to compare the proportion of she/her and he/him in theydies to the proportions of she/her and he/him in ladies
#rand variable 1 - she/her 0 - he/him
#theydies to ladies
theydies_n = theyd_he + theyd_she #counts
theydies_m = theyd_she / theydies_n #bernolli mean, aka what is the chance of the coin landing on she
theydies_std = np.sqrt(theydies_m*(1-theydies_m))  #sqr of mean div mean

lad_n = lad_he + lad_she #counts
lad_m = lad_she / lad_n #bernolli mean, aka what is the chance of the coin landing on she
lad_std = np.sqrt(lad_m*(1-lad_m))  #sqr of mean div mean

print("theydies to ladies\n")
print(stats.ttest_ind_from_stats(mean1=theydies_m, std1=theydies_std, nobs1=theydies_n,mean2=lad_m, std2=lad_std, nobs2=lad_n))
print("counts: ", theydies_n, " mean: ", theydies_m)
print("counts: ", lad_n, " mean: ", lad_m)

#theydies to gentlemen

gent_n = gent_he + gent_she #counts
gent_m = gent_she / gent_n #bernolli mean, aka what is the chance of the coin landing on she
gent_std = np.sqrt(gent_m*(1-gent_m))  #sqr of mean div mean

print("theydies to gentlemen\n")
print(stats.ttest_ind_from_stats(mean1=theydies_m, std1=theydies_std, nobs1=theydies_n,mean2=gent_m, std2=gent_std, nobs2=gent_n))
print("counts: ", theydies_n, " mean: ", theydies_m)
print("counts: ", gent_n, " mean: ", gent_m)
#print("chi-squared for ladies: ", stats.chisquare([lad_they, lad_he,lad_she, lad_it]))
#ladies to gentlethem
gentthem_n = gentthem_he + gentthem_she #counts
gentthem_m = gentthem_she / gentthem_n #bernolli mean, aka what is the chance of the coin landing on she
gentthem_std = np.sqrt(gentthem_m*(1-gentthem_m))  #sqr of mean div mean

print("ladies to gentlethem\n")
print(stats.ttest_ind_from_stats(mean1=lad_m, std1=lad_std, nobs1=lad_n,mean2=gentthem_m, std2=gentthem_std, nobs2=gentthem_n))
print("counts: ", lad_n, " mean: ", lad_m)
print("counts: ", gentthem_n, " mean: ", gentthem_m)

#gentlethem to gentlemen
print("gentlethem to gentlemen\n")
print(stats.ttest_ind_from_stats(mean1=gentthem_m, std1=gentthem_std, nobs1=gentthem_n,mean2=gent_m, std2=gent_std, nobs2=gent_n))
print("counts: ", gentthem_n, " mean: ", gentthem_m)
print("counts: ", gent_n, " mean: ", gent_m)

#theydies to gentlethem
print("gentlethem to theydies\n")
print(stats.ttest_ind_from_stats(mean1=gentthem_m, std1=gentthem_std, nobs1=gentthem_n,mean2=theydies_m, std2=theydies_std, nobs2=theydies_n))
print("counts: ", gentthem_n, " mean: ", gentthem_m)
print("counts: ", theydies_n, " mean: ", theydies_m)

#ladies to gentlemen
print("ladies to gentlemen\n")
print(stats.ttest_ind_from_stats(mean1=lad_m, std1=lad_std, nobs1=lad_n,mean2=gent_m, std2=gent_std, nobs2=gent_n))
print("counts: ", lad_n, " mean: ", lad_m)
print("counts: ", gent_n, " mean: ", gent_m)

#read about ks test
#find paper about twitter eethcicality