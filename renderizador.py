# Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
# Disciplina: Computação Gráfica
# Data: 28 de Agosto de 2020

import argparse     # Para tratar os parâmetros da linha de comando
import x3d          # Faz a leitura do arquivo X3D, gera o grafo de cena e faz traversal
import interface    # Janela de visualização baseada no Matplotlib
import gpu          # Simula os recursos de uma GPU


def polypoint2D(point, color):
    """ Função usada para renderizar Polypoint2D. """
    # Converte o esquema de cores
    color*=255
    color = int(color)

    for i in range(int(len(point)//2)):
        # Transforma de Float para inteiro cada X e Y
        y = int(point[(i*2)])
        x = int(point[(2*i)+1])

        # Define onde desenhar o pixel e com que cor
        gpu.GPU.set_pixel(
            y, x, color[0], color[1], color[2])


def polyline2D(lineSegments, color):
    """ Função usada para renderizar Polyline2D. """
    y1 = (lineSegments[0])
    y2 = (lineSegments[2])
    x1 = (lineSegments[1])
    x2 = (lineSegments[3])
    dx = abs(x2-x1)
    dy = abs(y2-y1)

    # Decide se usa X ou Y como base do FOR
    if(dx > dy):

        if(x1 < x2):
            # Comeca no ponto 1 e vai para ponto 2 - FOR em X
            s = (y2-y1)/(x2-x1)
            v = y1
            for u in range(int(x1), int(x2)+1):
                # altera um pixel da imagem
                gpu.GPU.set_pixel(int((v)//1), u, 255 *
                                  color[0], 255*color[1], 255*color[2])
                v += s
        else:
            # Comeca no ponto 2 e vai para ponto 1 - FOR em X
            s = (y1-y2)/(x1-x2)
            v = y2
            for u in range(int(x2), int(x1)+1):
                # altera um pixel da imagem
                gpu.GPU.set_pixel(int((v)//1), u, 255 *
                                  color[0], 255*color[1], 255*color[2])
                v += s

    else:

        if(y1 < y2):
            # Comeca no ponto 1 e vai para ponto 2 - FOR em Y
            s = (x2-x1)/(y2-y1)
            u = x1
            for v in range(int(y1), int(y2)+1):
                # altera um pixel da imagem
                gpu.GPU.set_pixel(v, int((u)//1), 255 *
                                  color[0], 255*color[1], 255*color[2])
                u += s
        else:
            # Comeca no ponto 2 e vai para ponto 1 - FOR em Y
            s = (x1-x2)/(y1-y2)
            u = x2
            for v in range(int(y2), int(y1)+1):
                # altera um pixel da imagem
                gpu.GPU.set_pixel(v, int((u)//1), 255 *
                                  color[0], 255*color[1], 255*color[2])
                u += s

        # gpu.GPU.set_pixel( int((v)//1), u, 255*color[0], 255*color[1], 255*color[2]) # altera um pixel da imagem


def triangleSet2D(vertices, color):
    """ Função usada para renderizar TriangleSet2D. """
    # Taxa de Supersampling
    supersample = 2

    # Salva os valores originais dos vertices
    y0_orig = vertices[0]
    x0_orig = vertices[1]
    y1_orig = vertices[2]
    x1_orig = vertices[3]
    y2_orig = vertices[4]
    x2_orig = vertices[5]

    # Valores dos vertices com supersampling
    y0 = y0_orig * supersample
    x0 = x0_orig * supersample
    y1 = y1_orig * supersample
    x1 = x1_orig * supersample
    y2 = y2_orig * supersample
    x2 = x2_orig * supersample

    x_min = round(min(x0, x1, x2))
    x_max = round(max(x0, x1, x2))
    y_min = round(min(y0, y1, y2))
    y_max = round(max(y0, y1, y2))

    # lista que vai guardar as coordenadas dos pixeis a serem desenhados, com supersampling
    lista_miniPixels = []

    # Verifica para cada pixel dentro do quadrado que contem o triangulo, se deve desenha-lo
    # calc0,calc1,calc2 
    for v in range(y_min-1, y_max+1):
        for u in range(x_min-1, x_max+1):
            
            calc1 = (y1-y2)*(u+0.5) + (x2-x1)*(v+0.5) + (x1*y2 - x2*y1)
            if((y1-y2)*(x0) + (x2-x1)*(y0) + (x1*y2 - x2*y1) < 0):
                calc1 *= -1

            if(calc1 >= 0):
                calc2 = (y0-y2)*(u+0.5) + (x2-x0)*(v+0.5) + (x0*y2 - x2*y0)
                if((y0-y2)*(x1) + (x2-x0)*(y1) + (x0*y2 - x2*y0) < 0):
                    calc2*=-1
                if(calc2 > 0):

                    calc3 = (y1-y0)*(u+0.5) + (x0-x1)*(v+0.5) + (x1*y0 - x0*y1)
                    if((y1-y0)*(x2) + (x0-x1)*(y2) + (x1*y0 - x0*y1) < 0):
                        calc3 *= -1
                    if(calc3>=0):
                        lista_miniPixels.append([u,v])
    
    x_min = round(min(x0_orig, x1_orig, x2_orig))
    x_max = round(max(x0_orig, x1_orig, x2_orig))
    y_min = round(min(y0_orig, y1_orig, y2_orig))
    y_max = round(max(y0_orig, y1_orig, y2_orig))

    for v in range(y_min-1, y_max+1):
        for u in range(x_min-1, x_max+1):
            intensity = sum(1 for i in lista_miniPixels if (i[0]//supersample == u and i[1]//supersample == v))/(supersample**2)
            # altera um pixel da imagem
            
            if(intensity>0):
                gpu.GPU.set_pixel(
                    v, u, 255*color[0]*intensity, 255*color[1]*intensity, 255*color[2]*intensity)


LARGURA = 30
ALTURA = 20

if __name__ == '__main__':

    # Valores padrão da aplicação
    width = LARGURA
    height = ALTURA
    x3d_file = "exemplo1.x3d"
    image_file = "tela.png"

    # Tratando entrada de parâmetro
    # parser para linha de comando
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-i", "--input", help="arquivo X3D de entrada")
    parser.add_argument("-o", "--output", help="arquivo 2D de saída (imagem)")
    parser.add_argument("-w", "--width", help="resolução horizonta", type=int)
    parser.add_argument("-h", "--height", help="resolução vertical", type=int)
    parser.add_argument(
        "-q", "--quiet", help="não exibe janela de visualização", action='store_true')
    args = parser.parse_args()  # parse the arguments
    if args.input:
        x3d_file = args.input
    if args.output:
        image_file = args.output
    if args.width:
        width = args.width
    if args.height:
        height = args.height

    # Iniciando simulação de GPU
    gpu.GPU(width, height, image_file)

    # Abre arquivo X3D
    scene = x3d.X3D(x3d_file)
    scene.set_resolution(width, height)

    # funções que irão fazer o rendering
    x3d.X3D.render["Polypoint2D"] = polypoint2D
    x3d.X3D.render["Polyline2D"] = polyline2D
    x3d.X3D.render["TriangleSet2D"] = triangleSet2D

    # Se no modo silencioso não configurar janela de visualização
    if not args.quiet:
        window = interface.Interface(width, height)
        scene.set_preview(window)

    scene.parse()  # faz o traversal no grafo de cena

    # Se no modo silencioso salvar imagem e não mostrar janela de visualização
    if args.quiet:
        gpu.GPU.save_image()  # Salva imagem em arquivo
    else:
        window.image_saver = gpu.GPU.save_image  # pasa a função para salvar imagens
        window.preview(gpu.GPU._frame_buffer)  # mostra janela de visualização
