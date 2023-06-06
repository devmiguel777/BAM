import os
import openai
import csv
from time import sleep



class Manage:
	ia = openai
	def __init__(self):	
		self.ia.organization = 'org-URmP9nbM9isoLzMHmQP2ZgUn'
		self.ia.api_key = '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'




	as_pro          = '' # 'Aja como o melhor proficional de marketing do mundo'
	revice_as       = ''

	#Gere uma lista de conteudos para postar todos os dias entre 25-19 no instagram da empresa supreme lubrificantes, 
	#com o publico alvo de mecanicos e engenheiros, nessa lista dee aver as seguintes colunas [tipo do conteudo, melhor
	# hora pra postar, hashtags de sucesso, formato(ex:reels, carrosel, imagem), ideia de copy, titulo chamativo, mais 
	#qualquer informaçao importante]
	#


	def make_quest(quest, as_pro, revice_as):
	    return as_pro + '\n' + revice_as




	def send_quest(quest, model="gpt-3.5-turbo", user='user'):
	    sleep(30)
	    return openai.ChatCompletion.create(
	    model=model,
	    messages=[
	        {"role": user, "content": quest}
	    ]
	    )

