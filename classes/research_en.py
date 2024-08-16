import streamlit as st
import pandas as pd


def create_html_table(df):
    html = """
    <style>
    .reference-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 14px;
        border: 0.2px solid #ddd;
        border-radius: 15px;
        overflow: hidden;
    }
    .reference-table th, .reference-table td {
        border: 0.2px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .reference-table th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    .reference-table td {
        color: #2C2C2C;
    }
    .link-button {
        background-color: #9d8ec7;
        color: white !important;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border-radius: 15px;
        font-size: 14px;
        transition: background-color 0.3s;
        font-weight: bold;
    }
    .link-button:hover {
        background-color: #8a7cb2;
    }
    /* Estilos para bordes redondeados */
    .reference-table tr:first-child th:first-child {
        border-top-left-radius: 15px;
    }
    .reference-table tr:first-child th:last-child {
        border-top-right-radius: 15px;
    }
    .reference-table tr:last-child td:first-child {
        border-bottom-left-radius: 15px;
    }
    .reference-table tr:last-child td:last-child {
        border-bottom-right-radius: 15px;
    }
    </style>
    <table class="reference-table">
    <tr>
        <th>Referencia (APA)</th>
        <th>Enlace</th>
    </tr>
    """
    
    for _, row in df.iterrows():
        html += f'<tr><td>{row["Referencia (APA)"]}</td>'
        if row['Enlace'] != "Sin Referencia":
            html += f'<td><a href="{row["Enlace"]}" target="_blank" class="link-button">Enlace</a></td>'
        else:
            html += '<td>Sin Referencia</td>'
        html += '</tr>'
    
    html += "</table>"
    return html

def main_en():
    
    st.title("Summary")

    st.write("""
    Circle Up Community is an initiative that combines academic volunteering with technology to drive the development of community skills. This project goes beyond being a volunteer program; it is a :blue[**comprehensive technological platform**] designed to optimize the use of local human capital and foster a :blue[**collaborative and adaptive learning ecosystem**].
    """)

    st.title("Conceptual Foundation and Context")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.info("""
            The project is based on a solid theoretical framework that integrates key concepts such as, :blue[**Community-Based Learning (CBL)**], :blue[**Lifelong Learning**] and :blue[**Knowledge Economy**]
            """, icon=":material/diversity_3:")

        with col2:
            st.success("""
            Circle Up Community responds to the needs of the :green[**fourth industrial revolution**], where adaptability and continuous learning are crucial.
            """, icon=":material/charger:")

    st.write("""
    This technological infrastructure allows Circle Up Community to be both standardized in its management and flexible in its implementation, adapting to the needs of the community.
    """)

    st.title("Central Problem and Objectives")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.info("""
            **Central Problem and General Objective**

            1. Underutilization of local human capital in Tocancipá for the development of community skills.

            2. Optimize the use of local human capital for the development of community skills in Tocancipá.
            """, icon=":material/target:")

        with col2:
            st.info("""
            **Specific Objectives**

            1. :blue[**Implement a structured system of academic volunteering.**]

            2. :blue[**Align local skills with the needs of the community.**]
            """, icon=":material/self_improvement:")

    st.title("Institutional Articulation")

    st.write("""
    Circle Up Community, as a Community-Based Learning (CBL) initiative in Tocancipá, establishes a significant relationship with the Secretariat of Social Development and Integration, particularly through the Youth Program. This strategic collaboration enhances the impact of both on the community and youth development of the municipality.
    """)

    st.write("Contributions of Circle Up to the Youth Program")

    st.write("""
    1. **Youth Capacities** Train young people in the construction of their life project. The courses and workshops offered by Circle Up develop essential soft and technical skills for the participants' personal and professional future.
    2. **Community Participation** Increase youth participation in community projects. This strengthens the social fabric and promotes youth leadership in Tocancipá.
    3. **Connection with Experts** Circle Up facilitates interaction between young people and experienced professionals from various fields. This connection provides valuable guidance on entrepreneurship and professional development, complementing the Youth Program's efforts in creating support networks for young people.
    """)


    st.title("Technological Platform and Innovation")

    st.write("""
    The core of Circle Up Community is a :blue[**digital platform**] that offers more than just volunteer management.
    """)

    with st.container(border=True):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("""
            :blue[**Artificial Intelligence**]

            Algorithms that collaborate with volunteers to develop and adapt personalized educational programs.
            """, icon=":material/rocket:")

        with col2:
            st.info("""
            :blue[**Process Automation System**]

            Improves resource allocation, course scheduling, and participant progress tracking.
            """, icon=":material/rocket:")

        with col3:
            st.info("""
            :blue[**Predictive Analytics**]

            Uses data to identify trends in the community's learning needs and anticipate demands.
            """, icon=":material/rocket:")


    with st.container(border=True):
        st.success("""
        **Benefits**

        This technological infrastructure allows Circle Up Community to be both, :green[**Standardized in its management**], :green[**Flexible in its implementation**]. Adapting to the specific needs of the community.
        """, icon=":material/bubble_chart:")

    st.image('./gallery/icons/research.svg',use_column_width=True)

    st.title("Introduction")

    st.write("Tocancipá, a municipality located in the Sabana Centro region of Colombia, has experienced remarkable industrial and economic growth in recent years. This development has brought about a series of demographic and social changes that have significantly impacted the educational and labor landscape of the region. The rapid population growth, driven in part by labor migration, has highlighted challenges in terms of skills development and access to educational opportunities that align with the demands of the evolving labor market.")

    st.write("The region faces particular challenges in the development of soft skills among its young population, a situation that can affect employability and long-term economic development. In addition, the intergenerational gap in terms of digital skills and technical knowledge presents another significant challenge for social cohesion and community development.")

    st.info("""
    **Key Challenges**
    - Rapid population and industrial growth
    - Development of soft skills in the young population
    - Intergenerational gap in digital and technical skills
    """, icon=":material/pool:")


    st.title("Justification")

    st.write("""
    The social and educational landscape in Colombia, particularly in regions of rapid industrial growth, presents a series of interconnected challenges that require innovative and adaptable solutions. This initiative emerges as a response to these multiple problems, seeking to address them in a comprehensive and effective manner.

    One of the most pressing challenges is the gap between the skills demanded by the labor market and those possessed by the current workforce. In areas of accelerated economic development, this disparity is accentuated, creating a demand for specific skills that the traditional education system cannot meet with the necessary speed. An approach that facilitates the transfer of practical and updated knowledge between local professionals and community members could significantly contribute to reducing this gap.
    """)





    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(':blue[**Dropout and Soft Skills**]',icon=':material/kayaking:')
            st.info("""School and university dropout represents another critical challenge. Offering practical and relevant training could increase student motivation and improve their employability prospects. Furthermore, the development of soft skills, increasingly valued in the workplace, is another area where the traditional education system often falls short.
            """)

        with col2:
            st.info(':blue[**Lifelong Learning and Youth Unemployment**]',icon=':material/kayaking:')
            st.info("""The lack of opportunities for lifelong learning and professional development, especially outside of large cities, is another challenge that requires attention. Youth unemployment and underemployment are persistent problems. Initiatives that improve the skills of young people and create professional networks could open up new job opportunities.
            """)

        with col3:
            st.info(':blue[**Inequality and Aging**]',icon=':material/kayaking:')
            st.info("""The inequality in access to quality educational resources between regions deserves attention. Leveraging local talent and digital technologies could bring specialized knowledge to communities with limited access. The aging of the population presents the need to take advantage of the experience of older adults, promoting their social inclusion and sense of purpose.
            """)

    st.write("""
    The lack of spaces for social innovation at the local level is another area of opportunity. Community collaboration platforms could catalyze the emergence of innovative solutions to local problems. Finally, the need to strengthen the social fabric and sense of community, especially in areas of rapid demographic growth, is a crucial aspect. Fostering meaningful interactions between community members through shared learning could contribute to social cohesion and the integral development of the region.
    """)

    st.info("CBL and the integration of emerging technologies offer a promising approach to addressing the educational and social challenges of Tocancipá.", icon=":material/memory:")

    st.title("Conceptual and Methodological Framework")

    st.write("""
    The conceptual foundation of Circle Up Community is based on a convergence of educational theories and practices that have evolved in response to the challenges of contemporary society. This theoretical framework explores the key concepts that underpin the initiative, providing a basis for its development and critical evaluation.
    """)

    st.title("Community-Based Learning (CBL)")

    st.info("""
    :blue[**Definition of CBL**]: Community-Based Learning (CBL) is a pedagogical approach that 
    integrates academic learning with community service and critical reflection.
    """, icon=":material/bubble_chart:")

    st.write("""
    This model has its roots in the educational philosophy of John Dewey, who argued that the 
    most effective learning occurs through experience and reflection on that experience 
    (*Giles & Eyler*, 1994, p. 78). In recent decades, CBL has evolved to include a 
    variety of practices, from service-learning to participatory action research.

    *Bringle and Clayton* (2020) define service-learning (SL) as an educational approach that combines academic learning with community service. Students apply what they learn in class to address real problems in their community, and in turn, reflect on their experiences to deepen their academic understanding. (p. 47).

    According to *Bringle and Clayton* (2020), this innovative approach meaningfully integrates 
    community service into the academic curriculum of universities, granting students 
    credits for the learning acquired through their active engagement in solving real-world problems. 
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(":green[**Reflection**]\n\nCritical reflection on experiences is fundamental in the service-learning process.", icon=":material/emoji_objects:")

    with col2:
        st.success(":green[**Experiential Learning**]\n\nStudents apply theoretical knowledge to real-world problems.", icon=":material/experiment:")

    with col3:
        st.success(":green[**Community Collaboration**]\n\nStudents, academics, and community members work together on mutually beneficial projects.", icon=":material/handshake:")

    st.write("""
    Service-learning transcends university classrooms and extends to the community at large. 
    Students, academics, and community members work hand-in-hand, sharing knowledge, 
    skills, and diverse perspectives. This collaborative approach fosters the creation of learning 
    communities where all participants become teaching resources, problem solvers, and partners 
    in the search for solutions to real-world challenges.

    SL has been praised for its potential to foster civic engagement and experiential learning, 
    uniting students and communities in mutually beneficial projects. However, as *Stoecker* (2016) 
    points out, SL is not without its critics.
    """)

    st.info(""":blue[**Critique of SL**]: *Stoecker* (2016) argues that institutionalized SL often focuses on student learning outcomes, neglecting the needs and priorities of the community. This approach can perpetuate unequal power dynamics, where educational institutions dictate the terms of engagement without true collaboration with the community.""", icon=":material/hiking:")

    st.write("""
    Furthermore, there is the criticism that SL can fall into "tokenism" or the practice of involving 
    community members in a superficial or symbolic way, using communities as mere learning scenarios 
    for students, without a genuine commitment to social change.

    These criticisms do not intend to invalidate SL, but rather to underline the importance of careful 
    design and continuous evaluation of these programs. For SL to be truly transformative, it must be 
    based on equitable and respectful relationships between educational institutions and communities. 
    This implies recognizing and valuing the knowledge and experience of community members, as well 
    as involving them in all stages of the process, from identifying needs to evaluating impact.
    """)

    st.title("Lifelong Learning")

    st.write("""
    The concept of lifelong learning has gained prominence in recent decades as a response to rapid technological and social changes. UNESCO has been a key advocate of this approach, arguing that lifelong learning is essential for sustainable development and social cohesion (*UNESCO*, 2016, p. 8).
    """)

    st.info("""
    :blue[**Definition of LLL**]: Lifelong Learning (LLL) encompasses the entire spectrum of learning, including formal, informal, and non-formal.

    -- *Laal and Salamati* (2012)
    """, icon=":material/hiking:")

    st.write("""
    This broad perspective on learning recognizes that education is not limited to formal institutions or a particular stage of life. The authors highlight that LLL occurs in various contexts, including everyday experiences, the workplace, and leisure activities, and that it can lead to both personal development and professional growth.

    Furthermore, *Laal and Salamati* (2012) point out that "in the 21st century, we all need to be lifelong learners. We need to continually keep our skills updated to have an edge in everything we do." This statement underscores the importance of continuous learning in today's rapidly changing world and emphasizes that learning is not just a means to an end but an ongoing process that spans a lifetime.
    """)

    st.warning("""
    :orange[**Equity Challenge**]: However, it is crucial to recognize that access to lifelong learning opportunities is not equitable (*Desjardins & Ioannidou*, 2020). Factors such as socioeconomic status, geographic location, and family obligations can limit people's ability to participate in continuous learning.
    """, icon=":material/hiking:")

    st.write("""
    Those who are already better educated and those with relatively secure professional positions are further expanding their advantage through additional investments in adult learning, the so-called Matthew principle or the phenomenon in which those who already have advantages, such as a better education or secure professional positions, continue to accumulate more advantages through participation in learning. Research findings to date also confirm that, for various reasons, companies support those employees in their skills development who already possess greater skills. Therefore, any initiative that seeks to promote lifelong learning must proactively address these barriers.
    """)

    st.success("""
    :green[**Key Implication**]: Lifelong learning initiatives must be designed with equity in mind, proactively addressing barriers that prevent access and participation for all segments of society.
    """, icon=":material/pool:")

    st.title("Knowledge Economy")

    st.info("""
    :blue[**Definition of Knowledge Economy**]: The knowledge economy represents a paradigm shift in which production and services are based primarily on knowledge-intensive activities.
    """, icon=":material/lightbulb:")

    st.write("""
    This shift is characterized by a greater emphasis on intellectual capabilities than on physical inputs or natural resources. *Powell and Snellman* (2004) point out that the knowledge economy is distinguished by "a greater reliance on intellectual capabilities than on physical inputs or natural resources" (p. 201). In this sense, innovation, creativity, and adaptability are crucial for success in this new economic model.

    The knowledge economy is also characterized by an accelerated pace of technological and scientific change. New technologies and scientific advances emerge at an unprecedented rate, which in turn leads to the rapid obsolescence of existing products and services. *Powell and Snellman* (2004) state that the knowledge economy is characterized by "a rapid pace of technical and scientific advance, as well as equally rapid obsolescence" (p. 199). In this environment, companies and individuals must be able to adapt quickly to changes to remain competitive.

    Furthermore, the knowledge economy is driven by the production and dissemination of new knowledge. Investments in research and development (R&D), education, and information and communication technology are fundamental for growth and development. This implies that knowledge is not only produced but also shared and applied effectively at all levels of the economy.
    """)

    st.title("21st Century Skills")

    st.write("""
    In this context, "21st-century skills" have gained prominence. *Binkley et al.* (2012) identified ten key skills for the 21st century, grouping them into four categories:
    """)

    with st.expander("See 21st Century Skills"):
        st.markdown("""
        - **Ways of Thinking:** Creativity and innovation, critical thinking, problem-solving and decision-making, and learning to learn and metacognition.
        - **Ways of Working:** Communication and collaboration (teamwork).
        - **Tools for Working:** Information literacy (including research) and ICT literacy.
        - **Living in the World:** Citizenship (local and global), life and career, and personal and social responsibility (including cultural awareness and competence) (p. 18-19).
        """)

    st.write("""
    These skills reflect the growing need for individuals to adapt to rapid changes in society and technology. The importance of students developing higher-order thinking, flexible problem-solving and collaboration skills, and communication skills to succeed in work and life is emphasized.
    """)

    st.title("Trends in the labor market")

    st.write("""
    A report from the World Economic Forum (2023) on the future of work reveals significant trends in the labor market, particularly regarding the growing importance of soft skills and the adoption of technology. The report, based on a survey of 803 companies in 27 sectors and 45 economies, highlights that more than 85% of the surveyed organizations anticipate that the adoption of new and cutting-edge technologies, along with increased digital access, will drive transformation in their companies (World Economic Forum, 2023, p. 10).

    In Latin America, companies are expected to adopt technologies such as big data, cloud computing, and artificial intelligence (AI) in the next five years (World Economic Forum, 2023, pp. 32-33). Although most of these technologies are expected to have a net positive impact on employment, companies in the region also anticipate significant labor disruption due to factors such as the rising cost of living and slowing economic growth (World Economic Forum, 2023, pp. 20-21).
    """)

    st.success("""
    :green[**Importance of soft skills**]: The report emphasizes the growing importance of soft skills in today's work environment. Despite advances in automation, analytical and creative thinking remain the most valued skills by employers (World Economic Forum, 2023, p. 38). Additionally, skills such as resilience, flexibility, motivation, and self-awareness are increasingly essential for workers to adapt to constant changes in the workplace and collaborate effectively (World Economic Forum, 2023, p. 38).
    """, icon=":material/scuba_diving:")

    st.warning("""
    It is estimated that 44% of workers' current skills could become obsolete in the next five years (World Economic Forum, 2023, p. 37), highlighting the urgent need to invest in training and upskilling programs.
    """, icon=":material/hiking:")

    st.write("""
    Companies in the region recognize this need and plan to invest in on-the-job learning and training as part of their strategies for the future (World Economic Forum, 2023, p. 50). However, the responsibility for closing this skills gap does not fall solely on companies but requires a joint effort from the public and private sectors to ensure that workers are prepared for the challenges and opportunities presented by the knowledge economy.
    """)

    st.title("Public policies and organizational practices")

    st.write("""
    Public policies and organizational practices play a crucial role in the knowledge economy by facilitating skills development and workforce adaptability. *Brown et al.* (2020) argue that the orthodox human capital theory has led to policies that reduce human productivity to "learning to earn," limiting the potential for worker growth and development.

    In this sense, it is essential that public policies promote a more holistic approach to education and skills development, going beyond the mere acquisition of credentials and focusing on personal growth and human flourishing (*Brown et al.*, 2020, p. 143). This involves fostering skills such as critical thinking, creativity, collaboration, and adaptability, which are essential in the ever-changing knowledge economy.
    """)

    st.info("""
    :blue[**Organizational practices**]: Organizational practices must adapt to support the continuous development of employees and foster a culture of learning. This can include training and development programs, on-the-job learning opportunities, mentoring and coaching, and performance evaluation systems that recognize and reward learning and growth (*Brown et al.*, 2020, p. 183).
    """, icon=":material/account_tree:")

    st.write("""
    Service-learning (SL) can complement this approach by providing opportunities for employees to apply their knowledge and skills in real-world contexts and develop a sense of civic responsibility (*Bringle & Clayton*, 2020). By participating in SL projects, employees can acquire new skills, broaden their perspectives, and strengthen their commitment to lifelong learning and personal growth.
    """)


    st.success("""
    :green[**Benefits of Service-Learning in Organizations**]:
    - Practical application of knowledge and skills
    - Development of civic responsibility
    - Acquisition of new skills
    - Broadening of perspectives
    - Strengthening commitment to lifelong learning
    - Fostering personal growth
    """, icon=":material/potted_plant:")


    st.title("Social innovation")

    st.info("""
    :blue[**Definition of Social Innovation**]: Social innovation represents changes in social relations, governance systems, and collective empowerment that lead to greater social inclusion.

    -- *Moulaert and MacCallum* (2019, p. 13)
    """, icon=":material/self_improvement:")

    st.write("""
    Social innovation has emerged as a field of study and practice that seeks to address complex social challenges through novel solutions. This definition emphasizes the transformative aspect of social innovation, beyond simply proposing new solutions.

    The concept of social innovation has gained prominence in recent decades as a response to the growing complexity of social problems and the limitations of traditional market-based or technological solutions. *Howaldt et al.* (2018) argue that social innovation represents a paradigm shift in how we address social challenges, moving away from purely technological or market-driven solutions towards more participatory and community-centered approaches (p. 16).
    """)

    st.info("""
    :blue[**Expanded Definition**]: Social innovation is defined as the development and implementation of new ideas, products, services, and models that meet social needs and create new social relationships or collaborations (*Howaldt et al.*, 2018, p. 84).
    """, icon=":material/notifications:")

    st.write("""
    Unlike traditional innovation, which often focuses on economic benefit and competitive advantage, social innovation prioritizes social well-being and the creation of public value. This approach recognizes that complex social problems, such as poverty, inequality, and climate change, require solutions that go beyond individual interventions and address the root causes of the problems.

    *Howaldt et al.* (2018) emphasize that social innovation is not limited to a single sector or discipline but encompasses a wide range of actors, including citizens, non-profit organizations, businesses, government institutions, and research institutions (p. 4). Collaboration among these diverse actors is essential to leverage different perspectives, knowledge, and resources, enabling the development of more comprehensive and sustainable solutions. Furthermore, social innovation often involves the active participation of citizens and communities affected by social problems, ensuring that solutions are relevant and responsive to their specific needs.
    """)

    st.success("""
    :green[**Key Finding**]: *Krlev et al.* (2021) found in their empirical study that "the most successful social innovation initiatives are those that manage to create diverse networks of actors and foster co-creation with the community" (p. 288).
    """, icon=":material/travel_explore:")

    st.write("""
    This finding underscores the importance of community participation and empowerment in social innovation processes. Co-creation, in particular, allows solutions to be designed and developed in collaboration with those experiencing social problems, thus ensuring that innovations are relevant and responsive to the real needs of the community (p. 259).

    Furthermore, *Krlev et al.* (2021) highlight that social innovation is not just about creating new ideas or solutions but about institutionalizing new practices that address the root causes of social problems (p. 280). The study also reveals that the success of social innovation often depends on the ability of actors to mobilize diverse resources and establish cross-sector collaborations (p. 281). This may include combining financial, human, and social resources from different sectors, such as government, businesses, and civil society organizations. By leveraging the strengths and expertise of diverse actors, social innovation initiatives can achieve greater impact and address social problems more comprehensively.
    """)

    st.warning("""
    :orange[**Warning**]: *Pel et al.* (2020) warn about the risk that "the rhetoric of social innovation is used to justify the withdrawal of the state from the provision of social services, without addressing the structural causes of social problems" (p. 2).
    """, icon=":material/hiking:")

    st.write("""
    This critique underscores the need to consider social innovation within the broader context of social policies and existing power structures. It should not be seen as a panacea for all social problems but as a tool that can be used effectively or ineffectively, depending on how it is implemented and who controls it.

    *Pel et al.* (2020) also point out the importance of understanding social innovation as a relational and contextualized process (p. 3). Social innovations do not occur in a vacuum; they are deeply embedded in existing social relations and specific socio-material contexts. Therefore, the analysis of social innovation must go beyond individual initiatives and consider the power dynamics, institutions, and social structures that shape these innovations.

    Furthermore, *Pel et al.* (2020) highlight the need to distinguish between different types of social innovation (p. 5). Not all social innovations are equal in terms of their transformative potential. Some may be incremental, while others may be more radical and challenge existing power structures. It is crucial, therefore, to develop a more nuanced understanding of the various types of social innovation and their implications for social change.
    """)







    st.title("Emerging technologies in education")

    st.write("""
    In the Latin American context, the adoption of emerging technologies in education presents both unique opportunities and challenges. The region has experienced significant growth in the use of educational technologies in the last decade, driven by the need to improve the quality and access to education in diverse socioeconomic contexts.
    """)

    st.warning("""
    :orange[**Challenge in Technology Adoption**]: *Avello Martínez et al.* (2021) point out that 
    "urban areas have benefited more than rural areas" (p. 45) in the integration of educational technologies.
    """, icon=":material/developer_board:")

    st.write("""
    This disparity is due to several factors, including the lack of technological infrastructure in 
    rural areas, insufficient teacher training in the use of emerging technologies, and the 
    economic limitations that prevent many rural schools from acquiring and maintaining these technologies.
    """)

    st.title("Promising emerging technologies")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        :blue[**Mobile Learning**]: *Crompton and Burke* (2018) argue that "the high penetration rate of 
        mobile phones in developing countries offers a unique opportunity to democratize access to digital educational resources" (p. 53).
        """, icon=":material/developer_board:")

    with col2:
        st.info("""
        :blue[**Artificial Intelligence**]: *Zawacki-Richter et al.* (2019) point out that "AI in 
        education has the potential to provide personalized support to students, automate administrative 
        tasks, and offer detailed learning analytics" (p. 3).
        """, icon=":material/developer_board:")

    st.write("""
    The trend of mobile learning is particularly relevant in Latin America, where mobile phones are widely available even in areas with limited resources.

    Regarding AI, intelligent tutoring systems, for example, can adapt the pace and content of instruction to the individual needs of each student, significantly improving the efficiency and effectiveness of learning, especially in contexts where teaching resources are limited.

    However, the effective implementation of AI in education requires careful adaptation to local educational contexts. *Zawacki-Richter et al.* (2019) emphasize the importance of considering ethical aspects, such as the responsible and transparent use of student data, the protection of their privacy, and the prevention of any type of discrimination (p. 21).
    """)

    st.success("""
    :green[**Critical Perspective**]: *Lugo and Ithurburu* (2019) warn that "the implementation of 
    educational technology must go beyond the mere provision of devices, to focus on the development of 
    digital skills in both students and teachers" (p. 12).
    """, icon=":material/travel_explore:")

    st.write("""
    This view underscores the importance of a holistic approach that focuses not only on access to devices and connectivity but also on the development of skills to use these tools critically and creatively.

    In the context of Circle Up Community in Tocancipá, Colombia, the integration of emerging technologies offers opportunities to enrich community learning and expand its reach. However, it will be crucial to critically evaluate its implementation and its impact on learning outcomes and educational equity, considering the particularities of the Latin American and Colombian context.
    """)


    st.title("Intergenerational Learning")

    st.write("""
    Intergenerational learning, a process that fosters the exchange of knowledge and experiences between different generations, is becoming an increasingly crucial component in modern organizations. This approach recognizes that both young and older employees possess valuable knowledge and experiences that they can share with each other, challenging the traditional view of unidirectional knowledge transfer from older to younger individuals.
    """)

    st.success("""
    :green[**Case Study: Intergenerational Learning**]

    *Gerpott et al.* (2017) explored the dynamics of intergenerational learning in an 18-month apprenticeship program at a German automotive company, where young (16-19 years old) and experienced (41-47 years old) apprentices collaborated to train as toolmakers.
    """, icon=":material/experiment:")

    st.write("""
    This unique learning environment allowed the researchers to observe how knowledge flowed in both directions, with young and older apprentices sharing their unique knowledge and skills. For example, younger apprentices contributed their knowledge of technology and current learning methods, while older apprentices shared their extensive practical experience and company-specific knowledge. This bidirectional exchange of knowledge highlights the concept of "reverse mentoring," where younger employees teach older ones, a phenomenon increasingly recognized in today's business landscape.

    The findings of *Gerpott et al.* (2017) revealed that "both generations possess distinct expert, practical, social, and metacognitive knowledge, and exchange different types of knowledge at different points in time" (p. 4). The study identified four types of knowledge exchanged during the program.
    """)

    with st.expander("Types of Knowledge in Intergenerational Learning"):
        st.markdown("""
        - **Expert knowledge:** Information that can be easily articulated and transmitted, such as the younger apprentices' school knowledge of mathematics or mechanics (p. 20).

        - **Practical knowledge:** Tacit knowledge acquired through experience, related to knowing how to perform specific tasks. Older apprentices possessed extensive practical knowledge about the procedures and manual movements required to create tools (p. 22).

        - **Social knowledge:** Encompasses skills such as relationship management and effective interaction with others. Older apprentices often acted as role models, teaching conflict management and the importance of friendship and integrity at work (p. 23).

        - **Metacognitive knowledge:** Refers to the monitoring of one's own thought processes. Young apprentices taught new strategies for memorizing information, while older ones demonstrated how to maintain focus and cope with stressful situations (p. 24).
        """)

    st.write("""
    While intergenerational learning offers numerous benefits, its successful implementation requires careful planning and consideration. *Findsen and Formosa* (2011) highlight the importance of addressing potential challenges that may arise due to generational differences. The authors point out that "differences in learning styles, expectations, and life experiences can create barriers to effective communication between generations" (p. 168). For example, older learners may prefer traditional teaching methods, while younger ones may be more comfortable with technology-based approaches. Furthermore, expectations about roles and responsibilities in learning may vary between generations, which can lead to misunderstandings and conflicts.

    In addition to differences in learning styles and expectations, *Findsen and Formosa* (2011) also point out that negative stereotypes about aging and the capabilities of older adults can be a significant obstacle to intergenerational learning. These stereotypes can lead to a lack of mutual respect and understanding, hindering the creation of a positive and inclusive learning environment.
    """)

    st.info("""
    :blue[**Key Recommendation**]: To overcome these challenges, the authors suggest that the design of intergenerational programs must be intentional and reflective. This involves recognizing and valuing the diverse perspectives and experiences that each generation brings to the learning environment.
    """, icon=":material/lightbulb:")

    st.write("""
    Programs should be designed to foster mutual respect, understanding, and collaboration between generations. Training in intercultural communication, group facilitation, and activities that promote interaction and knowledge exchange can be valuable tools to achieve these goals. Additionally, it is essential to address negative stereotypes through education and the promotion of positive interactions between generations. By doing so, we can create more effective intergenerational learning programs that harness the power of generational diversity for the benefit of all involved.
    """)


    st.title("Conclusion of the Conceptual Framework")

    st.info("""
    :blue[**Theoretical Framework of Circle Up Community**]: This theoretical framework provides the conceptual foundation for Circle Up Community, 
    situating the initiative within the context of contemporary educational theories and practices.
    """, icon=":material/hiking:")

    st.write("""
    By combining elements of CBL, lifelong learning, social innovation, and the use 
    of emerging technologies, Circle Up Community seeks to create a model of community learning that is relevant 
    and adaptable to the changing needs of society. Only through careful consideration 
    of these factors can we truly assess the potential of Circle Up Community to contribute to 
    community learning and development.
    """)

    st.warning("""
    :orange[**Important Consideration**]: However, it is crucial to recognize that each of these 
    concepts presents its own challenges and limitations. The implementation and evaluation of Circle Up Community 
    will need to carefully address these complexities, maintaining a critical and reflective approach at 
    all times.
    """, icon=":material/hiking:")

    st.title("Key Concepts of the Conceptual Framework")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("Community-Based Learning (CBL)", icon=":material/handshake:")

    with col2:
        st.success("Lifelong Learning", icon=":material/self_improvement:")

    with col3:
        st.success("Social Innovation", icon=":material/lightbulb:")

    with col4:
        st.success("Emerging Technologies in Education", icon=":material/developer_board:")


    st.write("""
    These concepts form the fundamental pillars of the theoretical framework of Circle Up Community. The effective integration 
    of these elements will be crucial for the success and sustainability of the initiative in 
    the context of Tocancipá, Colombia.
    """)

    st.info("""
    :blue[**Next Steps**]: The implementation of Circle Up Community will require careful consideration of 
    how these theoretical concepts translate into concrete and measurable practices. It will be essential to develop 
    metrics and indicators that allow us to evaluate the impact of the initiative in terms of 
    community learning, social innovation, and sustainable development.
    """, icon=":material/rocket:")

    st.title("Methodological Framework")

    st.write("""
    This study proposes a qualitative research approach with a case study design, 
    focused on the planning and design of Circle Up Community in Tocancipá, Colombia. The case study, 
    as defined by *Yin* (2018), is "an empirical inquiry that investigates a contemporary phenomenon 
    in depth and within its real-life context" (p. 15). This approach will allow for a deep understanding 
    of the contextual factors that influence the design of Circle Up Community.
    """)

    st.title("Research Design")

    st.write("""
    The study will be structured in three main phases, adapted to maximize the use of secondary data 
    and quantitative analysis, while maintaining the flexibility to incorporate qualitative elements when necessary:
    """)

    st.success("""
    :green[**Phases of the Research Design**]

    1. **Secondary Data Analysis Phase:**
      - Collection and organization of the databases from the Bogotá-Cundinamarca Multipurpose Survey and the 2018 census.
      - Comprehensive analysis of the literature on Community-Based Learning and emerging technologies in education, with an emphasis on studies based on secondary data.
      - Review of relevant local and regional educational policies for Circle Up Community, using official documents and public data.

    2. **Modeling and Projection Phase:**
      - Development of an analytical framework for Circle Up Community, integrating the findings from the secondary data analysis and literature review.
      - Elaboration of statistical and projection models to estimate the current conditions in Tocancipá, based on available historical data.
      - Design of potential scenarios for the implementation of Circle Up Community, using predictive modeling techniques.

    3. **Validation and Refinement Phase:**
      - Consultation with experts in data analysis, education, educational technology, and community development to validate the proposed models and projections.
      - Conducting a sensitivity analysis to assess the robustness of our estimates and projections.
      - Refinement of the models based on expert feedback and the results of the sensitivity analysis.
    """, icon=":material/travel_explore:")

    st.info("""
    :blue[**Note**]: This research design focuses on the rigorous analysis of secondary data 
    and the creation of predictive models. We acknowledge the inherent limitations of this approach and 
    commit to being transparent about these limitations in all phases of the study.
    """, icon=":material/bubble_chart:")

    st.title("Key aspects of the design")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        1. **Integration of multiple data sources:** We will combine data from the Multipurpose Survey, 
        the 2018 census, and other relevant sources to create a comprehensive picture of the situation in Tocancipá.

        2. **Focus on extrapolation and projection:** Given the dynamic nature of Tocancipá, 
        we will develop sophisticated models to project current trends based on the 
        available historical data.

        3. **Multidisciplinary validation:** We will seek validation from experts in various fields 
        to ensure that our interpretations and projections are robust and relevant.
        """)

    with col2:
        st.markdown("""
        4. **Methodological flexibility:** Although we focus on quantitative analysis, we will remain 
        open to incorporating qualitative insights when necessary to contextualize 
        our findings.

        5. **Scenario consideration:** We will develop multiple scenarios for the implementation 
        of Circle Up Community, recognizing the inherent uncertainty in future projections.
        """)

    st.write("""
    This design will allow us to make the most of the available data while maintaining a 
    critical and reflective approach to the limitations of our method. The goal is to provide a 
    solid foundation for informed decision-making about the implementation of Circle Up Community in Tocancipá.
    """)


    st.title("Proposed data collection methods")

    st.write("""
    For this study, we have opted for an approach based on the analysis of secondary data, 
    taking advantage of the rich information available through official sources. Our main 
    source of data will be the National Administrative Department of Statistics (DANE) of Colombia, 
    specifically:
    """)

    st.markdown("""
    1. We will use more than 5 databases from the Bogotá-Cundinamarca Multipurpose Survey. 
      This survey offers a detailed view of living conditions in the region, covering topics 
      such as housing, education, health, and employment.

    2. We will perform a careful extrapolation of the data presented in the 2018 national census 
      to obtain updated estimates for Tocancipá and the surrounding region.
    """)

    st.warning("""
    :orange[**Limitations and considerations**]

    We recognize that this approach has inherent limitations:

    - Estimates based on the 2018 census and the 2021 sample may not accurately reflect 
      the current situation, especially in areas of rapid growth like Tocancipá.
    - It is likely that our estimates underestimate current values due to the demographic dynamism 
      of the region.
    - Users of this information should consider an additional margin of error when interpreting these 
      results.
    - We recommend using these estimates as a general reference and not as precise values for 
      the current population of Tocancipá.
    """, icon=":material/hiking:")


    st.title("Reasons for Choosing this Method")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        1. **Resource Efficiency**: The use of secondary data allows us to access a large amount 
            of information without the costs and time associated with primary data collection.
        2. **Source Reliability**: DANE is recognized for its methodological rigor and the quality 
            of its data.
        """)

    with col2:
        st.markdown("""
        3. **Breadth of Information**: The Multipurpose Survey databases offer a 
            multidimensional view that would be difficult to replicate with limited resources.
        4. **Temporal Continuity**: By using data from the 2018 census and more recent surveys, we can 
            observe trends and changes over time.
        """)

    st.title("Mitigation of Limitations")

    st.markdown("""
    To mitigate the limitations of this approach, we propose to:

    1. Be transparent about the methodology and data sources used.
    2. Provide confidence intervals or estimation ranges when possible.
    3. Supplement, when feasible, with qualitative data or data from local sources to contextualize 
      our findings.
    4. Maintain a critical attitude towards our own results, openly acknowledging areas of uncertainty.
    """)

    st.title("Proposed Data Analysis")

    st.write("""
    The data analysis for this study will be based on a systematic and detailed approach to the 
    information provided by the Bogotá-Cundinamarca Multipurpose Survey and the 2018 census 
    data. We will use statistical analysis and data visualization techniques to extract meaningful insights.
    """)

    st.info("""
    :blue[**Proposed Methodology**]

    1. **Data Extraction and Preparation**
    2. **Data Cleaning and Transformation**
    3. **Exploratory Data Analysis (EDA)**
    4. **Data Visualization**
    5. **Statistical Estimation and Inference**
    6. **Comparative Analysis**
    7. **Handling Biases and Limitations**
    8. **Contextualization of Results**
    """, icon=":material/stacked_bar_chart:")


    st.write("""
    This methodological approach will allow us to conduct a robust and detailed analysis of the available data, always taking into account the inherent limitations of using secondary data and the dynamic nature of the region under study. Our goal is to provide valuable insights while maintaining a high standard of methodological rigor and transparency in our conclusions.
    """)

    st.title("Ethical Considerations")

    st.write("""
    The research design will include the development of rigorous ethical protocols, following 
    the ethical guidelines of the American Educational Research Association (*AERA*, 2011). Although 
    our study is primarily based on secondary data, it is essential to maintain high 
    ethical standards in all phases of the research.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **1. Protection of privacy and confidentiality:**
        - Ensure that no individual can be identified
        - Implement additional anonymization techniques if necessary
        """, icon=":material/hiking:")

        st.info("""
        **2. Responsible use of data:**
        - Use the data only for the specified purposes
        - Avoid analyses that could stigmatize communities
        """, icon=":material/hiking:")

        st.info("""
        **3. Transparency and reproducibility:**
        - Meticulously detail methods and sources
        - Make analysis scripts available
        """, icon=":material/hiking:")

    with col2:
        st.info("""
        **4. Consideration of potential impacts:**
        - Assess the consequences of the findings
        - Present results in a balanced manner
        """, icon=":material/hiking:")

        st.info("""
        **5. Informed consent for additional data:**
        - Implement detailed consent forms if additional data is required
        """, icon=":material/hiking:")

        st.info("""
        **6. Ethical handling of sensitive data:**
        - Pay special attention to sensitive data
        - Handle with utmost care and confidentiality
        """, icon=":material/hiking:")

    st.info("""
    :blue[**Important**]: It is essential to guarantee the protection of the rights and well-being of 
    all indirect participants in the study, maintaining high ethical standards in all 
    phases of the research, from data analysis to the dissemination of results.
    """, icon=":material/hiking:")

    st.title("Potential Limitations")

    st.warning("""
    :orange[**Warning**]: It is acknowledged that this study will be limited to the specific context of 
    Tocancipá, and the results may not be directly generalizable to other contexts. Furthermore, 
    being a study based on secondary data and extrapolations, the conclusions about the current 
    situation in Tocancipá and the potential impact of Circle Up Community will be tentative.
    """, icon=":material/hiking:")


    st.title("Study Limitations")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(":green[1. **Limitations of secondary data:** Potential outdatedness and inherent biases.]", icon=":material/tactic:")

        st.success(":green[4. **Tentative nature of conclusions:** Speculation about the potential impact of Circle Up Community.]", icon=":material/tactic:")

        st.success(":green[7. **Challenges in data integration:** Possible compatibility issues between sources.]", icon=":material/tactic:")

    with col2:
        st.success(":green[2. **Challenges in extrapolation:** Uncertainty in estimations due to rapid development.]", icon=":material/tactic:")

        st.success(":green[5. **Lack of current primary data:** Limitation in capturing very recent dynamics.]", icon=":material/tactic:")

    with col3:
        st.success(":green[3. **Limitations in generalization:** Specific findings may not be applicable to other regions.]", icon=":material/tactic:")

        st.success(":green[6. **Limitations in capturing qualitative aspects:** Possible lack of representation of lived realities.]", icon=":material/tactic:")

        st.success("""
        :green[**Mitigation Strategies**]:

        - Be transparent about all limitations in our reports and publications.
        - Provide estimation ranges and confidence intervals whenever possible.
        - Recommend caution in the interpretation and application of our findings.
        """, icon=":material/tactic:")


    st.title("Population")

    st.title("Demographic and Socioeconomic Analysis of Tocancipá")

    st.write("""
    Population segmentation is a fundamental pillar for Circle Up Community in Tocancipá. To design and 
    implement effective programs, it is essential to have an in-depth understanding of the current demographic and 
    socioeconomic context of the municipality. In this analysis, we will rely primarily on two key data 
    sources: the 2018 National Population and Housing Census (CNPV) and the 2021 Bogotá-Cundinamarca 
    Multipurpose Survey (EM).
    """)

    st.info("""
    :blue[**Methodological Note**]: Although these datasets are a few years old, 
    they represent the most complete and reliable information collected by DANE for Tocancipá. Our 
    analysis will seek to reconcile and contextualize the differences between these sources to provide 
    the most up-to-date view possible of the municipality's demographic situation.
    """, icon=":material/bubble_chart:")

    st.title("Population Growth and Age Structure")

    st.success("""
    :green[**Important Fact**]: The 2018 CNPV recorded a total population of 39,416 inhabitants in 
    Tocancipá, evidencing significant population growth since the 23,981 inhabitants 
    counted in 2005.
    """, icon=":material/stacked_bar_chart:")

    st.write("The age structure of Tocancipá shows notable variations between the 2018 CNPV and the 2021 EM:")

    df_comparacion = pd.DataFrame({
        'Age Group': ['0-14 years', '15-59 years', '60 years or older'],
        '2018 CNPV': ['24.4%', '68.6%', '7.0%'],
        '2021 EM': ['7.5%', '80.5%', '12.0%']
    })

    st.dataframe(df_comparacion, hide_index=True, use_container_width=True)

    st.write("This discrepancy in the data presents both opportunities and challenges for Circle Up Community:")

    with st.expander("Implications for Circle Up Community"):
        st.markdown("""
        - **Opportunities**: The higher proportion of the population between 15-59 years old according to the 2021 EM (80.5%) 
          suggests a large pool of potential participants for volunteer and mentoring programs.
        - **Challenges**: The marked difference in the proportion of children under 14 years old between both sources 
          indicates the need for a deeper analysis to understand the true current demographic composition, 
          although it will not be necessary since the target population is over 14 years old.
        """)

    st.warning("""
    The differences observed between the 2018 CNPV and the 2021 EM could indicate a bias in the EM sample 
    or demographic changes. It is crucial to consider both sources when designing strategies for 
    Circle Up Community and, possibly, make adjustments to the estimates.
    """, icon=":material/hiking:")

    st.write("""
    The (2021 EM) provides a detailed and multidimensional view of Tocancipá, crucial for the 
    design and implementation of Circle Up Community. The focus will be on data relevant to the population 
    over 14 years old, which constitutes the target group for all of Circle Up Community's lines of work.
    """)

    with st.expander("Selected Chapters | Multipurpose Survey"):
        st.markdown("""
        1. Identification
        2. Housing and its environment data
        5. Household composition and demographics
        6. Health
        8. Education
        9. Use of information technologies (ICT)
        10. Participation in organizations and social networks
        11. Workforce
        """)

    st.write("""
    This comprehensive structure allows us to analyze various aspects relevant to Circle Up Community, from 
    the educational level and the use of technologies to community participation and the working conditions 
    of the adult and young population of Tocancipá.
    """)

    st.success("""
    :green[**Important for Circle Up Community**]: This information is crucial to adapt each of its 
    lines of work to the specific needs of the population over 14 years old in Tocancipá:

    1. **The Academic Volunteering Program** can benefit from data on educational level 
      and workforce to identify potential volunteers and areas of knowledge needed.
    2. **The Reverse Mentoring Program** can use information on ICT use and household composition 
      to design effective intergenerational exchange strategies.
    3. **The Social Innovation Laboratory** can leverage data on participation in 
      organizations to identify priority areas for intervention.
    """, icon=":material/pool:")

    st.title("Segmentation Analysis | Tocancipá")

    st.write("""
    The segmentation analysis of the population of Tocancipá is based on two main sources of 
    information: the 2018 National Population and Housing Census (CNPV) and the 2021 Bogotá-Cundinamarca 
    Multipurpose Survey (EM). These sources present significant differences in the 
    age distribution of the population, which requires careful analysis and an extrapolation methodology 
    to obtain updated and consistent estimates.
    """)

    st.title("Comparison of Age Distributions")

    df_comparacion_revisada = pd.DataFrame({
        'Age Group': ['0-14 years', '15-59 years', '60 years or older'],
        '2018 CNPV': ['24.4%', '68.6%', '7.0%'],
        '2021 EM': ['7.5%', '80.5%', '12.0%'],
        'Difference': ['-16.9%', '+11.9%', '+5.0%']
    })

    st.dataframe(df_comparacion_revisada, hide_index=True, use_container_width=True)

    st.write("""
    The discrepancies observed between the 2018 CNPV and the 2021 EM do not necessarily reflect actual changes 
    in the population, but rather can be attributed to differences in data collection methodologies and 
    sample sizes.
    """)

    st.title("Extrapolation Methodology")

    st.write("""
    To address these differences and obtain updated estimates, a statistical extrapolation methodology is employed. 
    This approach is based on the sampling design of the 2021 EM, which, according to the methodological 
    document, is "a probabilistic, stratified, and cluster sample" (DANE, 2021, p. 8).
    """)

    st.write("**Estimation Process**")

    with st.expander("See details of the estimation process"):
        st.markdown("""
        1. **Calculation of the Sample Proportion**

          The sample proportion is calculated as:

          $$p = \\frac{x}{n}$$

          Where $x$ is the number of individuals with the characteristic of interest and $n$ is the total sample size.

        2. **Estimation of the Standard Error**

          The standard error is calculated as:

          $$SE = \\sqrt{\\frac{p(1-p)}{n}}$$

          This formula considers the complex sample design of the 2021 EM.

        3. **Calculation of the Confidence Interval**

          A 95% confidence interval is used, calculated as:

          $$CI_{95\\%} = p \\pm z \\times SE$$

          Where $z$ is the critical value of the standard normal distribution for a 95% confidence level, which is approximately 1.96.

        4. **Extrapolation to the Total Population**

          The estimate for the total population is calculated as:

          $$\\hat{N} = p \\times N$$

          Where $N$ is the total population according to the 2018 CNPV (39,416 for Tocancipá).

        5. **Calculation of the Relative Standard Error**

          The relative standard error is calculated as:

          $$RSE = \\frac{SE}{p} \\times 100\\%$$
        """)

    st.write("**Adjustment by Age Distribution**")

    st.write("""
    It is important to note that the 2021 EM sample for Tocancipá (n=2015) must be adjusted to 
    reflect the age distribution of the 2018 CNPV. This post-stratification process involves assigning 
    weights to the 2021 EM observations to match the census distribution. This 
    adjustment is crucial to ensure that the final estimates are representative of the current population 
    structure of Tocancipá.
    """)

    st.title("Limitations and Considerations")

    st.write("""
    1. **Time Lag**: Extrapolating 2021 data to a 2018 population base may not 
      fully capture recent demographic changes.
    2. **Sample Size**: The 2021 EM is based on a relatively small sample for Tocancipá, 
      which may increase the margin of error in the estimates.
    3. **Assumed Homogeneity**: The method assumes a similar distribution of population characteristics 
      between 2018 and 2021, which may not be entirely accurate.
    """)

    st.warning("""
    :orange[**Important Note**]: The resulting estimates should be interpreted with caution, 
    considering these limitations. It is recommended to complement this analysis with additional local 
    data when possible.
    """, icon=":material/hiking:")

    with st.expander("Population Data Distribution (VA, 25-44 years old)"):

        df_va_gender_age = pd.DataFrame({
            'Gender': ['Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', 'Female'],
            'Age Range': ['25-29', '30-34', '35-39', '40-44', '25-29', '30-34', '35-39', '40-44'],
            'Sample': [105, 87, 70, 81, 108, 90, 81, 93],
            'Population Estimate': ['1,671-2,436', '1,352-2,052', '1,054-1,684', '1,246-1,923', 
                                    '1,725-2,500', '1,405-2,116', '1,246-1,923', '1,458-2,180']
        })

        st.dataframe(df_va_gender_age, hide_index=True, use_container_width=True)

    st.info("""
    :blue[**Methodological note**]: The population estimates are based on the extrapolation of the 
    sample of 2,015 people from the 2021 EM to the total population of 39,416 according to the 2018 CNPV. It 
    is important to consider that this extrapolation assumes a proportional distribution, which may 
    not reflect demographic changes that occurred between 2018 and 2021.
    """, icon=":material/bubble_chart:")

    st.write("""
    The Academic Volunteers (VA) segment, which encompasses the age range of 25 to 44 years, presents 
    a significant demographic composition for the Circle Up Community program. In the sample, this group 
    is composed of 343 men and 372 women, which translates to a population estimate of 
    6,715 men and 7,284 women in Tocancipá.
    """)

    st.success("""
    :green[**Key Insight**]: The presence of 8.46% more women than men in the VA segment 
    (372 vs 343 in the sample) suggests a potential for female leadership in the academic volunteering 
    program of Circle Up Community, reflecting a trend of greater female participation in community 
    development activities.
    """, icon=":material/lightbulb:")

    st.title("Distribution by Age Subgroups")

    subgrupos = [
        ("25-29 years old", """This subgroup shows a slight female predominance, with 108 women 
        (estimated 1,725-2,500) compared to 105 men (estimated 1,671-2,436). This parity suggests a 
        generational balance in young professionals who could bring fresh perspectives 
        to the program."""),
        ("30-34 years old", """A small imbalance in favor of women is observed, with 90 women 
        (estimated 1,405-2,116) versus 87 men (estimated 1,352-2,052). This subgroup could represent 
        professionals with emerging experience, valuable to the program."""),
        ("35-39 years old", """Here the trend is reversed, with 81 women (estimated 1,246-1,923) and 70 
        men (estimated 1,054-1,684). This subgroup could contribute more consolidated professional experience 
        to the program."""),
        ("40-44 years old", """The oldest subgroup again shows a female predominance, with 
        93 women (estimated 1,458-2,180) compared to 81 men (estimated 1,246-1,923). This segment 
        could offer the most solid and diverse experience to the program.""")
    ]

    for group, description in subgrupos:
        with st.expander(group):
            st.write(description)


    st.title("Implications for Circle Up Community")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(":green[**1. Diversity of Experiences**\n\nThe relatively uniform distribution among the age subgroups suggests that Circle Up Community can benefit from a broad spectrum of professional and life experiences in its VA program.]", icon=":material/tactic:")

        st.success(":green[**4. Generational Adaptability**\n\nThe age diversity within the VA group requires that Circle Up Community develop engagement and retention strategies tailored to the different generations represented.]", icon=":material/tactic:")

    with col2:
        st.success(":green[**2. Potential for Internal Mentorship**\n\nThe presence of different age cohorts within the VA group offers the possibility of establishing an internal mentoring system, where older volunteers can guide younger ones.]", icon=":material/tactic:")

        st.success(":green[**5. Potential for Intergenerational Innovation**\n\nThe mix of different age cohorts within the VA group can foster innovation through the exchange of perspectives between generations.]", icon=":material/tactic:")

    with col3:
        st.success(":green[**3. Focus on Gender Equity**\n\nAlthough there is a slight female predominance, Circle Up Community should maintain a focus on gender equity to ensure balanced representation at all levels of the program.]", icon=":material/tactic:")

    st.write("""
    This demographic analysis provides a solid foundation for the design and adaptation of the Circle Up Community 
    Academic Volunteer program. The age diversity and slight female predominance offer unique opportunities to create 
    a volunteer program rich in experiences and perspectives, capable of effectively addressing the educational 
    and social challenges of Tocancipá.
    """)

    st.title("Academic Volunteers (VA) Employment Landscape")

    with st.expander("Employment Status of VA, 25-44 years old"):

        df_va_labor = pd.DataFrame({'Gender': ['Male', 'Male', 'Male', 'Male', 'Male', 'Male',
            'Female', 'Female', 'Female', 'Female', 'Female', 'Female'],
            'Status': ['Looking for work', 'Studying', 'Permanently disabled for work',
                'Home duties', 'Other activity', 'Employed',
                'Looking for work', 'Studying', 'Permanently disabled for work',
                'Home duties', 'Other activity', 'Employed'],
            'Sample': [49, 127, 2, 16, 5, 375, 43, 101, 7, 114, 6, 300],
            'Population Estimate': ['693-1,224', '2,066-2,903', '-15-93', '160-466', '12-183', '6,666-8,005',
                '592-1,090', '1,600-2,351', '36-238', '1,832-2,628', '24-211', '5,256-6,481']
        })

        st.dataframe(df_va_labor, hide_index=True, use_container_width=True)

    st.info("""
    :blue[**Methodological note**]: The population estimates assume a proportional distribution 
    between the sample and the total population, which may not reflect recent changes in the 
    employment dynamics of Tocancipá.
    """, icon=":material/bubble_chart:")

    st.write("""
    The analysis of the employment situation of potential Academic Volunteers (VA) reveals significant patterns 
    that directly impact Circle Up Community's recruitment and retention strategy:
    """)

    patrones_ocupacionales = [
        ("Predominance of the Private Sector", """The majority of employed VAs, both men (236, 
        estimated 4,063-5,170) and women (183, estimated 3,085-4,074), work in private companies. 
        This data suggests a wide pool of private sector experience that Circle Up Community can leverage 
        for its volunteer program."""),
        ("Gender Gap in Government Jobs", """Although participation in the public sector 
        is low overall, there is a greater female presence (11 women, estimated 88-342) compared 
        to men (5, estimated 12-183). This difference could indicate greater 
        potential among female VAs for projects related to public services and administration."""),
        ("Entrepreneurship and Self-Employment", """A significant number of VAs are self-employed or freelancers, 
        with 70 men (estimated 1,054-1,684) and 52 women (estimated 744-1,290). This group could bring 
        valuable self-management and creativity skills to the volunteer program."""),
        ("Independent Professionals", """Although smaller in number, the presence of independent professionals 
        (7 men, estimated 36-238; 9 women, estimated 61-291) suggests a niche of 
        specialized expertise that Circle Up Community could leverage for more technical or complex projects.""")
    ]

    for title, description in patrones_ocupacionales:
        with st.expander(title):
            st.write(description)

    st.success("""
    :green[**Key Insight**]: The occupational diversity among employed VAs offers Circle Up Community a 
    rich ecosystem of skills and experiences. However, the concentration in the private sector 
    suggests the need for specific strategies to engage these professionals in volunteer activities 
    that complement their corporate careers.
    """, icon=":material/lightbulb:")


    st.title("Occupational Implications for Circle Up Community")

    st.write("These occupational trends have strategic implications for Circle Up Community:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.warning(":orange[**1. Corporate Partnerships**]\n\nEstablish partnerships with local companies to promote corporate volunteering.", icon=":material/strategy:")

        st.warning(":orange[**4. Cross-Mentoring**]\n\nEncourage collaboration between VAs from different sectors to enrich knowledge exchange.", icon=":material/strategy:")

    with col2:
        st.warning(":orange[**2. Specialized Projects**]\n\nIndependent professionals could lead specific projects that require specialized skills.", icon=":material/strategy:")

        st.warning(":orange[**5. Complementary Skills Development**]\n\nOffer opportunities for VAs to develop skills outside their usual professional field.", icon=":material/strategy:")

    with col3:
        st.warning(":orange[**3. Project Diversification**]\n\nOffer a variety of projects that leverage different skills and professional experiences.", icon=":material/strategy:")


    st.title("Academic Volunteers (VA) Educational and Migration Profile")

    st.info("""
    :blue[**Education Levels**]:
    1. Technical or Vocational
    2. Completed University (with degree)
    3. Completed Specialization (with degree)
    4. Incomplete University (without degree)
    5. Technological 
    6. Completed Master's (with degree)
    """, icon=":material/hiking:")

    with st.expander("Educational Level Distribution (VA, 25-44 years old) Employed & Education"):

        df_va_education = pd.DataFrame({'Gender': ['Male', 'Male', 'Male', 'Female', 'Female', 'Female'] * 6,
            'Location (5 years ago)': ['This municipality', 'Another municipality', 'Another country'] * 12,
            'Education Level': ['Completed Specialization (with degree)', 'Completed Specialization (with degree)', 'Completed Specialization (with degree)',
                'Completed Specialization (with degree)', 'Completed Specialization (with degree)', 'Completed Specialization (with degree)',
                'Completed Master\'s (with degree)', 'Completed Master\'s (with degree)', 'Completed Master\'s (with degree)',
                'Completed Master\'s (with degree)', 'Completed Master\'s (with degree)', 'Completed Master\'s (with degree)',
                'Technological', 'Technological', 'Technological', 'Technological', 'Technological', 'Technological',
                'Technical or Vocational', 'Technical or Vocational', 'Technical or Vocational', 'Technical or Vocational', 'Technical or Vocational', 'Technical or Vocational',
                'Incomplete University (without degree)', 'Incomplete University (without degree)', 'Incomplete University (without degree)',
                'Incomplete University (without degree)', 'Incomplete University (without degree)', 'Incomplete University (without degree)',
                'Completed University (with degree)', 'Completed University (with degree)', 'Completed University (with degree)',
                'Completed University (with degree)', 'Completed University (with degree)', 'Completed University (with degree)'],
            'Sample': [1, 7, 0, 9, 11, 0, 2, 1, 0, 2, 2, 0, 3, 3, 2, 3, 3, 0, 14, 7, 0, 17, 9, 1, 3, 2, 2, 3, 0, 3, 12, 7, 5, 14, 10, 2],
            'Population Estimate': ['-19-58', '36-238', '0-0', '61-291', '88-342', '0-0',
                '-15-93', '-19-58', '0-0', '-15-93', '-15-93', '0-0',
                '-8-125', '-8-125', '-15-93', '-8-125', '-8-125', '0-0',
                '131-417', '36-238', '0-0', '175-490', '61-291', '-19-58',
                '-8-125', '-15-93', '-15-93', '-8-125', '0-0', '-8-125',
                '102-367', '36-238', '12-183', '131-417', '75-317', '-15-93']
        })

        st.dataframe(df_va_education, hide_index=True, use_container_width=True)

    st.write("""
    The analysis of the educational level distribution of employed Academic Volunteers (VAs), 
    considering their place of residence 5 years ago, reveals significant patterns:
    """)

    patrones_educativos = [
        ("Attraction of Skilled Talent", """Tocancipá is attracting professionals with higher 
        academic training, especially at the specialization and completed university levels. This 
        influx of skilled talent enriches the pool of potential VAs for Circle Up Community, contributing 
        a diversity of experiences and knowledge."""),
        ("Prominent Female Mobility", """There is a greater presence of women with higher 
        educational levels who have moved to Tocancipá in the last 5 years. For example, 
        11 women with a completed specialization (estimated 88-342) come from other municipalities, compared 
        to 7 men (estimated 36-238). This trend underscores the potential for female leadership 
        identified in previous analyses."""),
        ("Predominance of Local Technical Training", """Among long-term residents, there is a 
        greater presence of technical training, with 14 men (estimated 131-417) and 17 women 
        (estimated 175-490) who resided in Tocancipá 5 years ago. This suggests a solid base of 
        practical skills among local VAs."""),
        ("Selective International Migration", """Although smaller in number, there is a presence of 
        professionals with university degrees from other countries, especially men 
        (5, estimated 12-183). This adds an additional layer of cultural diversity and international 
        experience to the VA pool.""")
    ]

    for title, description in patrones_educativos:
        with st.expander(title):
            st.write(description)

    st.success("""
    :green[**Key Insight**]: The combination of local talent with technical training and the influx of 
    professionals with higher education creates a diverse ecosystem of knowledge and skills among 
    the VAs. Circle Up Community has the opportunity to leverage this diversity to enrich its volunteer programs 
    and foster social innovation in Tocancipá.
    """, icon=":material/lightbulb:")

    st.write("These educational and migration trends have strategic implications for Circle Up Community:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(":blue[**1. Integration Programs**]\n\nDevelop initiatives that facilitate the integration of new professional residents, especially women, into the Tocancipá community through volunteering.", icon=":material/strategy:")

        st.info(":blue[**4. Complementary Skills Development**]\n\nOffer opportunities for VAs with technical training to expand their theoretical knowledge, and for those with university training to acquire local practical skills.", icon=":material/strategy:")

    with col2:
        st.info(":blue[**2. Multidimensional Mentoring**]\n\nImplement a mentoring system that leverages both local experience (technical training) and the expertise of newly arrived professionals with higher education.", icon=":material/strategy:")

        st.info(":blue[**5. Professional Networking**]\n\nFacilitate networking spaces that promote collaboration between VAs from different educational backgrounds and geographical origins, enhancing knowledge exchange and opportunities.", icon=":material/strategy:")

    with col3:
        st.info(":blue[**3. Social Innovation Projects**]\n\nDesign projects that combine local practical knowledge with the innovative perspectives of professionals with advanced training, fostering creative solutions to community challenges.", icon=":material/strategy:")

    st.write("""
    This educational and migration analysis reveals that Circle Up Community has access to a rich and diverse pool of 
    talent among employed VAs. By designing volunteer programs that leverage this educational diversity 
    and migration dynamics, Circle Up Community can not only maximize the impact of its initiatives 
    in the Tocancipá community but also contribute to the integration and professional development of 
    its volunteers, thus strengthening the social and economic fabric of the municipality.
    """)


    st.title("Life Satisfaction of Academic Volunteers (VA)")

    st.write("Life Satisfaction (VA, 25-44 years old) Employed & Education")

    st.write("""
    The distribution of life satisfaction among employed VAs with academic training reveals 
    significant patterns:
    """)

    fig1, fig2, fig3 = st.columns([1, 2, 1])

    fig2.image("./figures/vida.png", caption="Distribution of Life Satisfaction in Potential Academic Volunteers (VA) of Circle Up Community: Employed 25-44 years old with Higher Education", use_column_width=True)

    patrones_satisfaccion = [
        ("Concentration at High Levels", """Both men (34.3%) and women (33.9%) show a 
        modal concentration at satisfaction level 9, indicating high subjective well-being in 
        this population segment."""),
        ("Asymmetric Dispersion", """A negative asymmetry is observed in both genders, with a 
        longer tail towards the lower values. This distribution suggests the existence of subgroups 
        with satisfaction levels that diverge from the general pattern."""),
        ("Subtle Gender Differences", """
        - Men: Show a more uniform distribution between levels 8, 9, and 10 (24.8%, 34.3%, 25.7% respectively).
        - Women: Show a more pronounced concentration at levels 8 and 9 (32.2% and 33.9%), with lower representation at level 10 (20.3%).
        """),
        ("Presence of Outliers", """The existence of responses at low levels (4-6) in both 
        genders, although a minority, indicates the presence of individuals with life experiences 
        significantly different from the majority of the population.""")
    ]

    for title, description in patrones_satisfaccion:
        with st.expander(title):
            st.write(description)

    st.success("""
    :green[**Key Insight**]: The high overall life satisfaction, combined with the presence of outliers, 
    suggests a complex scenario where diverse experiences coexist. This landscape offers 
    opportunities for volunteer initiatives that address both the maintenance of general well-being 
    and the attention to specific groups with particular needs.
    """, icon=":material/lightbulb:")

    st.write("Implications for research and program design:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(":blue[**1. Segmentation of Initiatives**]\n\nDesign differentiated programs that cater to both the satisfied majority and the subgroups with lower subjective well-being.", icon=":material/account_tree:")

        st.info(":blue[**4. Longitudinal Monitoring**]\n\nEstablish a system for temporal monitoring of life satisfaction.", icon=":material/account_tree:")

    with col2:
        st.info(":blue[**2. Analysis of Contextual Factors**]\n\nExplore the socioeconomic, labor, and community variables that could explain the observed distribution.", icon=":material/account_tree:")

        st.info(":blue[**5. Exploration of Motivations**]\n\nInvestigate the relationship between satisfaction levels and motivations for volunteering.", icon=":material/account_tree:")

    with col3:
        st.info(":blue[**3. Focus on Gender Equity**]\n\nInvestigate further the subtle differences between genders and their implications for participation in volunteer activities.", icon=":material/account_tree:")

        st.info(":blue[**6. Design of Targeted Interventions**]\n\nDevelop specific programs to address the needs of individuals at the lower end of the satisfaction scale.", icon=":material/account_tree:")

    st.write("""
    The complexity of the life satisfaction distribution among VAs underscores the need for a 
    nuanced approach in the design of volunteer programs. While the general trend towards high 
    levels of satisfaction suggests fertile ground for community initiatives, the presence of 
    variability and outliers demands a flexible and adaptive approach that recognizes the 
    diversity of experiences and needs within the target population.
    """)

    st.title("Job Satisfaction of Academic Volunteers (VA)")

    st.write("""
    The job satisfaction of potential VAs reveals significant patterns with direct implications 
    for Circle Up Community:
    """)

    fig1, fig2, fig3 = st.columns([1, 2, 1])

    fig2.image("./figures/trabajo.png", caption="Job Satisfaction in the (VA) Population", use_column_width=True)

    patrones_laborales = [
        ("High Overall Satisfaction", """Both men and women show high levels of 
        job satisfaction, with a concentration in levels 7-9. This trend suggests a 
        favorable work environment in Tocancipá, which could translate into a greater willingness 
        to volunteer."""),
        ("Subtle Gender Differences", """
        - Men: Peak at level 8 (36.2%), followed by 9 (17.1%) and 7 (15.2%).
        - Women: More uniform distribution between 9 (22.9%), 8 (21.2%), and 7 (16.1%).
        This variation indicates possible differences in job expectations or experiences between 
        genders, requiring a nuanced approach in volunteer recruitment."""),
        ("Cases of Low Satisfaction", """The presence of a small percentage with low satisfaction 
        (levels 1-5) in both genders indicates the existence of subgroups that could benefit from 
        professional development or job support initiatives.""")
    ]

    for title, description in patrones_laborales:
        with st.expander(title):
            st.write(description)

    st.write("Implications for Circle Up Community")

    col1, col2 = st.columns(2)

    with col1:
        st.success(":green[**Implication 1**]\n\nThe high overall job satisfaction suggests a pool of potentially motivated volunteers with positive experiences that they can transfer to the community sphere.", icon=":material/target:")

        st.success(":green[**Implication 2**]\n\nThe variability in satisfaction levels offers the opportunity to design volunteer programs that address diverse needs and motivations.", icon=":material/target:")

        st.success(":green[**Implication 3**]\n\nThe correlation between job satisfaction and community engagement deserves further investigation to optimize volunteer recruitment and retention strategies.", icon=":material/target:")

    with col2:
        st.success(":green[**Strategy 1**]\n\nDevelop volunteer programs that complement positive work experiences, leveraging the skills and motivation of highly satisfied VAs.", icon=":material/target:")

        st.success(":green[**Strategy 2**]\n\nImplement specific initiatives to engage those with lower job satisfaction, offering opportunities for personal and professional development through volunteering.", icon=":material/target:")

        st.success(":green[**Strategy 3**]\n\nEstablish partnerships with local employers to promote volunteering as an extension of professional development, enhancing both job and personal satisfaction.", icon=":material/target:")


    st.write("""
    The distribution of job satisfaction among potential VAs presents a favorable outlook 
    for Circle Up Community, with a large segment of satisfied and motivated professionals. However, the 
    presence of variability and cases of low satisfaction underscores the need for a 
    diversified approach in the design of volunteer programs, considering both leveraging 
    positive experiences and addressing the needs for development and personal fulfillment 
    of all segments of the target population.
    """)


    st.title("Community Satisfaction of Academic Volunteers (VA)")

    fig1, fig2, fig3 = st.columns([1, 2, 1])
    fig2.image("./figures/comunidad.png", caption="Community Satisfaction in the Employed Population Aged 25 to 44 with Academic Training in Tocancipá", use_column_width=True)

    st.write("""
    The figure reveals critical patterns in the community satisfaction of potential VAs, with 
    substantial implications for Circle Up Community:
    """)

    patrones_comunitarios = [
        ("Predominance of High Satisfaction", """Satisfaction level 8 dominates in both genders 
        (42 men, est. 719-1,247; 36 women, est. 616-1,067), indicating a solid foundation of community 
        appreciation. This trend suggests fertile ground for volunteer initiatives rooted 
        in local pride."""),
        ("Excellence Segment", """A significant group reports a satisfaction level of 9 (22 men, 
        26 women), representing potential community leaders and enthusiastic ambassadors for 
        Circle Up Community programs."""),
        ("Diversity of Experiences", """Approximately one-third of respondents (36.2% men, 
        37.3% women) report satisfaction levels of 7 or lower, signaling a critical segment that 
        perceives opportunities for community improvement.""")
    ]

    for title, description in patrones_comunitarios:
        with st.expander(title):
            st.write(description)

    st.title("Strategic Implications for Circle Up Community")

    implicaciones_comunitarias = [
        "The high overall satisfaction provides a base of potentially committed volunteers motivated by community well-being.",
        "The presence of a less satisfied segment offers opportunities for volunteer programs focused on addressing specific concerns and improving community quality of life.",
        "The varied distribution of satisfaction suggests the need for a diversified approach in volunteer recruitment and program design."
    ]

    for implication in implicaciones_comunitarias:
        st.markdown(f"- {implication}")

    st.title("Operational Recommendations")

    recomendaciones_comunitarias = [
        "Develop programs that capitalize on the community pride of the highly satisfied, involving them in improvement and preservation initiatives.",
        "Implement specific projects that address the concerns of the less satisfied segment, using volunteering as a tool for empowerment and community change.",
        "Establish a continuous feedback system to monitor how volunteer initiatives impact community satisfaction over time."
    ]

    for recommendation in recomendaciones_comunitarias:
        st.markdown(f"- {recommendation}")

    st.write("""
    The distribution of community satisfaction among potential VAs presents a promising scenario 
    for Circle Up Community, with a satisfied majority that can drive positive initiatives. However, 
    the presence of a significant segment with lower satisfaction underscores the importance of an 
    inclusive approach and one oriented towards continuous improvement in the design of volunteer programs. 
    This duality offers Circle Up Community the unique opportunity to catalyze civic engagement, leveraging 
    both the enthusiasm of the most satisfied and the motivation for change of those who 
    perceive areas for improvement in their community.
    """)

    st.title("Internet Use for Education among Academic Volunteers (VA)")

    df_internet_edu = pd.DataFrame({
        'Gender': ['Male', 'Male', 'Female', 'Female'],
        'Internet Use': ['No', 'Yes', 'No', 'Yes'],
        'Sample': [68, 37, 64, 54],
        'Population Estimate': ['1,019-1,641', '493-955', '950-1,554', '778-1,334']
    })

    st.dataframe(df_internet_edu, hide_index=True, use_container_width=True)

    st.write("""
    The table reveals crucial patterns in the use of the Internet for education among potential VAs, 
    with profound implications for Circle Up Community and the educational landscape in Tocancipá:
    """)

    patrones_internet = [
        ("Digital Divide in Education", """The majority of VAs do not use the Internet for educational purposes 
        (64.8% of men and 54.2% of women), evidencing a critical underutilization of digital 
        resources. This phenomenon suggests a disconnect between academic training and the adoption of 
        modern educational technologies, potentially limiting the continuous development of skills 
        in the local workforce."""),
        ("Gender Disparity in Digital Adoption", """Women show a greater propensity for educational use 
        of the Internet (45.8% vs 35.2% in men), indicating a gender gap in technological adaptability. 
        This trend could reflect differences in professional development strategies 
        or in the perception of the value of online learning between genders."""),
        ("Opportunity for Educational Innovation", """The significant segment that does use the Internet for 
        education (35.2% of men and 45.8% of women) represents a core of potential educational innovators. 
        This group could act as a catalyst for the wider adoption of digital learning 
        resources in the community.""")
    ]

    for title, description in patrones_internet:
        with st.expander(title):
            st.write(description)


    st.title("Strategic Implications for Circle Up Community")

    internet_implications = [
        "The low overall adoption of online learning signals a critical need for digital literacy programs and awareness of online educational resources.",
        "The gender disparity offers an opportunity to design volunteer initiatives that leverage and expand women's greater openness to digital learning.",
        "The segment of active internet users for education represents a valuable resource for the design and leadership of technology-based volunteer programs."
    ]

    for implication in internet_implications:
        st.markdown(f"- {implication}")

    st.title("Strategic Recommendations")

    internet_recommendations = [
        "Implement a **Digital Ambassadors** program utilizing the segment of active users to promote and teach online learning skills to their peers.",
        "Develop a micro-learning platform specifically for the Circle Up Community, gradually introducing VAs to online learning through relevant and accessible content.",
        "Establish partnerships with local businesses to promote and recognize professional development through online learning, incentivizing the adoption of these tools.",
        "Create a cross-mentorship program that leverages the greater female adoption of online learning to promote gender equity in digital skills."
    ]

    for recommendation in internet_recommendations:
        st.markdown(f"- {recommendation}")

    st.title("Future Research Perspectives")

    future_perspectives = [
        "Explore the specific barriers that hinder the adoption of online learning among VAs, considering factors such as access to technology, perceptions of usefulness, and learning preferences.",
        "Investigate the correlation between internet use for education and participation in volunteer activities, to inform more effective recruitment and retention strategies."
    ]

    for perspective in future_perspectives:
        st.markdown(f"- {perspective}")

    st.write("""
    This analysis reveals that Circle Up Community is uniquely positioned to catalyze an educational digital transformation in Tocancipá. By addressing the gap in internet use for education, Circle Up Community can not only improve the effectiveness of its volunteer programs but also contribute significantly to the development of local human capital, preparing the community for the challenges of the 21st-century knowledge economy.
    """)

    with st.expander("Social Networks: A Digital Bridge for VAs"):

        df_social_networks = pd.DataFrame({'Gender': ['Male', 'Male', 'Female', 'Female'],
                'Use of Social Networks': ['No', 'Yes', 'No', 'Yes'],
                'Sample': [1, 104, 0, 118],
                'Population Estimate': ['19-58', '1,654-2,415', '0-0', '1,904-2,712']
            })

        st.dataframe(df_social_networks, hide_index=True, use_container_width=True)

    st.write("""
    The table reveals an almost universal adoption of social networks among potential VAs, with crucial implications for Circle Up Community:
    """)

    social_network_findings = [
        ("Digital Saturation", """The 100% adoption among women and 99% among men indicates a saturation of the digital social space, creating a virtual ecosystem that is omnipresent in the lives of VAs."""),
        ("Minimal Gender Gap", """The marginal difference in adoption (1 male non-user) suggests digital gender equity in the social sphere, contrasting with the gap observed in the educational use of the internet.""")
    ]

    for title, description in social_network_findings:
        with st.expander(title):
            st.write(description)

    st.title("Social Network Strategy for Circle Up Community")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Strategic Implications", icon=":material/network_node:")
        st.success("1. Primary Communication Channel: Social networks emerge as the most effective means for disseminating information and recruiting VAs.", icon=":material/network_node:")
        st.success("2. Engagement Platform: Offers an ideal space to cultivate virtual communities of volunteers, facilitating coordination and the exchange of experiences.", icon=":material/network_node:")
        st.success("3. Micro-volunteering Tool: Enables the implementation of low-commitment but high-impact digital volunteer initiatives.", icon=":material/network_node:")
        st.success("4. Impact Amplifier: Provides a means for VAs to share their experiences, enhancing the multiplier effect of volunteering.", icon=":material/network_node:")

        st.success("Tactical Recommendations", icon=":material/network_node:")
        st.success("1. Develop a multi-platform content strategy that leverages the unique features of each social network.", icon=":material/network_node:")
        st.success("2. Implement digital storytelling campaigns to highlight the impact of volunteering through personal narratives of VAs.", icon=":material/network_node:")
        st.success("3. Create a digital ambassador program that leverages the social influence of the most active VAs on networks.", icon=":material/network_node:")
        st.success("4. Design viral challenges and hashtag campaigns that promote the visibility of Circle Up Community and its initiatives.", icon=":material/network_node:")

    with col2:
        st.success("Critical Considerations", icon=":material/network_node:")
        st.success("1. High adoption does not guarantee active engagement; it is crucial to develop content that resonates with the interests and values of VAs.", icon=":material/network_node:")
        st.success("2. Intensive use of social networks can lead to digital fatigue; Circle Up Community must balance its online presence with meaningful offline experiences.", icon=":material/network_node:")
        st.success("3. Data privacy and security must be prioritized in all digital interactions to maintain the trust of VAs.", icon=":material/network_node:")

        st.success("Research Opportunities", icon=":material/network_node:")
        st.success("1. Analyze the specific patterns of social network use among VAs to optimize the communication strategy.", icon=":material/network_node:")
        st.success("2. Explore the correlation between social media activity and propensity for volunteering to inform more effective recruitment strategies.", icon=":material/network_node:")

    st.write("""
    The ubiquity of social networks among VAs offers Circle Up Community a powerful channel to catalyze digital civic engagement. By strategically leveraging this virtual space, Circle Up Community can not only amplify its reach and impact but also redefine volunteering for the digital age, creating a model of community participation that is as dynamic and interconnected as the society it serves.
    """)

    st.title("Conclusions from the Demographic Analysis")

    st.write("""
    The demographic analysis of Tocancipá reveals a diverse and dynamic ecosystem, ideal for the implementation of Circle Up Community's programs. The population displays a combination of long-term residents and new migrants, creating a breeding ground for innovation and community development. The high levels of life and community satisfaction, along with a growing adoption of digital technologies, provide a solid foundation for volunteer and social innovation initiatives.

    The observed educational and occupational diversity offers a broad spectrum of skills and perspectives, crucial for addressing the multifaceted challenges of the community. However, significant gaps were also identified, particularly in the use of the internet for education and in female participation in certain sectors, which Circle Up Community can strategically address.
    """)

    st.title("Problem and Objective Trees")

    st.write("""
    This project utilizes problem and objective trees to analyze and address challenges in Tocancipá. It focuses on three areas: academic volunteering, reverse mentorships, and a social innovation lab. The study seeks to identify key problems, propose solutions, and develop strategies to enhance local human capital, foster intergenerational knowledge transfer, and promote community innovation.
    """)

    def mostrar_arbol(titulo, imagen_url, descripcion, tabla_data, implicaciones):
        st.title(titulo)

        fig1,fig2,fig3 = st.columns([1,2,1])
        fig2.image(imagen_url, use_column_width=True)
        st.write(descripcion)
        
        df = pd.DataFrame(tabla_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        with st.expander("Implications for Circle Up Community"):
            st.write(implicaciones)

    mostrar_arbol("Problem Tree - Academic Volunteering",
        "https://yuml.me/gocircleup/ap-va.svg",
        """
        The following problem tree analyzes the current situation of academic volunteering in Tocancipá. It identifies the underutilization of local human capital for the development of community skills as the central problem. This analysis reveals a series of interconnected causes that contribute to this situation, as well as the effects it has on the community.
        """,
        {
            "Nivel": ["Indirect Effects", "Direct Effects", "Central Problem", "Direct Causes", "Indirect Causes"],
            "Descripción": [
                "1. Stagnation in local socioeconomic development.\n2. Decrease in social cohesion and sense of community.",
                "1. Limited development of skills relevant to the local context.\n2. Underutilization of leadership potential in the community.",
                "Underutilization of local human capital in Tocancipá for the development of community skills.",
                "1. Absence of a structured system to channel the knowledge of local professionals.\n2. Disconnect between existing skills in the community and local needs.",
                "1.1. Lack of mechanisms to identify and mobilize local talent.\n1.2. Scarcity of incentives for participation in academic volunteer activities.\n2.1. Limited identification of the community's learning needs.\n2.2. Absence of a curriculum adapted to the local demographic characteristics."
            ]
        },
        """
        This problem tree suggests that Circle Up Community should focus on:
        1. Creating structured systems to identify and mobilize local talent.
        2. Developing effective incentives for volunteering.
        3. Designing curricula adapted to the specific needs of Tocancipá.
        4. Implementing mechanisms to identify the community's learning needs.

        Addressing these aspects could lead to a better utilization of local human capital and, consequently, to a greater development of community skills.
        """
    )

    # Objective Tree - VA
    mostrar_arbol("Objective Tree - Academic Volunteering",
        "https://yuml.me/gocircleup/ao-va.svg",
        """
        The following objective tree presents a structured vision to optimize the utilization of local human capital in Tocancipá. This approach seeks to transform the problems identified in the problem tree into achievable objectives and concrete means to achieve them.
        """,
        {
            "Nivel": ["Indirect Goals", "Direct Goals", "Overall Objective", "Specific Objectives", "Means"],
            "Descripción": [
                "1. Improvement in local socioeconomic development.\n2. Strengthening of social cohesion and sense of community.",
                "1. Increase in the acquisition of skills relevant to the local context.\n2. Increase in the number of trained community leaders.",
                "Optimize the utilization of local human capital for the development of community skills in Tocancipá.",
                "1. Implement a structured system of academic volunteering.\n2. Align local skills with the needs of the community.",
                "1.1. Develop a platform for the identification and management of volunteers.\n1.2. Establish a recognition system for academic volunteers.\n2.1. Conduct an ongoing analysis of the community's learning needs.\n2.2. Design a flexible curriculum based on local demographic characteristics."
            ]
        },
        """
        To achieve these objectives, Circle Up Community could consider the following strategies:
        1. Develop a digital platform to connect volunteers with teaching opportunities.
        2. Implement a system of badges or certifications to recognize the work of volunteers.
        3. Conduct regular surveys and focus groups to identify learning needs.
        4. Collaborate with local experts to design an adaptive and relevant curriculum.

        These strategies seek to create an efficient academic volunteering ecosystem aligned with the needs of Tocancipá.
        """
    )

    st.title("References")

    st.info("""
    This chapter presents an exhaustive list of the references used in this research project. The sources are organized in a table that includes the citation in APA format and a direct link to the original document when available. This compilation reflects the diversity and depth of the literature consulted, encompassing topics such as educational technology, lifelong learning, social innovation, and research methodologies.
    """, icon=":material/hiking:")






    referencias = pd.DataFrame([
        {"Referencia (APA)": "Álvarez, M., Gardyn, N., Iardelevsky, A., & Rebello, G. (2020). Segregación Educativa en Tiempos de Pandemia: Balance de las Acciones Iniciales durante el Aislamiento Social por el Covid-19 en Argentina. Revista Internacional de Educación para la Justicia Social, 9(3).", "Enlace": "https://drive.google.com/file/d/15MGMS96FzBvBJIxXRq4ua4VPpv8uJQ9H/view?usp=sharing"},
        {"Referencia (APA)": "American Educational Research Association. (2011). Code of Ethics. Educational Researcher, 40(3), 145-156.", "Enlace": "Sin Referencia"},
        {"Referencia (APA)": "Avello Martínez, R., Lavonen, J., & Zapata-Ros, M. (2022). Emerging Technologies in Education for Innovative Pedagogies and Competence Development. Sustainability, 37(5), 1723.", "Enlace": "https://drive.google.com/file/d/1HMZ_KbCVAg2HA48fPz9olCy6J4P4eMet/view?usp=sharing"},
        {"Referencia (APA)": "Bayne, S. (2015). What's the matter with 'technology-enhanced learning'? Learning, Media and Technology, 40(1), 5-20.", "Enlace": "https://drive.google.com/file/d/1iruNdNa_nDHPV2QDT7mQhPfkKI4C8gHf/view?usp=sharing"},
        {"Referencia (APA)": "Binkley, M., Erstad, O., Herman, J., Raizen, S., Ripley, M., Miller-Ricci, M., & Rumble, M. (2012). Defining twenty-first century skills. In P. Griffin, B. McGaw, & E. Care (Eds.), Assessment and teaching of 21st century skills (pp. 17-66).", "Enlace": "https://drive.google.com/file/d/1f2Di-Mx4HC9dchfucEY4oDdsl04Bzoke/view?usp=sharing"},
        {"Referencia (APA)": "Bond, M., Marín, V. I., Dolch, C., Bedenlier, S., & Zawacki-Richter, O. (2020). Digital transformation in German higher education: student and teacher perceptions and usage of digital media. International Journal of Educational Technology in Higher Education, 17(1), 1-21.", "Enlace": "https://drive.google.com/file/d/1Cw-CINpDMY_RfJjn3t5HEGyOIQDY8gV8/view?usp=sharing"},
        {"Referencia (APA)": "Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. Qualitative Research in Psychology, 3(2), 77-101.", "Enlace": "Sin Referencia"},
        {"Referencia (APA)": "Bringle, R. G., & Clayton, P. H. (2020). Integrating Service Learning and Digital Technologies: Examining the Challenge and the Promise. RIED. Revista Iberoamericana de Educación a Distancia, 23(1), 43-65.", "Enlace": "https://drive.google.com/file/d/1AtW5571ZP7oTF3Cg169BamBBw1T802D4/view?usp=sharing"},
        {"Referencia (APA)": "British Council. (n.d.). [Título del documento].", "Enlace": "https://drive.google.com/file/d/1iZluoOuZHqTov3FzIdtAHA2K7wbzhu4a/view?usp=sharing"},
        {"Referencia (APA)": "Brown, P., Lauder, H., & Cheung, S. Y. (2020). The Death of Human Capital?: Its Failed Promise and How to Renew It in an Age of Disruption. Oxford University Press.", "Enlace": "https://drive.google.com/file/d/15ZXERFpEw9UaAlLKdKw8hSo-gse0ZDUK/view?usp=sharing"},
        {"Referencia (APA)": "Crompton, H., & Burke, D. (2018). The use of mobile learning in higher education: A systematic review. Computers & Education, 123, 53-64.", "Enlace": "https://drive.google.com/file/d/1SAtVNFP28Q7C2q3fjuwaOgKjyTc-DG2D/view?usp=sharing"},
        {"Referencia (APA)": "DANE. (2021). Encuesta Multipropósito Bogotá - Cundinamarca - EM - 2021 Colombia.", "Enlace": "https://microdatos.dane.gov.co/index.php/catalog/743/get-microdata"},
        {"Referencia (APA)": "Desjardins, R. (2019). The political economy of adult learning systems - Some institutional features that promote adult learning participation.", "Enlace": "https://drive.google.com/file/d/1_EeboCgjQvPoJ4rCFST4zWrx_1UT4eVf/view?usp=sharing"},
        {"Referencia (APA)": "Findsen, B., & Formosa, M. (2011). Lifelong learning in later life: A handbook on older adult learning. Sense Publishers.", "Enlace": "https://drive.google.com/file/d/1aQDJGSZ8KcO_Pr3y2eAMTXq8iho-ddNd/view?usp=sharing"},
        {"Referencia (APA)": "Gerpott, F. H., Lehmann-Willenbrock, N., & Voelpel, S. C. (2017). A phase model of intergenerational learning in organizations. Academy of Management Learning & Education, 16(2), 193-216.", "Enlace": "https://drive.google.com/file/d/1QVtNCG5NiArgVDbs0UmjJ9PYJEN73Kmj/view?usp=sharing"},
        {"Referencia (APA)": "Giraudeau, C., & Bailly, N. (2019). Intergenerational programs: What can school-age children and older people expect from them? A systematic review. European Journal of Ageing, 16(3), 363-376.", "Enlace": "https://drive.google.com/file/d/1d2ne4AxNIk7s3sGx0W0KfUsRx1TS4TKy/view?usp=sharing"},
        {"Referencia (APA)": "Howaldt, J., Kaletka, C., Schröder, A., & Zirngiebl, M. (2018). Atlas of Social Innovation: New Practices for a Better Future. Sozialforschungsstelle, TU Dortmund University.", "Enlace": "https://drive.google.com/file/d/1hb1QJAdgbKuD0dBe8VLKwK204Exip1U7/view?usp=sharing"},
        {"Referencia (APA)": "Krlev, G., Anheier, H. K., & Mildenberger, G. (2021). Social Innovation in a Comparative Perspective. Routledge.", "Enlace": "https://drive.google.com/file/d/15vxPkw_sIhMr2HlqwUeT6qUM07VRcrxV/view?usp=sharing"},
        {"Referencia (APA)": "Laal, M., & Salamati, P. (2012). Lifelong learning; why do we need it? Procedia-Social and Behavioral Sciences, 31, 399-403.", "Enlace": "https://drive.google.com/file/d/1GpNnZdehT8Hdo_eVSVPV0Gpzp0WrA7Mr/view?usp=sharing"},
        {"Referencia (APA)": "Lugo, M. T., & Ithurburu, V. (2019). Políticas digitales en América Latina. Tecnologías para fortalecer la educación de calidad. Revista Iberoamericana de Educación, 79(1), 11-31.", "Enlace": "https://drive.google.com/file/d/10lMOy3yw0_lqAXnYu0kskeNDEvtnAsGy/view?usp=sharing"},
        {"Referencia (APA)": "Moulaert, F., & MacCallum, D. (2019). Advanced Introduction to Social Innovation. Edward Elgar Publishing.", "Enlace": "https://drive.google.com/file/d/1SvwHR_sRLyuU4W4CLQlF9_949sza3nCb/view?usp=sharing"},
        {"Referencia (APA)": "Pel, B., Haxeltine, A., Avelino, F., Dumitru, A., Kemp, R., Bauler, T., Kunze, I., Dorland, J., Wittmayer, J., & Jørgensen, M. S. (2020). Towards a theory of transformative social innovation: A relational framework and 12 propositions. Research Policy, 49(8), 104080.", "Enlace": "https://drive.google.com/file/d/12byZo62RW4uZKEdiAY83RDaSf7ftCY8C/view?usp=sharing"},
        {"Referencia (APA)": "Powell, W. W., & Snellman, K. (2004). The knowledge economy. Annual Review of Sociology, 30, 199-220.", "Enlace": "https://drive.google.com/file/d/1ei9ecK9vyy5ZnCrluJyzxNPgmADne7K0/view?usp=sharing"},
        {"Referencia (APA)": "Stoecker, R. (2016). Liberating service learning and the rest of higher education civic engagement. Temple University Press.", "Enlace": "https://drive.google.com/file/d/1ZKX1cdCEkjNZ7j0VxpM5W35RdIFHED0h/view?usp=sharing"},
        {"Referencia (APA)": "van Wijk, J., Zietsma, C., Dorado, S., de Bakker, F. G., & Martí, I. (2019). Social innovation: Integrating micro, meso, and macro level insights from institutional theory. Business & Society, 58(5), 887-918.", "Enlace": "https://drive.google.com/file/d/1hqny6lDE1wvCKxOuTDhVmWxbJeB21qdH/view?usp=sharing"},
        {"Referencia (APA)": "World Economic Forum. (2023). The Future of Jobs Report 2023.", "Enlace": "https://drive.google.com/file/d/1DkS32l0KuXITMWx0XcBsI3dY5sXOt8-d/view?usp=sharing"},
        {"Referencia (APA)": "Yin, R. K. (2018). Case Study Research and Applications: Design and Methods (6th ed.). Sage Publications.", "Enlace": "Sin Referencia"},
        {"Referencia (APA)": "Zawacki-Richter, O., Marín, V. I., Bond, M., & Gouverneur, F. (2019). Systematic review of research on artificial intelligence applications in higher education – where are the educators? International Journal of Educational Technology in Higher Education, 16(1), 39.", "Enlace": "https://drive.google.com/file/d/1O0QOlx800iGfgHLguJXKoieFda8XISdf/view?usp=sharing"}
    ])


    html_table = create_html_table(referencias)
    st.markdown(html_table, unsafe_allow_html=True)


    st.info("""
    Some references do not have associated links and are indicated as **No Reference** in the link column. For these entries, it is recommended to search for the original source or create a complete reference based on the available information.
    """, icon=":material/bubble_chart:")

    st.write("""
    This list of references provides a solid foundation for the research project, covering a wide range of topics relevant to Circle Up. The diversity of sources consulted ensures a comprehensive and up-to-date perspective on the challenges and opportunities in the field of academic volunteering, reverse mentoring, and social innovation.

    Readers interested in delving deeper into specific topics can directly access the original sources through the links provided, thus facilitating the verification and expansion of the information presented in this study.
    """)