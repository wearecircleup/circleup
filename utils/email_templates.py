import re
header = "https://i.ibb.co/3ptbBhS/footer.png"
footer = "https://i.ibb.co/q59pdXX/home.png"


def outline_text(text):
    highlighted_txt = re.sub(r"'(\w+)", r"<span style='color: #25c09e; font-weight: bold;'>\1", text)
    highlighted_txt = re.sub(r"(\w+\%?\.?)'", r"\1</span>", highlighted_txt)
    return highlighted_txt

def pensum_html(data,user_name):
  html = f"""
    <html>
        <div style="border-radius: 15px; overflow: hidden;">
            <img src="{header}" alt="Header" style="width: 100%; height: auto;">
        </div>

        <h1 style="color: #2c3e50;">Evaluación de Pensum @Circle Up</h1>

        <h2 style="color: #2c3e50;">Hola, {user_name}! </h2> 
        <p style="color: #2c3e50;">Esto es un backup del pensum que has construido, para que puedas llevar registro de las sugerencias de Anthropic y las tengas a la mano cuando trabajes en las mejoras.</p>
            
        <div style="margin-bottom: 20px; border-bottom: 1px solid #ddd; padding-bottom: 20px;">
            <h2 style="color: #2c3e50;">Pensum Propuesto</h2>
            <p><strong>Claridad:</strong> {outline_text(data['Claridad'][1])}</p>
            <p><strong>Relevancia:</strong> {outline_text(data['Relevancia'][1])}</p>
            <p><strong>Viabilidad:</strong> {outline_text(data['Viabilidad'][1])}</p>
            <p><strong>Impacto:</strong> {outline_text(data['Impacto'][1])}</p>
            <p><strong>Titulo:</strong> {outline_text(data['Titulo'][1])}</p>
            <p><strong>Objetivos:</strong> {outline_text(data['Objetivos'][1])}</p>
            <p><strong>Idea:</strong> {outline_text(data['Idea'][1])}</p>
            <p><strong>Actividades:</strong> {outline_text(data['Actividades'][1])}</p>
            <p><strong>Metodologia:</strong> {outline_text(data['Metodologia'][1])}</p>
        </div>

        <div style="border-radius: 15px; overflow: hidden;">
            <img src="{footer}" alt="Imagen de fondo" style="width: 100%; height: auto;">
        </div>

        </body>
    </html>
  """
  return html

def pensum_plain(data):
  plain = f"""
        Evaluación de Pensum @Circle Up
        Pensum Propuesto

        * **Claridad:** {data['Claridad'][1]}
        * **Relevancia:** {data['Relevancia'][1]}
        * **Viabilidad:** {data['Viabilidad'][1]}
        * **Impacto:** {data['Impacto'][1]}
        * **Titulo:** {data['Titulo'][1]}
        * **Objetivos:** {data['Objetivos'][1]}
        * **Idea:** {data['Idea'][1]}
        * **Actividades:** {data['Actividades'][1]}
        * **Metodologia:** {data['Metodologia'][1]}
  """
  return plain