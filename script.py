# -*- coding: utf-8 -*-
"""
Script que baixa tweets indefinidamente.
"""
import tweepy
import os.path
import pandas as pd
import json
import time

#leitura do arquivo no formato JSON
with open('auth.pass') as fp:    
    data = json.load(fp)

#Configurando a biblioteca. Não modificar
auth = tweepy.OAuthHandler(data['consumer_key'], data['consumer_secret'])
auth.set_access_token(data['access_token'], data['access_token_secret'])


#Produto escolhido:
produto = 'depressao'
#Filtro de língua, escolha uma na tabela ISO 639-1.
lang = 'pt'





planilha = pd.read_excel('DataBase.xlsx', "Sheet1")
#Cria um objeto para a captura
api = tweepy.API(auth)
#Inicia a captura, para mais detalhes: ver a documentação do tweepy
i = 0
Limite = 50
while i < Limite:
    for msg in tweepy.Cursor(api.search, q="{0} -filter:retweets".format(produto), lang=lang, tweet_mode="extended", count=200).items():
        new_msg = { 'User Name': msg.user.name,
                    'Tweet Created At': msg.created_at,
                    'Tweet Text': msg.full_text.lower(),
                    'Relevância': '',
                    'User Location': msg.user.location,
                    'Phone Type': msg.source,
                    'Favorite Count': msg.favorite_count,
                    'Retweets':msg.retweet_count
                    }
        i += 1
        if new_msg["Tweet Text"] not in planilha["Tweet Text"]:
            writer = pd.ExcelWriter('DataBase.xlsx', engine='xlsxwriter')
            planilha = planilha.append(pd.DataFrame([new_msg]), ignore_index=True)
            planilha.to_excel(excel_writer = writer, index = False)
            writer.save()   
            print("new_message: {0}".format(new_msg["Tweet Text"]))
            print('[{}] aguardando 5 segundos'.format(i))
            time.sleep(5)
        else:
            time.sleep(2)
        if i >= Limite:
            break
    
    