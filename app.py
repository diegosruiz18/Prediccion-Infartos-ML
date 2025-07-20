#En este archivo se crea la interfaz de usuario para interactuar
#con el modelo de predicción de ataques cardíacos.

#This file creates the user interface to interact with
#the heart attack prediction model.

#Importar librerías
import gradio as gr
import joblib
import pandas as pd

#Cargar modelo
modelo = joblib.load("heart_attack_rf_model.pkl")

#Lista para opciones y codificar campos
#English
list_hipertension_en = ["No", "Yes"]
list_antecedentes_en = ["No", "Yes"]
list_edad_en = ["0-5", "6-11", "12-18", "19-25", "26-59", "60+"]
list_glucosa_en = ["Normal", "Prediabetes", "Diabetes"]
list_imc_en = ["Underweight", "Healthy weight", "Overweight", "Obesity"]
list_trabajo_en = ["Self-employed", "Private company", "Government", "Never worked", "Children care"]
#Español
list_hipertension_es = ["No", "Sí"]
list_antecedentes_es = ["No", "Sí"]
list_edad_es = ["0-5", "6-11", "12-18", "19-25", "26-59", "60+"]
list_glucosa_es = ["Normal", "Prediabetes", "Diabetes"]
list_imc_es = ["Peso bajo", "Peso saludable", "Sobrepeso", "Obesidad"]
list_trabajo_es = ["Emprendedor", "Empresa privada", "Gobierno", "Nunca trabajó", "Cuidar niños"]

#Etiquetas, opciones(choices) y campos codificados en ambos idiomas
dict_idiomas = {
    "English":{
        "labels":{
            "titulo": "# 🩺 Heart attack prediction",
            "descripcion": "#### 🎯 This application prioritizes the prediction of individuals at high risk of suffering a heart attack.",
            "hipertension": "Do you have hypertension?",
            "antecedentes": "Any history of heart disease?",
            "edad": "Age",
            "glucosa": "Glucose level",
            "imc": "BMI",
            "trabajo": "Type of work",
            "btn_pred": "Predict",
            "resultado_alto": "High risk of heart attack.",
            "resultado_bajo": "Low risk of heart attack.",
            "prediccion": "Prediction result"
        },
        "choices":{
            "hipertension": list_hipertension_en[::-1],
            "antecedentes": list_antecedentes_en[::-1],
            "edad": list_edad_en,
            "glucosa": list_glucosa_en,
            "imc": list_imc_en,
            "trabajo": list_trabajo_en
        },
        "encoded":{
            "hipertension": {value: i for i,value in enumerate(list_hipertension_en)},
            "antecedentes": {value: i for i,value in enumerate(list_antecedentes_en)},
            "edad": {value: (i+1) for i, value in enumerate(list_edad_en)},
            "glucosa": {value: (i+1) for i, value in enumerate(list_glucosa_en)},
            "imc": {value: (i+1) for i, value in enumerate(list_imc_en)},
            "trabajo": {value: (i+1) for i, value in enumerate(list_trabajo_en)}
        }
    },
    "Español":{
        "labels":{
            "titulo": "# 🩺 Predicción de ataques cardíacos",
            "descripcion": "#### 🎯 Esta aplicación prioriza la predicción de personas en alto riesgo de sufrir un ataque cardíaco.",
            "hipertension": "¿Tiene hipertensión?",
            "antecedentes": "¿Antecedentes de enfermedad cardíaca?",
            "edad": "Edad",
            "glucosa": "Nivel de glucosa",
            "imc": "IMC",
            "trabajo": "Tipo de trabajo",
            "btn_pred": "Predecir",
            "resultado_alto": "Alto riesgo de ataque cardíaco.",
            "resultado_bajo": "Bajo riesgo de ataque cardíaco.",
            "prediccion": "Resultado de predicción"
        },
        "choices":{
            "hipertension": list_hipertension_es[::-1],
            "antecedentes": list_antecedentes_es[::-1],
            "edad": list_edad_es,
            "glucosa": list_glucosa_es,
            "imc": list_imc_es,
            "trabajo": list_trabajo_es
        },
        "encoded":{
            "hipertension": {value: i for i,value in enumerate(list_hipertension_es)},
            "antecedentes": {value: i for i,value in enumerate(list_antecedentes_es)},
            "edad": {value: (i+1) for i, value in enumerate(list_edad_es)},
            "glucosa": {value: (i+1) for i, value in enumerate(list_glucosa_es)},
            "imc": {value: (i+1) for i, value in enumerate(list_imc_es)},
            "trabajo": {value: (i+1) for i, value in enumerate(list_trabajo_es)}
        }
    }
}

#Función para predicción de ataques cardíacos
def heart_attack_prediction(h, a, e, g, i, t, idioma):
    #Validación de nulos
    if (h is None or h == "") or (a is None or a == ""):
        gr.Warning("Please fill in all the fields." if idioma == "English" else "Por favor complete todos los campos.")
        return ""

    #Datos para predicción
    encoded_options = dict_idiomas[idioma]["encoded"]
    df = pd.DataFrame({
        "Flag_hipertension": [encoded_options["hipertension"][h]],
        "Flag_problem_cardiaco": [encoded_options["antecedentes"][a]],
        "Edad_Encoded": [encoded_options["edad"][e]],
        "Glucosa_Encoded": [encoded_options["glucosa"][g]],
        "IMC_Encoded": [encoded_options["imc"][i]],
        "TipoTrabajo_Encoded": [encoded_options["trabajo"][t]]
    })

    #Predicción
    pred = modelo.predict(df)[0]

    label = dict_idiomas[idioma]["labels"]
    return f"🔴⚠️ {label['resultado_alto']}" if pred == 1 else f"🟢👍 {label['resultado_bajo']}"

#Función para actualizar interfaz
def update_labels(idioma):
    opts = dict_idiomas[idioma]
    return (
        gr.update(value=opts["labels"]["titulo"]),
        gr.update(value=opts["labels"]["descripcion"]),
        gr.update(label=opts["labels"]["hipertension"], choices=opts["choices"]["hipertension"], value=None),
        gr.update(label=opts["labels"]["antecedentes"], choices=opts["choices"]["antecedentes"], value=None),
        gr.update(label=opts["labels"]["edad"], choices=opts["choices"]["edad"], value=opts["choices"]["edad"][0]),
        gr.update(label=opts["labels"]["glucosa"], choices=opts["choices"]["glucosa"], value=opts["choices"]["glucosa"][0]),
        gr.update(label=opts["labels"]["imc"], choices=opts["choices"]["imc"], value=opts["choices"]["imc"][0]),
        gr.update(label=opts["labels"]["trabajo"], choices=opts["choices"]["trabajo"], value=opts["choices"]["trabajo"][0]),
        gr.update(value=opts["labels"]["btn_pred"]),
        gr.update(label=opts["labels"]["prediccion"], value=None)
    )

#Interfaz
with gr.Blocks(theme=gr.themes.Ocean()) as dashboard:
    #Configuración de estilos
    gr.HTML("""
        <style>
            .svelte-1hfxrpf, .svelte-g2oxp3, .svelte-1bx8sav {
                font-size: 13px !important;         /* Tamaño más pequeño */
            }
            .app.svelte-1px0ac9.svelte-1px0ac9 {
                padding-top: 16px;
                margin-top: 0px;
            }
            #component-1{
                display: none;
            }
        </style>
        """)

    #Título
    titulo = gr.Markdown(dict_idiomas["English"]["labels"]["titulo"])
    descripcion = gr.Markdown(dict_idiomas["English"]["labels"]["descripcion"])

    #Idiomas
    idioma = gr.Radio(["English", "Español"], value="English", label="🌐 Language / Idioma")

    #Formulario
    with gr.Row():
        with gr.Column(scale=4):
            with gr.Row():
                #Radiobuttons
                h = gr.Radio(choices=dict_idiomas["English"]["choices"]["hipertension"],
                             label=dict_idiomas["English"]["labels"]["hipertension"])
                a = gr.Radio(choices=dict_idiomas["English"]["choices"]["antecedentes"],
                             label=dict_idiomas["English"]["labels"]["antecedentes"])
            #Dropdown
            e = gr.Dropdown(choices=dict_idiomas["English"]["choices"]["edad"],
                            label=dict_idiomas["English"]["labels"]["edad"])
            with gr.Row():
                g = gr.Dropdown(choices=dict_idiomas["English"]["choices"]["glucosa"],
                                label=dict_idiomas["English"]["labels"]["glucosa"])
                i = gr.Dropdown(choices=dict_idiomas["English"]["choices"]["imc"],
                                label=dict_idiomas["English"]["labels"]["imc"])

            t = gr.Dropdown(choices=dict_idiomas["English"]["choices"]["trabajo"],
                            label=dict_idiomas["English"]["labels"]["trabajo"])
            #Botón
            btn = gr.Button(value=dict_idiomas["English"]["labels"]["btn_pred"])
        with gr.Column(scale=5):
            #Resultado
            resultado = gr.Textbox(label=dict_idiomas["English"]["labels"]["prediccion"])

    #Predicción
    btn.click(fn=heart_attack_prediction, inputs=[h, a, e, g, i, t, idioma], outputs=resultado)

    #Cambiar idioma
    idioma.change(fn=update_labels, inputs=[idioma], outputs=[titulo, descripcion, h, a, e, g, i, t, btn, resultado])

#Ejecutar app
if __name__ == '__main__':
    dashboard.launch()