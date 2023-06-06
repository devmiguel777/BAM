from django.db import models
from django.utils import timezone
# Create your models here.
from chatgpt.api_manage import *
from .models import Post, Analize
from chatgpt.models import Infotext, Pedido, Registro
from time import sleep


topics = ( "Vocação turística do litoral sul de Alagoas", "Vocações de gastronomia no litoral sul de Alagoas", "Principais pontos turísticos do litoral sul de Alagoas", "Vocações turísticas da região do quilombo em alagoas", "Principais pontos turísticos da região do quilombo em Alagoas" )

order = Pedido.objects.get(nome_do_cliente="Rotas Inteligentes")


def make_analize(_from, _query):
    send_question(_query=+" "+ str(_from))


def make_post(category = "default", pretop="faca um artigo sobre ",top='games ', postop= "usando em seu texto palavras chaves expesificas em alta no google trends como um redator que prenda a atensao do usuario"):
    text = send_quest(pretop + top +postop).choices[0].message['content']
    title = send_quest("faca um titulo chamativo para o seguinte post'''"+text).choices[0].message['content']
    sub_t = send_quest(" faca um subtitulo chamativo e sujestivo para esse titulo '''" + title + "''' que descrava esse texto '''" + text + "'''").choices[0].message['content']
    short_title = send_quest(" faca um tilulo curtito que reduza '''" + sub_t +"''' em no maximo 16 caracteres").choices[0].message['content']
    short_desc = send_quest(" faca uma descricao curta de no maximo 64 caracteres do sefuinte texto '''" + text).choices[0].message['content']

    post= Post(

     title = title,
        subtitle = sub_t,
        short_title = short_title,
        short_desc = short_desc,
        context = text,
        category = category,
    )
    post.save()
    Registro(pedido=order,post=post).save()
    sleep(20)
    return post






def make_post_analizer(artigo):
    _q = f"""
Descreva em detalhes a analize feita informando as seguintes informaçoes
'publico alvo;uma persona que iria compartilhar essa informação;os principa erros sobre e apenas se for reconhecido;como melhorar essa publicação'

do seguinte artigo escrito para um jornal
{artigo.context}
    """
    _r = send_quest(_q).choices[0].message['content']
    Analize(post=artigo, text=_r).save()



category = "nd "



for i in topics:
    print("+1")
    text= """ topico=" """
    for j in i:
        text += j
    text += '"'

    a = make_post(category=category,top=text)
    make_post_analizer(a)

topics = ("Estratégias de marketing digital",
 "Importância do conteúdo para o marketing digital",
 "Tendências de marketing digital")



for i in topics:
    print("+1")

    text= """ topico=" """
    for j in i:
        text += j
    text += '"'

    a = make_post(category=category,top=text)
    make_post_analizer(a)
