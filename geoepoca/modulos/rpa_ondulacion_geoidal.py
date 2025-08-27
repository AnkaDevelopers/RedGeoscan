from geoepoca.modulos.buscar_img import buscar_y_click_en_set_imagenes
import pyautogui
import time


def ondulacion_geoidal():
    #***************************************************************************************
    # Data set de icono de conversion a ondulacion geoidal
    imagenes_conversion_ondulacion_geoidal = {
    r"C:\RedGeoscan\geoepoca\Imagenes\ondulacion-geoidal\1.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\ondulacion-geoidal\2.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\ondulacion-geoidal\3.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\ondulacion-geoidal\4.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\ondulacion-geoidal\5.PNG",
    }

    ancho, alto = pyautogui.size()  # Obtiene el tamaño de la pantalla
    pyautogui.moveTo(ancho / 2, alto / 2, duration=0.1)  # Mueve al centro en 0.1s
    time.sleep(0.5)
        
    # Buscar boton para el cambio de conversion y transformación.
    busqueda = buscar_y_click_en_set_imagenes(imagenes_conversion_ondulacion_geoidal, sensibilidad = 0.95)
        
    # segundo inteto busqueda de imagen
    if not busqueda:
        print("⚠ No se encontró el botón de conversion y transformación.")
            
        busqueda = buscar_y_click_en_set_imagenes(imagenes_conversion_ondulacion_geoidal, sensibilidad = 0.9)
            
        if not busqueda:
            busqueda = buscar_y_click_en_set_imagenes(imagenes_conversion_ondulacion_geoidal, sensibilidad = 0.8)
            if not busqueda:
                msj_depuracion = "❌ No se encontro el icono de conversion y transformación."
                print(msj_depuracion)
                return None, msj_depuracion
        
    #***************************************************************************************
    # Data set de icono de carga archivo ondulacion geoidal.
    imagenes_archivo_conversion_elipsoidal_decimal = {
    r"C:\RedGeoscan\geoepoca\Imagenes\archivo-ondulacion-geoidal\1.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\archivo-ondulacion-geoidal\2.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\archivo-ondulacion-geoidal\3.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\archivo-ondulacion-geoidal\4.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\archivo-ondulacion-geoidal\5.PNG",
    }
        
    # Buscar Boton para desplegar el formulario de carga archivo ondulacion geoidal.
    busqueda = buscar_y_click_en_set_imagenes(imagenes_archivo_conversion_elipsoidal_decimal, sensibilidad = 0.9)
        
    # segundo inteto busqueda de imagen
    if not busqueda:
        print("⚠ No se encontró el botón de archivo ondulacion geoidal..")
            
        busqueda = buscar_y_click_en_set_imagenes(imagenes_archivo_conversion_elipsoidal_decimal, sensibilidad = 0.9)
            
        if not busqueda:
            msj_depuracion = "❌ No se encontro el icono de archivo ondulacion geoidal."
            print(msj_depuracion)
            return None, msj_depuracion
        
    # inicio seleccionar carpeta
    #***************************************************************************************
    # Data set de icono de abrir
    imagen_btn_archivo ={
    r"C:\RedGeoscan\geoepoca\Imagenes\abrir\1.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\abrir\2.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\abrir\3.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\abrir\4.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\abrir\5.PNG",        
    }
    time.sleep(1)
    # Buscar boton abrir
    busqueda = buscar_y_click_en_set_imagenes(imagen_btn_archivo, sensibilidad = 0.9)
        
    # segundo inteto busqueda de boton abrir
    if not busqueda:
        print("⚠ No se encontró el boton abrir.")
            
        busqueda = buscar_y_click_en_set_imagenes(imagen_btn_archivo, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(imagen_btn_archivo, sensibilidad = 0.7)
            
            if not busqueda:
                msj_depuracion = "❌ No se encontro el boton abrir"
                print(msj_depuracion)
                return None, msj_depuracion
    print('boton archivo')
    #***************************************************************************************
    # Seleccionar Cargar equipo:
    # Data set de imagenes icno este equipo
    imagenes_equipo = {
    r"C:\RedGeoscan\geoepoca\Imagenes\este_equipo\1.png",
    r"C:\RedGeoscan\geoepoca\Imagenes\este_equipo\2.png",
    r"C:\RedGeoscan\geoepoca\Imagenes\este_equipo\3.png",
    r"C:\RedGeoscan\geoepoca\Imagenes\este_equipo\4.png",
    r"C:\RedGeoscan\geoepoca\Imagenes\este_equipo\5.png",
    r"C:\RedGeoscan\geoepoca\Imagenes\este_equipo\6.png",
    r"C:\RedGeoscan\geoepoca\Imagenes\este_equipo\7.png",
    r"C:\RedGeoscan\geoepoca\Imagenes\este_equipo\8.png",
    }
    time.sleep(1)
    # Buscar icono de este equipo
    busqueda = buscar_y_click_en_set_imagenes(imagenes_equipo, sensibilidad = 0.9)
        
    # segundo inteto busqueda de icono de este equipo
    if not busqueda:
        print("⚠ No se encontró el icono de este equipo.")
            
        busqueda = buscar_y_click_en_set_imagenes(imagenes_equipo, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(imagenes_equipo, sensibilidad = 0.7)
            
            if not busqueda:
                msj_depuracion = "❌ No se encontro el icono de este equipo"
                print(msj_depuracion)
                return None, msj_depuracion
        
    #***************************************************************************************
    # Data set de icono de carga archivo cambio de Epoca
    # Busqueda de icono disco local C
    time.sleep(1)
    imagenes_disco_local_c = {
    r"C:\RedGeoscan\geoepoca\Imagenes\disco_local_c\1.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\disco_local_c\2.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\disco_local_c\3.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\disco_local_c\4.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\disco_local_c\5.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\disco_local_c\6.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\disco_local_c\7.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\disco_local_c\8.PNG",
    }

    # Buscar Icono disco local C
    busqueda = buscar_y_click_en_set_imagenes(imagenes_disco_local_c, sensibilidad = 0.9)
        
    # segundo inteto busqueda de imagen
    if not busqueda:
        print("⚠ No se encontró el iono de disco local C.")
            
        busqueda = buscar_y_click_en_set_imagenes(imagenes_disco_local_c, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(imagenes_disco_local_c, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de disco local C"
                print(msj_depuracion)
                return None, msj_depuracion
    
        
    # Selección de Disco Local C
    pyautogui.press('enter')
    pyautogui.press('space')
    time.sleep(0.2) 
    # Seleccion de carpeta 0 - Geo Epoca
    pyautogui.press('space')
    pyautogui.press('enter')
    time.sleep(0.2) 
    # Selección de carpeta año actual 2018
    pyautogui.press('space')
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(0.2) 
    # Seleccion de archivo
    pyautogui.press('space')
    pyautogui.press('enter')
    time.sleep(0.2) 
    # Seleccion de columnas
    pyautogui.press('tab', presses= 3, interval=0.1)
    pyautogui.press('space')
    # Seleccion de tipo Coordenadas
    pyautogui.press('tab', presses=2, interval=0.1)
    pyautogui.press('down',presses=2, interval=0.1)
    pyautogui.press('tab', presses=16,interval=0.1)
    pyautogui.press('enter')
    # Selección de id
    pyautogui.press('tab', presses=2, interval=0.1)
    pyautogui.press('down')
        
    # seleccion de x
    pyautogui.press('tab')
    pyautogui.press('down', presses=2, interval=0.1)
        
    # seleccion de y
    pyautogui.press('tab')
    pyautogui.press('down', presses=3, interval=0.1)
    
    # seleccion de z
    pyautogui.press('tab')
    pyautogui.press('down', presses=4, interval=0.1)
    #***************************************************************************************
    # Seleccion ruta donde se guardara el excel en ELIPSOIDAL-DECIMAL
    pyautogui.press('tab', presses=4, interval=0.1)
    pyautogui.press('enter')
    #***************************************************************************************
    # Seleccionar Cargar equipo:
    # Data set de imagenes icno este equipo
    time.sleep(1)
    # Buscar icono de este equipo
    busqueda = buscar_y_click_en_set_imagenes(imagenes_equipo, sensibilidad = 0.9)
        
    # segundo inteto busqueda de icono de este equipo
    if not busqueda:
        print("⚠ No se encontró el icono de este equipo.")
            
        busqueda = buscar_y_click_en_set_imagenes(imagenes_equipo, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(imagenes_equipo, sensibilidad = 0.7)
            
            if not busqueda:
                msj_depuracion = "❌ No se encontro el icono de este equipo"
                print(msj_depuracion)
                return None, msj_depuracion
    
    # Buscar Icono disco local C
    busqueda = buscar_y_click_en_set_imagenes(imagenes_disco_local_c, sensibilidad = 0.9)
        
    # segundo inteto busqueda de imagen
    if not busqueda:
        print("⚠ No se encontró el iono de disco local C.")
            
        busqueda = buscar_y_click_en_set_imagenes(imagenes_disco_local_c, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(imagenes_disco_local_c, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de disco local C"
                print(msj_depuracion)
                return None, msj_depuracion


    # Selección de Disco Local C
    pyautogui.press('enter')
    pyautogui.press('space')
    time.sleep(0.1) 
    # Seleccion de carpeta 0 - Geo Epoca
    pyautogui.press('space')
    pyautogui.press('enter')
    time.sleep(0.1) 
    # Selección de carpeta 2018-elipsoidal-decimal
    pyautogui.press('space')
    pyautogui.press('down', presses=4, interval=0.1)
    pyautogui.press('enter')
    time.sleep(0.1) 
    # nombre del archivo
    pyautogui.press('tab')
    pyautogui.write('ondulacion-geoidal-2018')
    pyautogui.press('enter')
    # Guardar el archivo
    pyautogui.press('tab', presses=4, interval=0.1)
    time.sleep(0.5)
    pyautogui.press('enter')
    
    # Aceptar
    #***************************************************************************************
    # Data set de icono de aceptar
    time.sleep(1)
    imagenes_acptar = {
    r"C:\RedGeoscan\geoepoca\Imagenes\aceptar\1.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\aceptar\2.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\aceptar\3.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\aceptar\4.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\aceptar\5.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\aceptar\6.PNG",
    r"C:\RedGeoscan\geoepoca\Imagenes\aceptar\7.PNG",
    }

    # Buscar Icono boton aceptar
    busqueda = buscar_y_click_en_set_imagenes(imagenes_acptar, sensibilidad = 0.9)
        
    # segundo inteto busqueda de imagen
    if not busqueda:
        print("⚠ No se encontró el iono de boton aceptar.")
            
        busqueda = buscar_y_click_en_set_imagenes(imagenes_acptar, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(imagenes_acptar, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de boton aceptar"
                print(msj_depuracion)
                return None, msj_depuracion
      
    #***************************************************************************************
    msj = "✅ Archivo excel con conversion de 2018 a ondulacion geoidal"
    print(msj)
    return True, msj