import cv2

# Carregar a imagem
imagem = cv2.imread('mazejogo.png')

# Converter para escala de cinza
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Binarizar a imagem (ajuste o valor do limiar conforme necessário)
_,imagem_preto_branco = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)

# Salvar ou exibir a imagem binarizada
cv2.imwrite('labirinto.jpg', imagem_preto_branco)
cv2.imshow('Preto e Branco', imagem_preto_branco)
cv2.waitKey(0)
cv2.destroyAllWindows()
