import pytest

# Sample AI-generated text (typical ChatGPT style)
AI_TEXT_EN = """
The landscape of artificial intelligence has undergone a transformative evolution in recent years. This multifaceted technology has revolutionized numerous sectors, illuminating new pathways for innovation and growth. Furthermore, the profound impact of machine learning algorithms has created a tapestry of interconnected systems that seamlessly integrate into our daily lives.

It is important to note that the comprehensive nature of these advancements has fostered a robust ecosystem of tools and platforms. Moreover, the pivotal role of data in driving these innovations cannot be understated. The intricate relationship between data quality and model performance underscores the need for meticulous data curation practices.

Additionally, the realm of natural language processing has witnessed remarkable progress. These innovative approaches have enabled machines to navigate the complexities of human communication with unprecedented accuracy. The vibrant community of researchers continues to push the boundaries of what is possible, leveraging cutting-edge techniques to elucidate the nuances of language understanding.
"""

AI_TEXT_ES = """
En el ámbito de la inteligencia artificial, se ha producido una transformación sin precedentes en los últimos años. Es importante señalar que esta tecnología multifacética ha revolucionado numerosos sectores, iluminando nuevos caminos para la innovación y el crecimiento. Asimismo, el profundo impacto de los algoritmos de aprendizaje automático ha creado un tapiz de sistemas interconectados que se integran sin problemas en nuestra vida cotidiana.

Cabe destacar que la naturaleza integral de estos avances ha fomentado un ecosistema robusto de herramientas y plataformas. No obstante, el papel fundamental de los datos en impulsar estas innovaciones no puede subestimarse. La intrincada relación entre la calidad de los datos y el rendimiento del modelo subraya la necesidad de prácticas meticulosas de curación de datos.

Resulta fundamental comprender que el ámbito del procesamiento del lenguaje natural ha sido testigo de un progreso notable. Estos enfoques innovadores han permitido a las máquinas navegar las complejidades de la comunicación humana con una precisión sin precedentes.
"""

# Sample human-written text (natural, varied style)
HUMAN_TEXT_EN = """
I've been thinking about AI a lot lately. Not in the grand, sweeping way you see in tech blogs -- more like how it's quietly changing the small stuff. My friend Sarah? She uses it to draft emails now. Says it saves her about an hour a day.

But here's the thing. The emails don't sound like her. They're too... neat. Too polished. She told me she rewrites half of them anyway because they feel "off." Kind of defeats the purpose, right?

And look, I get it. The technology is impressive. Really impressive. Last week I watched a demo where an AI wrote a decent short story in seconds. Seconds! But it was missing something. That weird, human messiness that makes writing interesting. The tangents. The half-formed thoughts. The jokes that only sort of land.

I don't know where this is all going. Nobody does, honestly. But I think the best use of AI isn't replacing human writing -- it's handling the boring stuff so we have more time for the creative bits. At least that's what I'm hoping.
"""

HUMAN_TEXT_ES = """
Llevo un tiempo dándole vueltas al tema de la inteligencia artificial. No de esa forma grandilocuente que ves en los blogs de tecnología, sino más bien pensando en cómo está cambiando las cosas pequeñas del día a día. Mi amiga Laura, por ejemplo, la usa para escribir correos. Dice que le ahorra como una hora al día.

Pero oye, hay un problema. Los correos no suenan como ella. Son demasiado... perfectos. Demasiado pulidos. Me contó que al final reescribe la mitad porque le parecen raros. Pues vaya ahorro, ¿no?

Y mira, lo entiendo. La tecnología es impresionante. De verdad que sí. La semana pasada vi una demo donde una IA escribió un relato corto en segundos. ¡Segundos! Pero le faltaba algo. Esa especie de desorden humano que hace que la escritura sea interesante. Las divagaciones. Los pensamientos a medio formar. Los chistes que no acaban de funcionar.

No sé adónde va todo esto. Nadie lo sabe, la verdad. Pero creo que lo mejor de la IA no es sustituir la escritura humana, sino encargarse de lo aburrido para que tengamos más tiempo para lo creativo. O eso espero, vamos.
"""


@pytest.fixture
def ai_text_en():
    return AI_TEXT_EN.strip()


@pytest.fixture
def ai_text_es():
    return AI_TEXT_ES.strip()


@pytest.fixture
def human_text_en():
    return HUMAN_TEXT_EN.strip()


@pytest.fixture
def human_text_es():
    return HUMAN_TEXT_ES.strip()
