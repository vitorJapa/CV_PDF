from fpdf import FPDF
from setuptools.command.alias import alias


def create_cv(output_path):
    def sanitize_text(text):
        # Replace Unicode characters with their ASCII equivalents
        replacements = {
            '\u2019': "'",  # Replace typographic apostrophe
            '\u2013': "-",  # Replace en dash
            '\u2026': "..."  # Replace ellipsis
        }
        for unicode_char, ascii_char in replacements.items():
            text = text.replace(unicode_char, ascii_char)
        return text

    class PDF(FPDF):
        def header(self):
            self.add_font('Montserrat', '', 'Montserrat-Regular.ttf', uni=True)
            self.add_font('Montserrat', 'B', 'Montserrat-Bold.ttf', uni=True)
            self.add_font('Montserrat', 'I', 'Montserrat-Italic.ttf', uni=True)
            self.add_font('Montserrat-Thin', '', 'Montserrat-Thin.ttf', uni=True)
            self.add_font('OpenSans', '', 'OpenSans-Regular.ttf', uni=True)
            self.add_font('OpenSans', 'B', 'OpenSans-Bold.ttf', uni=True)

            # Nome no topo
            self.set_font('Montserrat-Thin', '', 20)
            name = "VITOR"
            self.cell(80, 5, name, align='R', ln=False)
            self.set_font('Montserrat', 'B', 20)
            last_name = "TAKAO KIHARA"
            self.cell(0, 5, last_name, ln=True)
            self.set_font('Montserrat', '', 8)
            self.cell(0, 5, 'SOFTWARE DEVELOPER', align='C', ln=True)
            self.line(35, 20, 175, 20)

            # Informações de contato (lado a lado)
            self.set_font('OpenSans', '', 7)
            contact_info = [
                {"icon": "phone_icon.png", "text": "(236) 412-0389"},
                {"icon": "email_icon.png", "text": "vitortk@hotmail.com"},
                {"icon": "linkedin_icon.png", "text": "linkedin.com/in/vitorkihara"},
                {"icon": "location_icon.png", "text": "New Westminster, BC"}
            ]

            icon_size = 3  # Tamanho do ícone (3x3mm)
            text_offset = 1  # Distância entre o ícone e o texto
            item_width = 40  # Largura total por item (ícone + texto)

            total_width = len(contact_info) * item_width + 10  # Adicionando 10 para o ajuste no espaçamento
            start_x = (self.w - total_width) / 2  # Centraliza horizontalmente
            y_offset = 25  # Posição vertical da linha

            # Alteração no cálculo do espaçamento entre o telefone e o email
            for i, item in enumerate(contact_info):
                self.set_xy(start_x, y_offset)  # Define a posição do ícone
                self.image(item["icon"], x=start_x, y=y_offset, w=icon_size, h=icon_size)  # Adiciona o ícone
                self.set_xy(start_x + icon_size + text_offset, y_offset)  # Define a posição do texto ao lado do ícone
                self.cell(item_width - icon_size - text_offset, 3, item["text"], align='L')  # Espaço para o texto
                start_x += item_width if i < 2 else item_width + 5  # Aumentando o espaçamento após o telefone

    pdf = PDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    left_column_width = 60  # Diminui a largura da coluna PROFILE
    right_column_width = 90

    # Profile Section
    pdf.set_xy(10, 40)
    pdf.set_font('Montserrat', 'B', 12)
    pdf.cell(left_column_width, 10, 'PROFILE', border='B', ln=True)
    pdf.set_font('OpenSans', '', 8)
    profile_text = sanitize_text(
        "As a software developer with over six years of experience, I have a strong foundation in Computer Science "
        "and a passion for creating high-quality software. I am a graduate of FIAP, and have a track record of "
        "delivering user-friendly, scalable, and bug-free applications. I am dedicated to producing software that meets "
        "the needs of users and exceeds their expectations."
    )
    pdf.multi_cell(left_column_width, 6, profile_text)
    profile_end_y = pdf.get_y()
    pdf.ln(5)

    # Education Section (posicionada abaixo do PROFILE)
    pdf.set_xy(10, profile_end_y + 5)
    pdf.set_font('Montserrat', 'B', 12)
    pdf.cell(left_column_width, 10, 'EDUCATION', border='B', ln=True)
    pdf.set_font('OpenSans', 'B', 7)
    education_title = sanitize_text("Bachelor's Degree in Computer Engineering")
    pdf.multi_cell(left_column_width, 6, education_title)
    pdf.set_font('OpenSans', '', 8)
    education_text = sanitize_text("FIAP (São Paulo, Brazil) 2012-2017")
    pdf.multi_cell(left_column_width, 6, education_text)
    profile_end_y = pdf.get_y()
    pdf.ln(2)

    # Skills Section
    pdf.set_xy(10, profile_end_y + 5)
    pdf.set_font('Montserrat', 'B', 12)
    pdf.cell(left_column_width, 10, 'SKILLS', border='B', ln=True)
    pdf.set_font('OpenSans', '', 8)
    skills_list = ["SQL", "Python", "Java", "MongoDB", "OutSystems", "Jira", "Agile & Scrum", "Pega"]
    column_width = left_column_width / 2  # Divide o espaço em duas colunas
    row_height = 6  # Altura de cada linha
    num_skills = len(skills_list)

    # Loop para criar duas colunas
    for i in range(0, num_skills, 2):
        pdf.set_x(10)  # Posiciona no início da linha
        pdf.cell(column_width, row_height, sanitize_text(skills_list[i]), border=0, align='L')
        if i + 1 < num_skills:  # Garante que existe um item na segunda coluna
            pdf.cell(column_width, row_height, sanitize_text(skills_list[i + 1]), border=0, align='L')
        pdf.ln(row_height)  # Avança para a próxima linha

    profile_end_y = pdf.get_y()
    pdf.ln(5)

    # Languages Section
    pdf.set_xy(10, profile_end_y + 5)
    pdf.set_font('Montserrat', 'B', 12)
    pdf.cell(left_column_width, 10, 'LANGUAGES', border='B', ln=True)

    # Lista de idiomas e proficiências
    languages_list = [
        {"language": "English", "proficiency": "Professional Proficiency"},
        {"language": "Portuguese", "proficiency": "Native"}
    ]

    pdf.set_font('OpenSans', '', 8)
    row_height = 6  # Altura de cada linha
    for lang in languages_list:
        pdf.set_x(10)  # Posiciona no início da linha
        pdf.cell(left_column_width / 2, row_height, lang["language"], border=0, align='L')  # Coluna de idiomas
        pdf.cell(left_column_width / 2, row_height, f"({lang['proficiency']})", border=0,
                 align='L')  # Coluna de proficiência
        pdf.ln(row_height)  # Avança para a próxima linha

    profile_end_y = pdf.get_y()
    pdf.ln(2)

    # Certifications Section
    pdf.set_xy(10, profile_end_y + 5)
    pdf.set_font('Montserrat', 'B', 12)
    pdf.cell(left_column_width, 10, 'CERTIFICATIONS', border='B', ln=True)
    pdf.set_font('OpenSans', '', 8)
    education_text = sanitize_text("Associate Reactive Developer OutSystems - Jul 2023")
    pdf.multi_cell(left_column_width, 6, education_text)

    num_skills = len(skills_list)

    # Ajusta a largura da coluna direita (experiência profissional)
    right_column_width = 120  # Aumente este valor conforme necessário

    # Professional Experience Section
    pdf.set_xy(80, 40)  # Certifique-se de iniciar no lado direito
    pdf.set_font('Montserrat', 'B', 12)
    pdf.cell(right_column_width, 10, 'PROFESSIONAL EXPERIENCE', border='B', ln=True)
    pdf.ln(2)

    start_x = 80  # Coordenada X fixa para alinhar à direita
    start_y = pdf.get_y()  # Pega a posição Y atual para começar a imprimir

    experiences = [
        {
            "role": "PEGA SUPPORT ANALYST",
            "company": "Canaccord Genuity",
            "location": "Vancouver, BC",
            "dates": "Feb/2022 - Sep/2022",
            "details": [
                "Provided end-to-end engineering support, including designing, configuring, testing, and troubleshooting systems.",
                "Collaborated with users to define functional specifications for hardware and software solutions.",
                "Managed and resolved complex incidents using Jira and ServiceNow, ensuring minimal disruption to operations.",
                "Authored and maintained comprehensive user manuals and technical guidelines."
            ]
        },
        {
            "role": "SOFTWARE DEVELOPER",
            "company": "Deloitte",
            "location": "São Paulo, Brazil",
            "dates": "Jun/2018 - Nov/2021",
            "details": [
                "Developed REST applications and microservices using OutSystems, Java, and Python.",
                "Conducted unit testing and implemented object-oriented programming solutions.",
                "Designed and deployed over 100 production packages with minimal downtime.",
                "Monitored production environments and created detailed reports to meet stakeholder requirements.",
                "Enhanced system performance by identifying and resolving bottlenecks in collaboration with cross-functional teams."
            ]
        },
        {
            "role": "JUNIOR SYSTEM ANALYST",
            "company": "Deloitte",
            "location": "São Paulo, Brazil",
            "dates": "Apr/2017 - Jun/2018",
            "details": [
                "Delivered support for business applications and infrastructure in production environments.",
                "Managed over 10 production tickets daily, maintaining a customer satisfaction rating of 95%.",
                "Prioritized and resolved tickets in collaboration with global teams, ensuring timely resolution."
            ]
        },
        {
            "role": "SUPPORT ANALYST",
            "company": "Geber Outsourcing",
            "location": "São Paulo, Brazil",
            "dates": "Apr/2013 - Apr/2017",
            "details": [
                "Installed and maintained IT equipment and configured servers with Windows and relevant software.",
                "Ensured proper server setup and system functionality for clients."
            ]
        }
    ]

    for exp in experiences:
        pdf.set_xy(start_x, start_y)  # Mantém a posição fixa à direita
        pdf.set_font('Montserrat', '', 9)
        pdf.multi_cell(right_column_width, 6, sanitize_text(f"{exp['company']} - {exp['location']}"))
        start_y = pdf.get_y()
        pdf.set_xy(start_x, start_y)
        pdf.set_font('Montserrat', 'B', 9)
        pdf.multi_cell(right_column_width, 6, sanitize_text(f"{exp['role']}, {exp['dates']}"))
        start_y = pdf.get_y()
        pdf.set_font('Montserrat', '', 8)
        for detail in exp['details']:
            pdf.set_xy(start_x, start_y)
            pdf.multi_cell(right_column_width, 6, sanitize_text(f"- {detail}"))
            start_y = pdf.get_y()
        pdf.ln(5)  # Adiciona espaço entre as experiências
        start_y = pdf.get_y()  # Atualiza a posição Y para a próxima experiência

    # Save PDF
    pdf.output(output_path)

if __name__ == '__main__':
# Call the function to create the CV
    create_cv("Vitor_Kihara_CV.pdf")
