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



def feed_tweets(quantidade, autorizacao):
    planilha = pd.read_excel('DataBase.xlsx', "Sheet1")
    #Cria um objeto para a captura
    api = tweepy.API(auth)
    #Inicia a captura, para mais detalhes: ver a documentação do tweepy
    i = 0
    novas_mensagens = 0
    while i < quantidade:
        repeater = 0
        for msg in tweepy.Cursor(api.search, q="{0} -filter:retweets".format("depressao"), lang='pt', tweet_mode="extended").items():
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
                print("[{2}]\n{0}\n{1}".format(new_msg["User Name"], new_msg["Tweet Text"], i))
                novas_mensagens +=1
                
            else:
                print("[{}] Tweet repetido".format(i))
            print('[{}] -=-=-=-=-= aguardando 4.5 segundos =-=-=-=-=-\n\n'.format(i))
            time.sleep(4.5)
            if i >= quantidade or repeater >= 10:
                print("[Encerrando Programa]")
                break
    print(planilha.loc[:][["User Name","Tweet Text"]].sort_values(by="User Name").head(10))
    print("{} new messages in DataBase.xlsx".format(novas_mensagens))
    return True
    
def return_tweet(quantidade, autorizacao):
    """return_tweet(autorizacao, quantidade)"""
    api = tweepy.API(autorizacao)
    i = 0
    anterior = {'User Name': 'foo',
                'Tweet Created At': 'foo','Tweet Text': 'foo','Relevância': 'foo',
                'User Location': 'foo','Phone Type': 'foo',
                'Favorite Count': 'foo','Retweets':'foo'}
    novas_mensagens = 0
    while i < quantidade:
        for msg in tweepy.Cursor(api.search, q="{0} -filter:retweets".format("depressao"), lang='pt', tweet_mode="extended").items():
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
            if  new_msg["Tweet Text"] != anterior["Tweet Text"]:
                anterior = new_msg
                print("[{2}]\n{0}\n{1}".format(new_msg["User Name"], new_msg["Tweet Text"], i))
                novas_mensagens +=1
                
            else:
                print("[***] Tweet repetido")
            print("\t -=-=-=-=-= aguardando 4.5 segundos =-=-=-=-=-\n\n")
            time.sleep(4.5)
            if i >= quantidade:
                break
        print("[Fim do Programa]")

def get_text(autorizacao):
    """return_tweet(autorizacao, quantidade)"""
    api = tweepy.API(autorizacao)
    lista_vazia = []
    for msg in tweepy.Cursor(api.search, q="{0} -filter:retweets".format("depressao"), lang='pt', tweet_mode="extended").items():
        new_msg = { 
            # 'User Name': msg.user.name,
            #         'Tweet Created At': msg.created_at,
                    'Tweet Text': msg.full_text.lower(),
                    # 'Relevância': '',
                    # 'User Location': msg.user.location,
                    # 'Phone Type': msg.source,
                    # 'Favorite Count': msg.favorite_count,
                    # 'Retweets':msg.retweet_count
                    }
        lista_vazia.append(new_msg["Tweet Text"])
        break
    return new_msg["Tweet Text"]


