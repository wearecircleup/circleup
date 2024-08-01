import re
header = "https://i.ibb.co/pQ97Jf9/Header-Size.png"
footer = "https://i.ibb.co/q59pdXX/home.png"

def claude_fb_html(user_name, recipient, feedback):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50;">   
        <div style="border-radius: 15px; overflow: hidden;">
            <img src="{header}" alt="Header" style="width: 100%; height: auto;">
        </div>
        
        <div style="margin-bottom: 20px; border-bottom: 1px solid #ddd; padding-bottom: 20px;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">Detalles de tu Propuesta</h3>
            <div>
                <p>Hola {user_name}!, gracias por compartir tu propuesta. Hemos revisado tu plan y a continuación te presentamos un feedback constructivo diseñado para potenciar la experiencia de aprendizaje de los participantes. Nuestras sugerencias buscan integrar los conceptos técnicos con habilidades de liderazgo, resolución de problemas y pensamiento crítico, adaptándose a los recursos disponibles en CircleUp. Te invitamos a considerar estas recomendaciones para optimizar el impacto de tu curso y proporcionar una experiencia educativa enriquecedora y práctica.</p>
            </div>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <th style="text-align: left; padding: 8px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Usuario</th>
                    <td style="padding: 8px; border: 1px solid #ddd;">{user_name}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Email</th>
                    <td style="padding: 8px; border: 1px solid #ddd;">{recipient}</td>
                </tr>
            </table>
        </div>
        {feedback}
    </body>
    </html>
    """
    
    return html

def claude_fb_plain(user_name, recipient, feedback):
    plain_text = f"""
Detalles de tu Propuesta
------------------------
Usuario: {user_name}
Email: {recipient}
Feedback: {feedback}
    """
    return plain_text.strip()

def pensum_html_file(user_name, recipient,course_name):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50;">
        <div style="border-radius: 15px; overflow: hidden;">
            <img src="{header}" alt="Header" style="width: 100%; height: auto;">
        </div>

        <h2 style="color: #2c3e50;">Hola, {user_name}</h2> 
        <p style="color: #2c3e50;">
            ¡Felicitaciones por completar el formulario del pensum! Reconozco el esfuerzo y el tiempo que has invertido en este proceso. 
            Tu dedicación es admirable y estoy aquí para ayudarte a perfeccionar tu propuesta.
        </p>
        <p style="color: #2c3e50;">
            Mi objetivo es colaborar contigo para desarrollar un contenido que no solo sea valioso, sino que también se alinee 
            con nuestros pilares fundamentales: liderazgo, pensamiento crítico y resolución de problemas. 
            Juntos, crearemos algo verdaderamente impactante para nuestra comunidad.
        </p>
            
        <div style="margin-bottom: 20px; border-bottom: 1px solid #ddd; padding-bottom: 20px;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">Detalles de tu Propuesta</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <th style="text-align: left; padding: 8px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Propuesta</th>
                    <td style="padding: 8px; border: 1px solid #ddd;">{course_name}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Email Contacto</th>
                    <td style="padding: 8px; border: 1px solid #ddd;">{recipient}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Nota</th>
                    <td style="padding: 8px; border: 1px solid #ddd;">Si necesitas hacer alguna corrección o tienes preguntas, por favor responde directamente a este correo. Estoy aquí para ayudarte en cada paso del proceso.</td>
                </tr>
            </table>
        </div>

        <p style="color: #2c3e50;">
            Revisaré tu propuesta cuidadosamente y te enviaré mis comentarios pronto. Estoy emocionado/a por ver 
            cómo tu idea contribuirá a enriquecer nuestra comunidad de aprendizaje.
        </p>

        <p style="color: #2c3e50;">
            Gracias por tu entusiasmo y compromiso. ¡Sigamos adelante con este emocionante proyecto!
        </p>

    </body>
    </html>
    """
    return html

def pensum_plain_file(user_name, recipient,course_name):
    plain_text = f"""
Hola, {user_name}

¡Felicitaciones por completar el formulario del pensum! Reconozco el esfuerzo y el tiempo que has invertido en este proceso. 
Tu dedicación es admirable y estoy aquí para ayudarte a perfeccionar tu propuesta.

Mi objetivo es colaborar contigo para desarrollar un contenido que no solo sea valioso, sino que también se alinee 
con nuestros pilares fundamentales: liderazgo, pensamiento crítico y resolución de problemas. 
Juntos, crearemos algo verdaderamente impactante para nuestra comunidad.

Detalles de tu Propuesta
------------------------
Nombre Curso: {course_name}
Email Contacto: {recipient}
Nota: Si necesitas hacer alguna corrección o tienes preguntas, por favor responde directamente a este correo. Estoy aquí para ayudarte en cada paso del proceso.

Revisaré tu propuesta cuidadosamente y te enviaré mis comentarios pronto. Estoy emocionado/a por ver 
cómo tu idea contribuirá a enriquecer nuestra comunidad de aprendizaje.

Gracias por tu entusiasmo y compromiso. ¡Sigamos adelante con este emocionante proyecto!
    """
    return plain_text.strip()

def pensum_html_anthropic(user_name, user,course_name):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50;">

        <p style="color: #2c3e50;">
            El usuario <strong>{user_name}</strong> ha cargado el proyecto <strong>{course_name.upper()}</strong> y está esperando una respuesta.
        </p>
            
        <div style="margin-bottom: 20px; border-bottom: 1px solid #ddd; padding-bottom: 20px;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">Detalles de tu Propuesta</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <th style="text-align: left; padding: 8px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Nombre Curso</th>
                    <td style="padding: 8px; border: 1px solid #ddd;">{course_name}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Nombre Usuario</th>
                    <td style="padding: 8px; border: 1px solid #ddd;">{user_name}</td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 8px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Código</th>
                    <td style="padding: 8px; border: 1px solid #ddd;">{user}</td>
                </tr>
            </table>
        </div>

    </body>
    </html>
    """
    return html

def pensum_plain_anthropic(user_name, user,course_name):
    plain_text = f"""

El usuario {user_name} ha cargado el proyecto {course_name.upper()} y está esperando una respuesta.

Detalles de tu Propuesta
------------------------
Nombre Curso: {course_name}
Nombre Usuario: {user_name}
Código: {user} 

    """
    return plain_text.strip()

