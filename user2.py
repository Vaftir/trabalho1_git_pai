
import PySimpleGUI as sg
import cv2 as cv
import io
import os.path
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


global aux
sg.theme("DarkTeal2")

file_types= [
    ("JPEG (*.jpg)","*.jpg"),
    ("PNG (*.png)","*.png"),
    ("Todos os arquivos","*.*")
]


x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropping = False    
'''
Requerimentos:
    pip install Pillow
    pip install opencv-contrib-python
    pip install matplotlib
imageCut - > def para corte da imagem (a imagem recortada é salva como cropped.jpg
                                        na pasta photos do projeto)
                                        OBS: o imageCut é um método pronto
            parametros:
                x e y -> posiçoes do mouse
                event -> evento para clique do mouse
                flags -> flag base para setMouseCallback
                param -> argumento para setMouseCallback
'''
def imageCut(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
    
    # Evento referente ao lique do mause
    if event == cv.EVENT_LBUTTONDOWN: 
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    
    elif event == cv.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
   
    elif event == cv.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2:
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv.imshow("corte", roi)
            cv.imwrite(f'photos/cropped.jpg', roi)
'''
Primeira página -> menu
'''
def menu_window():
    sg.theme("DarkTeal2")
    menu_layout = [
        [sg.Text('Trabalho parte 1', font=('Verdana', 16), text_color='#ffffff')],
        [sg.Text('_'*30, text_color='#ffffff')],
        [sg.Button('Carregar arquivo', font=('Verdana', 12))],
        [sg.Button('Correlação', font=('Verdana', 12))],
        [sg.Button('Sair', font=('Verdana', 12), button_color='#eb4034')]
    ]
    menu_window = sg.Window('Menu', menu_layout, element_justification='c')
    while True:
        event, values = menu_window.read()
        if event == 'Sair' or event == sg.WIN_CLOSED:
            break
        elif event == 'Carregar arquivo':
            menu_window.close()
            view_img_window()
        elif event == 'Correlação':
            menu_window.close()
            correlacao_window()
    menu_window.close()
'''
Segunda página
'''
def view_img_window(): 
    sg.theme("DarkTeal2")
    '''
        Layout do menu
    '''
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image file"),
            sg.Input(size=(25,1), key= "-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Submit"),
            sg.Button("Cortar imagem"),
            sg.Button("Menu"),
            
        ]
    ]
    img_view_window = sg.Window("Visualizador de imagens", layout)
    '''
    Loop para rodar a aplicação da segunda página
    '''
    while True: 
        event, values = img_view_window.read()
        if event == sg.WIN_CLOSED or event=="Exit": #Evento para fechar a aplicação
            break
        elif event == "Submit": #Botão submit que mostra o template da imagem
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((500,500))
                bio = io.BytesIO()
                aux = image.save(bio,format="PNG")
                image.save(bio,format="PNG")
                img_view_window["-IMAGE-"].update(data=bio.getvalue())
        elif event == "Cortar imagem": #Botão que libera pra cortar a imagem
                filename = values["-FILE-"]
                img = cv.imread(filename)
                imS = cv.resize(img, (960, 540))
                img = imS

                cv.namedWindow(filename)
                cv.setMouseCallback(filename, imageCut) #Chama imagemcut para cortar com o mouse
                
                global oriImage
                oriImage = img.copy()
                if not cropping: #Mostra a imagem sem corte
                    cv.imshow(filename, oriImage)
                if cropping:
                    cv.rectangle(oriImage, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2) #mostra a imagem cortada
        elif event == "Menu": #Volta pro menu
            img_view_window.close()
            menu_window()
            
    img_view_window.close()


'''
Terceira página
'''
def correlacao_window():
    sg.theme("DarkTeal2")
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Imagem A"),
            sg.Input(size=(25,1), key= "-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Submit"),
        ],
        [sg.Image(key="-IMAGE2-")],
        [
            sg.Text("Imagem B"),
            sg.Input(size=(25,1), key= "-FILE2-"),
            sg.FileBrowse(file_types=file_types,initial_folder='photos'),
            sg.Button("Submit Crop"),
        ],
        [sg.Button("Menu")]
    ]
    correlacao_window = sg.Window("Correlação", layout)
    '''
    Loop da aplicação da terceira página
    '''
    while True: 
       event, values = correlacao_window.read()
       if event == sg.WIN_CLOSED or event=="Exit": #Evento para fechar a aplicação
            break
       elif (event == "Submit") and (values["-FILE-"]): #Botão submit que mostra o template da imagem
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((500,500))
                bio = io.BytesIO()
                aux = image.save(bio,format="PNG")
                image.save(bio,format="PNG")
                correlacao_window["-IMAGE-"].update(data=bio.getvalue())
       elif (event == "Submit Crop") and (values["-FILE2-"]): #Botão submit que mostra o template da imagem
            filename = values["-FILE2-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE2-"])
                image.thumbnail((500,500))
                bio = io.BytesIO()
                image.save(bio,format="PNG")
                correlacao_window["-IMAGE2-"].update(data=bio.getvalue()) 
       elif event == "Menu": #Volta pro menu
            correlacao_window.close()
            menu_window()

def main():
    menu_window()
    
if __name__ == '__main__':
    main()