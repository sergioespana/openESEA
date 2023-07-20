openESEA is a model-driven ethical, social and environmental accounting tool. 

This project is steered by University of Utrecht. We welcome collaboration with organisations and individuals. A tight collaboration with Universitat Politècnica de València has started in 2023.

If you want to cite this tool, please also cite this scientific papers:
 - España, S., Bik, N., & Overbeek, S. (2019, May). Model-driven engineering support for social and environmental accounting. In 2019 13th International Conference on Research Challenges in Information Science (RCIS) (pp. 1-12). IEEE, https://doi.org/10.1109/RCIS.2019.8877042
 - España, S., Ramautar, V., Overbeek, S., & Derikx, T. (2022, May). Model-driven production of data-centric infographics: An application to the impact measurement domain. In International Conference on Research Challenges in Information Science. Springer, pp. 477-494, https://doi.org/10.1007/978-3-031-05760-1_28
 - Ramautar, V., & España, S. (2023). The OpenESEA Modeling Language and Tool for Ethical, Social, and Environmental Accounting. Complex Systems Informatics & Modeling Quarterly, (34).

The tool has a front end and a back end. Each folder has a readme file that explains the installation procedure.

At this very moment, there are two branches of this tool:
(i) The branch found in https://github.com/sergioespana/open-sea is developed in Javascript and Firestore. It is the original first version of the tool and it includes features to manage networks and organisations, load textual specifications of ESEA methods and interpret them in runtime (e.g. deploying stakeholder surveys asking questions relater to an organisation's non-financial performance, calculating indicators that represent such performance better, generating infographics that summarise the results, checking the compliance of the results with certification rules to determine whether the organisation achieves the certification). The textual models are compliant with the openESEA domain-specific language.
(ii) This branch, found in https://github.com/sergioespana/openESEA is developed in Django/Python. It was initially programmed by Competa IT, with guidance and requirements input from Utrecht University. The architecture is more secure and scalable, but it has less features than earlier versions. As an advantage, it allows specifying the ESEA methods with usable user interfaces, and the stakeholder surveys are deployed within the tool, without the need of LimeSurvey. As disadvantages, it has no infographic generation or certification rule checking. In later development iterations, we have included features related to auditing and assurance of social and environmental accounts. We are currently implementing features related to model management operations and automatic dashboard generations.

We are currently in the process of re-implementing the features of the earlier versions into this later version, so as to have the best of each branch.


If you want to collaborate in this project, please contact us.

Some of the current and past project members:
Sergio España, Assistant Professor in Utrecht University, is the project leader and manager. Sergio is a visiting researcher in Universitat Politècnica de València during 2023 and 2024, supported by a María Zambrano grant of the Spanish Ministry of Universities, co-funded by the Next Generation EU European Recovery Plan.
Vijanti Ramautar, doctoral researcher in Utrecht University is the product owner. 
Sietse Overbeek, Assistant Professor in Utrecht University, has supervised the development of some features of the tool.
Niels Bik developed the first version, including features to register organisations and networks, specify basic method components such as topics and indicators, and interpret the method specifications in runtime; his code is kept in a separate github repository https://github.com/nielsrowinbik/open-sea
Henny Kruiper developed a feature to specify and deliver stakeholder surveys; his code is kept in a separate github repository https://github.com/nielsrowinbik/open-sea
Tijmen Derikx developed a feature to specify and automatically generate infographics that present the account results; ; his code is kept in a separate github repository https://github.com/nielsrowinbik/open-sea
Diederik van Rijen has merged branches (i) and (ii) onto a new version of the tool, retaining most of the features from each branch and improving the usability. 
Jelle Verschragen (user interface designer), Tjeerd Verschragen (user interface developer), Tino Trok (backend developer), Matthew Kunkeler (business manager), Michiel Auerbach (project manager), Andy Haxby (Director at Competa), all contributed to the development of the tool while working for Competa IT https://competa.com
Sara Martín, Yulie Anneria Sinaga and Gudrun Thorsteinsdottir contributed theoretical knowledge on ESEA methods that is valuable for the tool development and valorisation.
Ties van Dijk and Artur Moeijes have extended openESEA with features to audit accounts.
Óscar Pastor, full professor in Universitat Politècnica de València, acts as scientific advisor, requirements engineer and conceptual modeller within the project.


If we are forgetting you, please contact us and we will update this list ;-)
