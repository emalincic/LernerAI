import streamlit as st
from groq import Groq

def configurar_pagina():
    st.title("LernerAI")
    st.sidebar.title("Configuración de la IA")
    elegirModelo =  st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

MODELOS = [
    'llama3-8b-8192',
    'llama3-70b-8192',
    'mixtral-8x7b-32768'
]

# 3. espacio en la interfaz

def area_chat():
    contenedorDelChat = st.container(height=700, border=False)
    with contenedorDelChat:
        mostrar_historial()

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
    model=modelo,
    messages=[{"role": "user", "content": mensajeDeEntrada}],
    stream=True
)

mensajes = []

# 1. actualizar historial
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({
        "role": rol,
        "content": contenido,
        "avatar": avatar
    })

# 2. mostrar historial 
def mostrar_historial():
    for mensaje in st.session_state.mensajes: # bucle
        with st.chat_message(mensaje["role"]): # burbuja
            st.markdown(mensaje["content"]) # texto

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
        yield frase.choices[0].delta.content 
        # - mostrar el CONTENIDO de la variable a demanda
    return respuesta_completa # return / funciones - mostrar la variable en sí


# def main():
#     modelo = configurar_pagina()
#     clienteUsuario = crear_usuario_groq()
#     inicializar_estado()
#     area_chat()
#     mensaje = st.chat_input("Escribí tu mensaje")
#     print(mensaje)
#     if mensaje:
#         actualizar_historial("user", mensaje, "🙂")
#         chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
#         if chat_completo:
#             with st.chat_message("assistant"):
#                 respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
#                 actualizar_historial("assistant", chat_completo,"🤖")
#         st.rerun()
        
def main():
    modelo = configurar_pagina()

    clienteUsuario = crear_usuario_groq()
    inicializar_estado()

    mensaje = st.chat_input("Escribí tu mensaje: ")
    print(mensaje)

    area_chat()
    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")

        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa[0],"🤖")

        st.rerun()

if __name__ == "__main__":
    main()



