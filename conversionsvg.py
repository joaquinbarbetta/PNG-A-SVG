import cv2
import svgwrite
import numpy as np

def jpg_to_svg(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print("Error: No se encuentra la imagen.")
        return

    # 1. Preprocesamiento básico
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # 2. Encontrar contornos Y jerarquía (quién está dentro de quién)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Configurar SVG
    height, width = img.shape[:2]
    dwg = svgwrite.Drawing(output_path, size=(width, height), profile='tiny')
    
    # --- LOGICA DE CAPAS ---
    # Creamos una lista con los datos de cada contorno para poder ordenarlos
    # Guardaremos: (Area, Contorno, Nivel_de_profundidad)
    shapes = []
    
    if hierarchy is not None:
        # hierarchy tiene forma [[[next, prev, child, parent], ...]]
        h_list = hierarchy[0]
        
        for i, contour in enumerate(contours):
            # Calcular "Profundidad": ¿Cuántos padres tiene este contorno?
            depth = 0
            current_parent = h_list[i][3]
            while current_parent != -1:
                depth += 1
                current_parent = h_list[current_parent][3]
            
            # Calcular Area (para dibujar los grandes primero)
            area = cv2.contourArea(contour)
            shapes.append((area, contour, depth))

    # 3. Ordenar: Dibujamos del más grande al más pequeño
    # Esto evita que un círculo negro tape a las letras blancas de adentro
    shapes.sort(key=lambda x: x[0], reverse=True)

    print(f"Procesando {len(shapes)} formas...")

    # 4. Dibujar
    for area, contour, depth in shapes:
        points = []
        for point in contour:
            x, y = point[0]
            points.append((int(x), int(y)))

        if len(points) > 2:
            # EL TRUCO:
            # Si el nivel es PAR (0, 2, 4...) -> Es Tinta (Negro)
            # Si el nivel es IMPAR (1, 3, 5...) -> Es Hueco (Blanco)
            if depth % 2 == 0:
                color = 'black'
            else:
                color = 'white'
            
            # stroke='none' para que no haya líneas, solo relleno puro
            dwg.add(dwg.polygon(points, fill=color, stroke='none'))

    dwg.save()
    print(f"¡Listo! Archivo con relleno guardado en: {output_path}")

if __name__ == "__main__":
    jpg_to_svg('logococa.png', 'salida_vectorizada2.svg')