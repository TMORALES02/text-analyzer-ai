import sys
from openai import OpenAI

client = OpenAI()

def main():
    try:
        with open("texto.txt", encoding="utf-8") as file:
            reader = file.read()
    except FileNotFoundError:
        sys.exit("el archivo no existe")
    

    if not reader.strip():
        sys.exit("el archivo esta vacio")


    palabras = cant_palabras(reader)
    frases = cant_frases(reader)
    caracteres = cant_caracteres(reader)
    palabra, cantidad = palabra_mas_repetida(reader)
    resumen = resumen_ia(reader)
        
    print(f"la cantidad de palabras es {palabras}")
    print(f"la cantidad de frases es {frases}")
    print(f"la cantidad de caracteres es {caracteres}")
    print(f"la palabra mas repetida es {palabra} y aparece {cantidad} veces")
    print(f"resumen de texto:{resumen}")

    with open("resultado.txt", "w", encoding="utf-8") as file:
        file.write(f"la cantidad de palabras es {palabras}\n")
        file.write(f"la cantidad de frases es {frases}\n")
        file.write(f"la cantidad de caracteres es {caracteres}\n")
        file.write(f"la palabra mas repetida es {palabra} y aparece {cantidad} veces\n")
        file.write(f"\nResumen:\n {resumen}\n")



def limpiar_texto(texto):
    import string
    texto = texto.lower()
    for signo in string.punctuation:
        texto = texto.replace(signo, "")
    return texto

def cant_palabras (texto):
    texto = limpiar_texto(texto)
    return len(texto.split())


def cant_frases(texto):
    return texto.count(".") + texto.count("!") + texto.count("?")


def cant_caracteres(texto):
    return len(texto)


def palabra_mas_repetida(texto):
    import string

    conteo = {}
    texto = limpiar_texto(texto)

    palabras = texto.split()

    for palabra in palabras:
        if palabra in conteo:
            conteo[palabra] += 1
        else:
            conteo[palabra] = 1

    palabra_rep = ""
    cant_max = 0

    for palabra,cantidad in conteo.items():
        if cantidad > cant_max:
            cant_max = cantidad
            palabra_rep = palabra        

    return palabra_rep, cant_max

def get_completion(prompt):      
    response = client.responses.create(
        model = "gpt-4.1-mini" ,
        input = prompt
    )
    return response.output[0].content[0].text

def resumen_ia(texto):
    prompt = f"""
    Quiero que generes un resumen de unas 5 oraciones del siguiente texto
     condiciones:
      -1 sola oracion por cada linea de codigo
      -cada oracion debe terminar con un salto de linea
      -formato claro y legible, no escribas todo en un solo parrafo
        texto:{texto}"""
    response = get_completion(prompt)
    return response









if __name__ == "__main__":
    main()