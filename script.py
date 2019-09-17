# -*- coding: utf-8 -*-
"""
Script que baixa tweets indefinidamente.
"""
import tweepy
import os.path
import pandas as pd
import json
import time
from random import shuffle

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
Limite = 200
novas_mensagens = 0
while i < Limite:
    for msg in tweepy.Cursor(api.search, q="{0} -filter:retweets".format(produto), lang=lang, tweet_mode="extended", count=10).items():
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
        if  new_msg["Tweet Text"] not in planilha["Tweet Text"].values:
            writer = pd.ExcelWriter('DataBase.xlsx', engine='xlsxwriter')
            planilha = planilha.append(pd.DataFrame([new_msg]), ignore_index=True)
            planilha.to_excel(excel_writer = writer, index = False)
            writer.save()   
            print("[{2}]\t{0}\t{1}".format(new_msg["User Name"], new_msg["Tweet Text"], i))
            novas_mensagens +=1
            
        else:
            print("[{}] Tweet repetido".format(i))
        print('[{}] -=-=-=-=-= aguardando 5 segundos =-=-=-=-=-\n\n'.format(i))
        time.sleep(5)
        if i >= Limite:
            break
    print("[Encerrando Programa]")
print(planilha.loc[:][["User Name","Tweet Text"]].sort_values(by="User Name"))
print("{} new messages in DataBase.xlsx".format(novas_mensagens))
    
    