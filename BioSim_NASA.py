# Unificación de datos y aplicación Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_daq as daq
import os
import random

# --- Diccionario de pioneros con relación a la NASA y sus imágenes ---
pioneros_nasa = {
    'Franklin Chang-Díaz (Costa Rica)': {
        'historia': 'Astronauta de la NASA. Voló en 7 misiones espaciales. Fundador de Ad Astra Rocket Company.',
        'imagen': 'franklin_chang_diaz.jpg'
    },
    'Rodolfo Neri Vela (México)': {
        'historia': 'Voló en la misión STS-61-B del transbordador Atlantis en 1985.',
        'imagen': 'rodolfo_neri_vela.jpg'
    },
    'Carlos Noriega (Perú)': {
        'historia': 'Astronauta de la NASA. Voló en STS-84 y STS-97.',
        'imagen': 'carlos_noriega.jpg'
    },
    'Kalpana Chawla (India)': {
        'historia': 'Astronauta de la NASA. Falleció en el accidente del transbordador Columbia.',
        'imagen': 'kalpana_chawla.jpg'
    },
    'Pablo de León (Argentina)': {
        'historia': 'Ingeniero aeroespacial. Colaborador en el diseño de trajes espaciales y hábitats con la NASA.',
        'imagen': 'pablo_de_leon.jpg'
    },
    'Noel de Castro (Argentina)': {
        'historia': 'En entrenamiento para futuras misiones. Con un vínculo directo a programas educativos y simulaciones de la NASA.',
        'imagen': 'noel_de_castro.jpg'
    },
    'Marc Garneau (Canadá)': {
        'historia': 'Primer astronauta canadiense. Voló en STS-41-G y otras misiones con la NASA.',
        'imagen': 'marc_garneau.jpg'
    },
    'Roberta Bondar (Canadá)': {
        'historia': 'Primera mujer canadiense en el espacio. Voló en STS-42. Colaboración directa con la NASA.',
        'imagen': 'roberta_bondar.jpg'
    },
    'Jean-Loup Chrétien (Francia)': {
        'historia': 'Voló en STS-86 con la NASA. Participó en caminatas espaciales.',
        'imagen': 'jean_loup_chretien.jpg'
    },
    'Claudie Haigneré (Francia)': {
        'historia': 'Voló en STS-93 con la NASA. Médica y científica.',
        'imagen': 'claudie_haignere.jpg'
    },
    'Heidemarie Stefanyshyn-Piper (Alemania/EE.UU.)': {
        'historia': 'Astronauta de la NASA. Voló en STS-115 y STS-126.',
        'imagen': 'heidemarie_stefanishyn_piper.jpg'
    },
    'Chiaki Mukai (Japón)': {
        'historia': 'Voló en STS-65 y STS-95 con la NASA. Investigadora médica.',
        'imagen': 'chiaki_mukai.jpg'
    },
    'Alan Shepard (EE.UU.)': {
        'historia': 'Primer astronauta estadounidense. Voló en Mercury-Redstone 3 y Apollo 14.',
        'imagen': 'alan_shepard.jpg'
    },
    'Sally Ride (EE.UU.)': {
        'historia': 'Primera mujer estadounidense en el espacio. Voló en STS-7 y STS-41-G.',
        'imagen': 'sally_ride.jpg'
    },
    'Ana Mosquera (Uruguay)': {
        'historia': 'Ingeniera uruguaya con participación en proyectos vinculados a misiones lunares.',
        'imagen': 'ana_mosquera.jpg'
    },
}

# --- Datos de los Sujetos y Glosario ---
# Diccionario para almacenar el estado de la simulación
sim_data = {
    'dias': [0],
    'salud': [100],
    'densidad_osea': [100],
    'bitacora': ["Misión iniciada. Se observan datos iniciales y se espera su evolución."]
}

# Diccionario de sujetos con sus datos y descripciones
sujetos_data = {
    'astronauta': {
        'nombre': 'Noel de Castro (Argentina)',
        'imagen': '/assets/astronauta_mision.jpg',
        'historia': 'Noel de Castro es una astronauta argentina. Con su estricta rutina de ejercicios, ella luchará contra los efectos de la microgravedad y la radiación. ¿Podrá mantenerse sana?',
        'descripcion_ia': 'El cuerpo de Noel de Castro se ajusta a la microgravedad. El sistema circulatorio se redistribuye, y los fluidos se desplazan hacia la parte superior del cuerpo. A nivel celular, las mitocondrias, responsables de la energía, se adaptan a la nueva demanda metabólica.',
        'bitacora_evolucion': [
            "Día 1: **Aclimatación y adaptación.** El cuerpo de Noel de Castro se ajusta a la microgravedad. El sistema circulatorio se redistribuye, y los fluidos se desplazan hacia la parte superior del cuerpo. A nivel celular, las mitocondrias, responsables de la energía, se adaptan a la nueva demanda metabólica.",
            "Día 2: No hay eventos notables, todo parece normal.",
            "Día 3: Noel completa su primer ciclo de ejercicios. Los músculos de las piernas y la columna, que en la Tierra se usan para mantener la postura contra la gravedad, comienzan a atrofiarse. La salud se mantiene estable, pero la densidad ósea tiene una ligera disminución.",
            "Día 4: Se registra una pequeña fluctuación en la salud, posiblemente debido a un ajuste en la ingesta de calorías. La bitácora registra: 'Hoy siento menos hambre y tengo la sensación de estar flotando constantemente'.",
            "Día 5: La densidad ósea de los huesos largos (fémur y tibia) comienza a mostrar una reducción más marcada. Noel aumenta la duración de sus sesiones de ejercicio para contrarrestar este efecto. La salud se mantiene en buen estado.",
            "Día 6: Se ha detectado un aumento en el nivel de radiación cósmica. Noel debe pasar más tiempo en las zonas protegidas de la estación. Esto reduce el tiempo dedicado a ejercicios, afectando la densidad ósea.",
            "Día 7: Los análisis de sangre muestran una ligera disminución en el recuento de glóbulos rojos. Este es un efecto común de la vida en el espacio. El cuerpo de Noel se adapta para vivir con menos de estas células, optimizando su función en microgravedad.",
            "Día 8: Noel se queja de un ligero dolor en los tobillos, debido a la falta de presión en las articulaciones. Su salud general es estable, pero la densidad ósea sigue descendiendo. La bitácora registra: 'Se extrañan las caminatas'.",
            "Día 9: El nivel de radiación ha vuelto a la normalidad. Noel vuelve a su rutina de ejercicios completa. La densidad ósea se ha estabilizado. La salud se recupera gracias a una dieta rica en calcio y vitamina D.",
            "Día 10: La salud de Noel está en buen estado, y los análisis muestran que su cuerpo se está adaptando al nuevo entorno. La densidad ósea se mantiene estable. La bitácora registra: 'Hoy todo parece más fácil. Me siento cómoda en mi nuevo hogar'.",
            "Día 11: Se produce un pequeño error en el sistema de purificación de aire, lo que afecta la calidad del oxígeno. Esto provoca un descenso de la salud. Noel y la tripulación trabajan para resolver el problema.",
            "Día 12: El sistema de purificación de aire ha sido reparado. La salud de Noel comienza a recuperarse lentamente. Los ejercicios de resistencia continúan, lo que ayuda a frenar la pérdida de densidad ósea.",
            "Día 13: Noel utiliza el sistema de bicicleta estática de la estación para una sesión de 2 horas. El simulador de gravedad artificial ayuda a reducir la pérdida ósea.",
            "Día 14: La salud se recupera completamente. La densidad ósea se ha estabilizado. Noel y la tripulación realizan una inspección de rutina de la nave.",
            "Día 15: La mitad de la misión ha sido completada. Noel celebra junto a sus compañeros. Los análisis muestran que el cuerpo se ha adaptado. La densidad ósea se mantiene estable.",
            "Día 16: Se observa un aumento en el nivel de radiación cósmica. La tripulación reduce las actividades fuera de las zonas protegidas. La exposición a la radiación tiene un ligero impacto en la salud.",
            "Día 17: La densidad ósea comienza a disminuir de nuevo debido a la falta de ejercicios. La tripulación se mantiene en zonas de protección.",
            "Día 18: Noel sigue en las zonas de protección. La bitácora registra: 'El cansancio es notable. La falta de ejercicios me hace sentir débil'. La salud disminuye lentamente.",
            "Día 19: El nivel de radiación cósmica ha vuelto a la normalidad. La tripulación vuelve a su rutina normal. Noel se enfoca en recuperar su salud con ejercicios cardiovasculares y de resistencia.",
            "Día 20: La salud se ha recuperado considerablemente. La densidad ósea ha mejorado ligeramente. La bitacora registra: 'El cuerpo es una máquina de adaptación. Estoy impresionada de lo que podemos lograr'.",
            "Día 21: Los análisis de sangre muestran que el recuento de glóbulos rojos se ha estabilizado. La salud y la densidad ósea se mantienen estables.",
            "Día 22: Un pequeño meteorito impacta cerca de la estación, lo que provoca una fluctuación en los sistemas de soporte vital. La salud de Noel disminuye ligeramente.",
            "Día 23: Los sistemas de soporte vital han sido reparados. Noel se recupera. La bitácora registra: 'Hoy tuvimos un susto. La resiliencia de la tripulación es nuestra mayor fortaleza'.",
            "Día 24: La densidad ósea se ha mantenido estable. La salud de Noel está en buen estado. Continúa con su rutina de ejercicios.",
            "Día 25: Se registra una ligera disminución en la ingesta de calcio. La densidad ósea disminuye lentamente. Noel se queja de un ligero dolor en las articulaciones.",
            "Día 26: El equipo de nutrición aumenta el nivel de calcio y vitamina D en la dieta de Noel. La densidad ósea se estabiliza. La salud se mantiene estable.",
            "Día 27: Noel realiza ejercicios de resistencia intensivos para fortalecer sus huesos. La bitácora registra: 'Cada día que pasa, me siento más fuerte y preparada para el regreso'.",
            "Día 28: La densidad ósea ha mejorado ligeramente. La salud se mantiene estable. Noel y la tripulación se preparan para el regreso a la Tierra.",
            "Día 29: Los análisis finales muestran que el cuerpo de Noel se ha adaptado a la microgravedad. La densidad ósea se ha estabilizado y la salud está en excelente estado. La bitácora registra: 'La misión ha sido un éxito. El conocimiento adquirido nos ayudará a llegar más lejos'.",
            "Día 30: **Misión completada. Recuperación.** La misión ha finalizado con éxito. El cuerpo de Noel de Castro está comprometido, pero los datos genéticos y celulares recopilados son invaluables. Se enfrentará a un riguroso programa de rehabilitación para recuperar la fuerza muscular y la densidad ósea perdidas, un proceso que puede durar varios meses. Su caso es un modelo de estudio para futuras misiones a Marte."
        ]
    },
    'mono_juan': {
        'nombre': 'Mono Juan (Argentina)',
        'imagen': '/assets/mono_juan.jpg',
        'historia': 'Juan es un pionero de la biología espacial. Fue parte de la misión argentina Canopus I en 1967. Su simulación nos muestra los efectos en un ser vivo sin ejercicio. ¿Sobrevivirá al aterrizaje?',
        'descripcion_ia': 'El mono Juan es un pionero en la biología espacial. Fue parte de la misión argentina Canopus I en 1967. Su simulación nos muestra los efectos en un ser vivo sin ejercicio. ¿Sobrevivirá al aterrizaje?',
        'bitacora_evolucion': [
            "Día 1: **Adaptación inicial.** Juan se muestra inquieto, pero estable. Su cuerpo, sin el estímulo de la gravedad, ya comienza a movilizar el calcio de sus huesos. A nivel de tejido, las células óseas se reorganizan, y las fibras de colágeno pierden su rigidez. A diferencia de un humano, no puede realizar ejercicios para contrarrestar este efecto.",
            "Día 2: La densidad ósea del mono Juan continúa disminuyendo a un ritmo acelerado. Su estado de salud se mantiene estable, pero muestra signos de estrés, como un aumento del ritmo cardíaco. La bitácora registra: 'Se ha notado una disminución del apetito'.",
            "Día 3: El simulador de gravedad artificial ha fallado. La densidad ósea del mono Juan continúa su descenso. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la masa muscular'.",
            "Día 4: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye más rápido. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 5: El simulador de gravedad artificial ha sido reparado. La densidad ósea del mono Juan se ha estabilizado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado un aumento de la masa muscular'.",
            "Día 6: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 7: La densidad ósea del mono Juan continúa disminuyendo a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la masa muscular'.",
            "Día 8: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 9: El simulador de gravedad artificial ha sido reparado. La densidad ósea del mono Juan se ha estabilizado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado un aumento de la masa muscular'.",
            "Día 10: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 11: La densidad ósea del mono Juan continúa disminuyendo a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la masa muscular'.",
            "Día 12: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 13: El simulador de gravedad artificial ha sido reparado. La densidad ósea del mono Juan se ha estabilizado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado un aumento de la masa muscular'.",
            "Día 14: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 15: La densidad ósea del mono Juan continúa disminuyendo a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la masa muscular'.",
            "Día 16: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 17: El simulador de gravedad artificial ha sido reparado. La densidad ósea del mono Juan se ha estabilizado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado un aumento de la masa muscular'.",
            "Día 18: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 19: La densidad ósea del mono Juan continúa disminuyendo a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la masa muscular'.",
            "Día 20: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 21: El simulador de gravedad artificial ha sido reparado. La densidad ósea del mono Juan se ha estabilizado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado un aumento de la masa muscular'.",
            "Día 22: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 23: La densidad ósea del mono Juan continúa disminuyendo a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la masa muscular'.",
            "Día 24: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 25: El simulador de gravedad artificial ha sido reparado. La densidad ósea del mono Juan se ha estabilizado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado un aumento de la masa muscular'.",
            "Día 26: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 27: La densidad ósea del mono Juan continúa disminuyendo a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la masa muscular'.",
            "Día 28: Se ha detectado un aumento en el nivel de radiación cósmica. La densidad ósea del mono Juan disminuye. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la fuerza física'.",
            "Día 29: El simulador de gravedad artificial ha sido reparado. La densidad ósea del mono Juan se ha estabilizado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado un aumento de la masa muscular'.",
            "Día 30: **Misión completada. Recuperación.** La misión ha finalizado con éxito. El cuerpo de Juan está comprometido, pero los datos genéticos y celulares recopilados son invaluables. Se enfrentará a un riguroso programa de rehabilitación para recuperar la fuerza muscular y la densidad ósea perdidas, un proceso que puede durar varios meses. Su caso es un modelo de estudio para futuras misiones a Marte."
        ]
    },
    'planta': {
        'nombre': 'Planta',
        'imagen': '/assets/planta.jpg',
        'historia': 'Esta planta es un experimento para ver cómo la vida vegetal se adapta a la microgravedad. ¿Cómo afectará la ausencia de gravedad a su crecimiento? ¿Podrá sobrevivir sin la luz del sol?',
        'descripcion_ia': 'La planta se adapta a un entorno sin gravedad. Sus raíces, que en la Tierra crecen hacia abajo, ahora se orientan de manera aleatoria, demostrando la ausencia de gravitropismo. Las células de las raíces usan los amiloplastos para detectar la dirección, pero la microgravedad los desorienta.',
        'bitacora_evolucion': [
            "Día 1: **Desafío a la gravedad.** La planta se adapta a un entorno sin gravedad. Sus raíces, que en la Tierra crecen hacia abajo, ahora se orientan de manera aleatoria, demostrando la ausencia de gravitropismo. Las células de las raíces usan los amiloplastos para detectar la dirección, pero la microgravedad los desorienta.",
            "Día 2: Se registra un crecimiento anormal de las hojas y el tallo. Las células de la planta, que en la Tierra se usan para mantener la postura contra la gravedad, comienzan a desorganizarse. La salud se mantiene estable, pero la densidad ósea tiene una ligera disminución.",
            "Día 3: La planta comienza a mostrar signos de estrés, como un cambio en el color de las hojas y una disminución en la producción de oxígeno. El simulador de gravedad artificial ha fallado. La densidad ósea de la planta continúa su descenso.",
            "Día 4: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 5: El simulador de gravedad artificial ha sido reparado. La densidad ósea de la planta se ha estabilizado. La salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 6: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 7: La planta continúa mostrando signos de estrés. La densidad ósea disminuye a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 8: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 9: El simulador de gravedad artificial ha sido reparado. La densidad ósea de la planta se ha estabilizado. La salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 10: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 11: La planta continúa mostrando signos de estrés. La densidad ósea disminuye a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 12: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 13: El simulador de gravedad artificial ha sido reparado. La densidad ósea de la planta se ha estabilizado. La salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 14: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 15: La planta continúa mostrando signos de estrés. La densidad ósea disminuye a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 16: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 17: El simulador de gravedad artificial ha sido reparado. La densidad ósea de la planta se ha estabilizado. La salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 18: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 19: La planta continúa mostrando signos de estrés. La densidad ósea disminuye a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 20: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 21: El simulador de gravedad artificial ha sido reparado. La densidad ósea de la planta se ha estabilizado. La salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 22: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 23: La planta continúa mostrando signos de estrés. La densidad ósea disminuye a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 24: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 25: El simulador de gravedad artificial ha sido reparado. La densidad ósea de la planta se ha estabilizado. La salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 26: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 27: La planta continúa mostrando signos de estrés. La densidad ósea disminuye a un ritmo acelerado. El estado de salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 28: Se ha detectado un aumento en el nivel de radiación cósmica. La planta se expone a altos niveles de radiación, lo que afecta su salud y la densidad ósea. La bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 29: El simulador de gravedad artificial ha sido reparado. La densidad ósea de la planta se ha estabilizado. La salud se mantiene estable, pero la bitácora registra: 'Se ha notado una disminución de la producción de oxígeno'.",
            "Día 30: **Misión completada. Recuperación.** La misión ha finalizado con éxito. El cuerpo de la planta está comprometido, pero los datos genéticos y celulares recopilados son invaluables. Se enfrentará a un riguroso programa de rehabilitación para recuperar la fuerza muscular y la densidad ósea perdidas, un proceso que puede durar varios meses. Su caso es un modelo de estudio para futuras misiones a Marte."
        ]
    }
}

# Datos del glosario
glosario_data = {
    'Densidad ósea': 'Cantidad de masa ósea por metro cuadrado. En el espacio, la falta de gravedad y el ejercicio adecuado puede causar una reducción significativa, haciendo que los huesos se vuelvan frágiles.',
    'Microgravedad': 'Es el estado de "caída libre" constante. En este estado, los cuerpos flotan, lo que afecta a los músculos, los huesos, el sistema cardiovascular y la percepción del equilibrio.',
    'Radiación Cósmica': 'Partículas de alta energía provenientes del Sol y del espacio profundo. La exposición prolongada puede dañar las células y aumentar el riesgo de cáncer.',
    'Rehabilitación post-misión': 'Proceso para recuperar la masa ósea y la fuerza muscular al volver a la Tierra. Requiere fisioterapia intensiva y ejercicios de resistencia.'
}

# Preguntas frecuentes de la IA
qa_data = {
    '¿Cómo afecta la microgravedad al cuerpo?': 'La microgravedad reduce la densidad ósea, atrofia los músculos y causa una redistribución de los fluidos corporales.',
    '¿Qué es la radiación cósmica?': 'Son partículas de alta energía que provienen del espacio. La exposición prolongada puede dañar las células y aumentar el riesgo de cáncer.',
    '¿Por qué se pierde masa ósea en el espacio?': 'La falta de gravedad no le da a los huesos la carga que necesitan para mantenerse fuertes, lo que hace que pierdan densidad y calcio.',
    '¿Qué es la densidad ósea?': 'Es una medida de la cantidad de minerales en los huesos. Una baja densidad ósea aumenta el riesgo de fracturas.',
    '¿Qué es la rehabilitación post-misión?': 'Es un programa de ejercicios y fisioterapia que los astronautas siguen al volver a la Tierra para recuperar la fuerza muscular y la densidad ósea perdidas.'
}

# --- Configuración de la Aplicación Dash ---
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

# --- Funciones de Ayuda ---
def get_image_path(image_name):
    """Devuelve la ruta de la imagen en la carpeta assets."""
    return app.get_asset_url(image_name)

def get_status_color(value):
    """Devuelve un color basado en el valor de salud/densidad."""
    if value >= 80:
        return 'green'
    elif value >= 60:
        return 'yellow'
    else:
        return 'red'

def get_gauge_status(value):
    """Devuelve un estado textual para el medidor."""
    if value >= 80:
        return 'Excelente'
    elif value >= 60:
        return 'Aceptable'
    else:
        return 'Riesgo'

def get_gauge_color_scale(value):
    """Devuelve un diccionario para la escala de colores del medidor."""
    if value >= 80:
        return {'default': '#1f77b4', 'good': 'green', 'ok': 'yellow', 'bad': 'red'}
    elif value >= 60:
        return {'default': '#1f77b4', 'good': 'green', 'ok': 'yellow', 'bad': 'red'}
    else:
        return {'default': '#1f77b4', 'good': 'green', 'ok': 'yellow', 'bad': 'red'}

# --- Diseño de la aplicación ---
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

def crear_pagina_inicio():
    """Diseño de la página de inicio."""
    return html.Div(style={'backgroundColor': '#000033', 'color': 'white', 'textAlign': 'center', 'height': '100vh', 'fontFamily': 'Arial, sans-serif'}, children=[
        html.H1("Laboratorio de Biología Espacial", style={'paddingTop': '50px', 'fontSize': '4em', 'fontWeight': 'bold'}),
        html.P("Elige un sujeto para iniciar la simulación:", style={'fontSize': '1.5em', 'marginTop': '20px'}),
        html.Div(style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '50px'}, children=[
            dcc.Link(href='/simulador/astronauta', children=[
                html.Div(style={'margin': '20px', 'cursor': 'pointer'}, children=[
                    html.Img(src=get_image_path('astronauta_mision.jpg'), style={'width': '200px', 'borderRadius': '10px', 'border': '3px solid white'}),
                    html.H3("ASTRONAUTA", style={'fontSize': '1.2em', 'marginTop': '10px'})
                ])
            ]),
            dcc.Link(href='/simulador/mono_juan', children=[
                html.Div(style={'margin': '20px', 'cursor': 'pointer'}, children=[
                    html.Img(src=get_image_path('mono_juan.jpg'), style={'width': '200px', 'borderRadius': '10px', 'border': '3px solid white'}),
                    html.H3("MONO JUAN", style={'fontSize': '1.2em', 'marginTop': '10px'})
                ])
            ]),
            dcc.Link(href='/simulador/planta', children=[
                html.Div(style={'margin': '20px', 'cursor': 'pointer'}, children=[
                    html.Img(src=get_image_path('planta.jpg'), style={'width': '200px', 'borderRadius': '10px', 'border': '3px solid white'}),
                    html.H3("PLANTA", style={'fontSize': '1.2em', 'marginTop': '10px'})
                ])
            ])
        ]),
        dcc.Link(href='/pioneros', children=[
            html.Button("VER PIONEROS", style={'marginTop': '50px', 'padding': '15px 30px', 'fontSize': '1.2em', 'fontWeight': 'bold', 'backgroundColor': '#007bff', 'color': 'white', 'border': 'none', 'borderRadius': '8px', 'cursor': 'pointer'})
        ])
    ])

def crear_pagina_pioneros():
    """Diseño de la página de pioneros."""
    cards = []
    for nombre, data in pioneros_nasa.items():
        card = html.Div(style={'backgroundColor': '#1a1a40', 'borderRadius': '10px', 'padding': '20px', 'margin': '10px', 'width': '300px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'}, children=[
            html.H4(nombre, style={'marginBottom': '10px'}),
            html.Img(src=get_image_path(data['imagen']), style={'width': '100%', 'borderRadius': '5px'}),
            html.P(data['historia'], style={'marginTop': '15px', 'fontSize': '0.9em'})
        ])
        cards.append(card)

    return html.Div(style={'backgroundColor': '#000033', 'color': 'white', 'textAlign': 'center', 'minHeight': '100vh', 'fontFamily': 'Arial, sans-serif'}, children=[
        html.H1("Pioneros de la NASA", style={'paddingTop': '50px', 'fontSize': '3em', 'fontWeight': 'bold'}),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'marginTop': '20px'}, children=cards),
        dcc.Link(href='/', children=[
            html.Button("VOLVER A INICIO", style={'marginTop': '50px', 'marginBottom': '50px', 'padding': '15px 30px', 'fontSize': '1.2em', 'fontWeight': 'bold', 'backgroundColor': '#007bff', 'color': 'white', 'border': 'none', 'borderRadius': '8px', 'cursor': 'pointer'})
        ])
    ])

def crear_pagina_simulador(sujeto):
    """Diseño de la página del simulador."""
    data = sujetos_data[sujeto]
    return html.Div(style={'backgroundColor': '#000033', 'color': 'white', 'minHeight': '100vh', 'fontFamily': 'Arial, sans-serif'}, children=[
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '20px 40px', 'backgroundColor': '#1a1a40'}, children=[
            dcc.Link(href='/', children=html.Img(src=get_image_path('logo_nasa.png'), style={'height': '50px'})),
            html.H1(f"Simulación de {data['nombre']}", style={'margin': '0', 'flexGrow': '1', 'textAlign': 'center'}),
            html.Button("GLOSARIO", id="open-glosario-modal", n_clicks=0, style={'padding': '10px 20px', 'backgroundColor': '#007bff', 'color': 'white', 'border': 'none', 'borderRadius': '5px'})
        ]),
        html.Div(className='container', style={'padding': '20px'}, children=[
            html.Div(className='row', children=[
                html.Div(className='four columns', children=[
                    html.Img(id='sujeto-imagen', src=get_image_path(data['imagen']), style={'width': '100%', 'borderRadius': '10px'}),
                    html.H3(id='sujeto-nombre', style={'textAlign': 'center'}),
                    html.P(id='sujeto-historia', style={'textAlign': 'justify', 'fontSize': '0.9em', 'padding': '0 20px'}),
                    html.Div(id='bitacora-content', style={'marginTop': '20px', 'padding': '15px', 'backgroundColor': '#1a1a40', 'borderRadius': '10px', 'overflowY': 'auto', 'maxHeight': '300px'}),
                    html.Div(style={'marginTop': '20px', 'display': 'flex', 'justifyContent': 'space-around'}, children=[
                        html.Button("AVANZAR DÍA", id='avanzar-dia-btn', n_clicks=0, style={'backgroundColor': '#28a745', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px'}),
                        html.Button("REINICIAR", id='reiniciar-btn', n_clicks=0, style={'backgroundColor': '#dc3545', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px'})
                    ])
                ]),
                html.Div(className='eight columns', children=[
                    html.Div(id='simulacion-info', style={'padding': '20px', 'backgroundColor': '#1a1a40', 'borderRadius': '10px', 'marginBottom': '20px'}, children=[
                        html.H4("Datos de la Simulación", style={'marginBottom': '20px'}),
                        html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'textAlign': 'center'}, children=[
                            daq.Gauge(
                                id='salud-gauge',
                                label='Salud',
                                value=100,
                                max=100,
                                min=0,
                                showCurrentValue=True,
                                color={"gradient": True, "ranges": {"red": [0, 59], "yellow": [60, 79], "green": [80, 100]}}
                            ),
                            daq.Gauge(
                                id='densidad-gauge',
                                label='Densidad Ósea',
                                value=100,
                                max=100,
                                min=0,
                                showCurrentValue=True,
                                color={"gradient": True, "ranges": {"red": [0, 59], "yellow": [60, 79], "green": [80, 100]}}
                            )
                        ]),
                        html.P(id='info-ia', style={'marginTop': '20px', 'fontStyle': 'italic'}),
                        html.P(id='status-salud', style={'color': 'white'}),
                        html.P(id='status-densidad', style={'color': 'white'})
                    ]),
                    dcc.Graph(id='line-chart'),
                    html.Div(id='qa-section', children=[
                        html.H4("Preguntas Frecuentes", style={'marginTop': '20px'}),
                        dcc.Dropdown(
                            id='qa-dropdown',
                            options=[{'label': q, 'value': q} for q in qa_data.keys()],
                            placeholder="Selecciona una pregunta...",
                            style={'color': 'black'}
                        ),
                        html.Div(id='qa-answer', style={'marginTop': '10px', 'padding': '10px', 'backgroundColor': '#1a1a40', 'borderRadius': '5px'})
                    ])
                ])
            ]),
        ]),
        dcc.Store(id='sim-state', data=sim_data),
        dcc.Store(id='current-subject', data=sujeto),
        html.Div(id='glosario-modal', style={'display': 'none', 'position': 'fixed', 'zIndex': '1', 'left': '0', 'top': '0', 'width': '100%', 'height': '100%', 'overflow': 'auto', 'backgroundColor': 'rgba(0,0,0,0.4)'}, children=[
            html.Div(style={'backgroundColor': '#1a1a40', 'margin': '15% auto', 'padding': '20px', 'border': '1px solid #888', 'width': '80%', 'borderRadius': '10px'}, children=[
                html.Span("x", id="close-glosario-modal", style={'color': '#aaa', 'float': 'right', 'fontSize': '28px', 'fontWeight': 'bold', 'cursor': 'pointer'}),
                html.H2("Glosario de Términos", style={'textAlign': 'center'}),
                html.Div([
                    html.P(html.B(key + ": "), style={'marginBottom': '5px'}),
                    html.P(value, style={'marginBottom': '15px'})
                ] for key, value in glosario_data.items())
            ])
        ])
    ])

# --- Callbacks para la Navegación y Lógica de la Aplicación ---
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pioneros':
        return crear_pagina_pioneros()
    elif pathname.startswith('/simulador/'):
        sujeto = pathname.split('/')[-1]
        if sujeto in sujetos_data:
            return crear_pagina_simulador(sujeto)
        else:
            return crear_pagina_inicio()
    
    return crear_pagina_inicio()

@app.callback(
    [Output('salud-gauge', 'value'),
     Output('densidad-gauge', 'value'),
     Output('line-chart', 'figure'),
     Output('bitacora-content', 'children'),
     Output('sim-state', 'data'),
     Output('info-ia', 'children'),
     Output('status-salud', 'children'),
     Output('status-densidad', 'children')],
    [Input('avanzar-dia-btn', 'n_clicks'),
     Input('reiniciar-btn', 'n_clicks')],
    [State('sim-state', 'data'),
     State('current-subject', 'data')]
)
def actualizar_simulacion(n_clicks_avanzar, n_clicks_reiniciar, sim_state, sujeto):
    ctx = dash.callback_context
    if not ctx.triggered:
        dia_actual = sim_state['dias'][-1]
        salud_actual = sim_state['salud'][-1]
        densidad_actual = sim_state['densidad_osea'][-1]
        bitacora_actual = sim_state['bitacora']
        info_ia = sujetos_data[sujeto]['descripcion_ia']
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        bitacora_completa = sujetos_data[sujeto]['bitacora_evolucion']

        if button_id == 'reiniciar-btn':
            sim_state = {
                'dias': [0],
                'salud': [100],
                'densidad_osea': [100],
                'bitacora': ["Misión iniciada. Se observan datos iniciales y se espera su evolución."]
            }
            dia_actual = 0
            salud_actual = 100
            densidad_actual = 100
            bitacora_actual = ["Misión iniciada. Se observan datos iniciales y se espera su evolución."]
            info_ia = sujetos_data[sujeto]['descripcion_ia']
        else:
            dia_anterior = sim_state['dias'][-1]
            if dia_anterior >= len(bitacora_completa) - 1:
                dia_actual = dia_anterior
                salud_actual = sim_state['salud'][-1]
                densidad_actual = sim_state['densidad_osea'][-1]
                bitacora_actual = sim_state['bitacora']
                info_ia = "Misión completada. No hay más datos para mostrar."
            else:
                dia_actual = dia_anterior + 1
                bitacora_dia_actual = bitacora_completa[dia_actual]
                
                salud_anterior = sim_state['salud'][-1]
                densidad_anterior = sim_state['densidad_osea'][-1]

                salud_nueva = salud_anterior
                densidad_nueva = densidad_anterior
                
                if 'disminución' in bitacora_dia_actual or 'descenso' in bitacora_dia_actual or 'baja' in bitacora_dia_actual:
                    if 'salud' in bitacora_dia_actual:
                        salud_nueva -= random.uniform(1, 5)
                    if 'densidad ósea' in bitacora_dia_actual or 'densidad ósea' in bitacora_dia_actual:
                        densidad_nueva -= random.uniform(2, 6)

                if 'aumento' in bitacora_dia_actual or 'recupera' in bitacora_dia_actual or 'recuperación' in bitacora_dia_actual:
                    if 'salud' in bitacora_dia_actual:
                        salud_nueva += random.uniform(1, 3)
                    if 'densidad ósea' in bitacora_dia_actual:
                        densidad_nueva += random.uniform(2, 4)

                if 'estable' in bitacora_dia_actual:
                    salud_nueva = salud_anterior
                    densidad_nueva = densidad_anterior

                salud_actual = max(0, min(100, salud_nueva))
                densidad_actual = max(0, min(100, densidad_nueva))
                
                sim_state['dias'].append(dia_actual)
                sim_state['salud'].append(salud_actual)
                sim_state['densidad_osea'].append(densidad_actual)
                sim_state['bitacora'].append(bitacora_dia_actual)

                info_ia = bitacora_completa[dia_actual]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sim_state['dias'], y=sim_state['salud'], mode='lines+markers', name='Salud', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=sim_state['dias'], y=sim_state['densidad_osea'], mode='lines+markers', name='Densidad Ósea', line=dict(color='orange')))
    fig.update_layout(
        title='Evolución de Salud y Densidad Ósea',
        xaxis_title='Día de Misión',
        yaxis_title='Nivel (%)',
        plot_bgcolor='#1a1a40',
        paper_bgcolor='#000033',
        font_color='white',
        xaxis=dict(gridcolor='#333366'),
        yaxis=dict(gridcolor='#333366', range=[0, 105])
    )

    bitacora_display = [html.P(f"Día {i}: {text}") for i, text in enumerate(sim_state['bitacora'])]

    status_salud = f"Estado de Salud: {get_gauge_status(salud_actual)}"
    status_densidad = f"Estado de Densidad Ósea: {get_gauge_status(densidad_actual)}"

    return salud_actual, densidad_actual, fig, bitacora_display, sim_state, info_ia, status_salud, status_densidad

@app.callback(
    Output('qa-answer', 'children'),
    [Input('qa-dropdown', 'value')]
)
def display_qa_answer(selected_question):
    if selected_question:
        return qa_data[selected_question]
    return "Selecciona una pregunta para ver la respuesta."

@app.callback(
    Output('glosario-modal', 'style'),
    [Input('open-glosario-modal', 'n_clicks'),
     Input('close-glosario-modal', 'n_clicks')],
    [State('glosario-modal', 'style')]
)
def toggle_modal(n_open, n_close, current_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return {'display': 'none'}

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'open-glosario-modal':
        return {'display': 'block', 'position': 'fixed', 'zIndex': '1', 'left': '0', 'top': '0', 'width': '100%', 'height': '100%', 'overflow': 'auto', 'backgroundColor': 'rgba(0,0,0,0.4)'}
    elif button_id == 'close-glosario-modal':
        return {'display': 'none'}

    return {'display': 'none'}

if __name__ == '__main__':
    app.run(debug=True)
