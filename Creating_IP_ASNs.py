#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:33:33 2020

@author: jacksonbrietzke
"""
import csv
import subprocess
import ipaddress
import pandas as pd

def main():
    print("Creating IPs")
    asn_df = pd.read_csv("Full/Output/ASN_Scores.csv")
    create_whois_lookup(asn_df)
#    create_geolite_lookup(asn_df)
   
def create_whois_lookup(asn_df):
    print("Creating WHOIS")
    asn_list = []
    for x in range(0,500000):
        asn_list.append([x,0])

    for index, row in asn_df.iterrows():
        total_ips = 0
        try:
            ips = subprocess.check_output("whois -h whois.radb.net -- '-i origin AS" 
                            + str(row['ASN']) +
                            "'| grep -Eo '([0-9.]+){4}/[0-9]+'",
                            shell=True).decode("utf-8")
            ips = ips.split('\n')[:-1]
            if(ips != False):
                try:
                    for y in ips:
                        try:
                            total_ips += ipaddress.ip_network(y).num_addresses
                        except Exception as e: 
                            print(e)
                except Exception as e: 
                        print(e)
            else:
                print("Not doing this")
        except Exception as e: 
            print(e)
            
        asn_list[int(row['ASN'])] = [int(row['ASN']), total_ips]
    
    df = pd.DataFrame(asn_list, columns=['ASN', 'Total_IPs'])
    df.to_csv('Full/Output/whois_lookup.csv')
            
def create_geolite_lookup(asn_df):
    print("Creating Geolite")
    geo_df = pd.read_csv('geolite.csv', )
    geo_df = geo_df.drop(geo_df.columns[[0, 1, 4]], axis=1)
    geo_df = geo_df[geo_df.ASN != '-']
    geo_df = geo_df.astype({'ASN': int})
    print(geo_df.head())
#    geo_df.columns=geo_df.columns.str.strip()
    geo_df.sort_values(by='ASN', inplace=True)
    asn_list = []
    for x in range(0,600000):
        asn_list.append([x,0])
    current_ASN = 0
    current_ip_total = 0
    for index, row in geo_df.iterrows():
#            print(row['IP_CIDR'], type(row['ASN']))
        if(int(row['ASN']) == current_ASN):
            current_ip_total += ipaddress.ip_network(row['IP_CIDR']).num_addresses
        else:
            asn_list[current_ASN] = [current_ASN, current_ip_total]
            current_ASN = int(row['ASN'])
            current_ip_total = ipaddress.ip_network(row['IP_CIDR']).num_addresses
    asn_list[current_ASN] = [current_ASN, current_ip_total]
    df = pd.DataFrame(asn_list, columns=['ASN', 'Total_IPs'])
    df.to_csv('Full/Output/geolite_lookup.csv')

if __name__ == "__main__":
    main()