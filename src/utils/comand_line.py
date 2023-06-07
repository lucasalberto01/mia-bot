import aiml

ai_neutra = aiml.Kernel() # inicialização
ai_neutra.learn('neutro.xml') # le o arquivo principal da AIML e faz referencias aos outros
ai_neutra.respond('load aiml b') # faz com que os outros arquivos da AIML sejam carregados

while True:
	entrada = input('>> ')
	saida = ai_neutra.respond(entrada)
	saida = saida.replace('#', ' ')
	print('> ', saida)
	print('\n')