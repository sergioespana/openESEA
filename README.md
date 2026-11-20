# openESEA

**An open-source, model-driven framework for ethical, social and environmental accounting.**

> **Project status: development is moving to Show your Heart.** Development of the standalone openESEA application is being wound down. We have joined forces with *Enseña el Corazón* / *Ensenya el Cor*, internationally branded as **Show your Heart**. This repository is retained as a reference implementation and a record of the research, modelling language and experimental features developed within openESEA. For the continuing project, see the [Show your Heart website](https://showyourheart.sites.uu.nl/).

openESEA helps organisations assess and report on their ethical, social and environmental performance. It supports the specification and application of accounting methods: the topics to assess, the questions to ask stakeholders, the indicators to calculate and the ways to present the results. This domain is also commonly described as sustainability accounting or environmental, social and governance (ESG) accounting.

Many software tools support a single accounting method. openESEA takes a different approach: methods are represented as models that a common software platform interprets. This allows method designers to specify and tailor methods without developing a separate application for each one.

The project brings together a domain-specific modelling language, a web-based interpreter and research prototypes for comparing methods, supporting audits and designing reporting dashboards.

## How it works

1. **Specify a method.** Define its topics, direct indicators, calculated indicators, surveys and questions using the openESEA modelling language or the interpreter's method-editing interfaces.
2. **Apply the method.** Register organisations and networks, organise reporting campaigns and collect data through stakeholder surveys. An *ESE account* records an organisation's application of a method for a particular reporting period.
3. **Calculate and communicate results.** Calculate indicators from the collected data, review the account and present results through reporting interfaces and dashboards.

For example, a method might collect annual electricity consumption and the number of employees as direct indicators, then calculate electricity consumption per employee as an indirect indicator. These definitions belong to the method model, while the values supplied by an organisation belong to its account.

## Repository contents

| Component | Purpose | Start here |
| --- | --- | --- |
| **openESEA modelling language** | A textual domain-specific language (DSL) for specifying accounting methods. The grammar includes topics, indicators, formulas, surveys, validation rules, certification levels and dashboard constructs. | [Xtext grammar](openESEA%20DSL/Dsl.xtext) |
| **openESEA interpreter** | A Django/Python and Vue.js web application for managing methods, organisations, networks, surveys, accounts, audits and dashboards. | [Interpreter README](openESEA_interpreter/README.md) |
| **Model management** | A separate notebook-based prototype for matching and merging method fragments using language models, similarity measures and transformation rules. Its aim is to reduce repeated data collection when organisations apply multiple methods. | [Model-management README](openESEA%20model%20management/README.md) |
| **Dashboard recommendation evaluation** | Scripts, input dashboards and results for evaluating the reinforcement-learning-based dashboard recommender. | [Evaluation README](RL_Evaluation/README.md) and [methodology](RL_Evaluation/METHODOLOGY.md) |

## Capabilities and development status

This repository contains a research implementation and associated experimental components. Their coverage and maturity differ.

The interpreter includes functionality for:

- Managing organisations, networks and their members.
- Creating, importing and editing accounting methods, including topics, direct and indirect indicators, surveys and questions.
- Organising campaigns and collecting responses through surveys within the application.
- Calculating indicators from survey responses and formulas.
- Supporting audit workflows, including auditor assignment, response sampling, review and assurance declarations, alongside experimental analytical support for selecting information to audit.
- Creating and editing model-driven dashboards with tables, value displays, progress indicators and charts.
- Suggesting dashboard modifications through an experimental reinforcement-learning model.

The model-management notebooks run separately from the web application. Suggested matches and merges require domain review: textual similarity alone does not establish that two indicators measure the same thing.

The modelling language and interpreter have evolved through several versions. **A construct in the grammar or a feature described in a publication is not necessarily supported by the current interpreter.** Check the [interpreter documentation](openESEA_interpreter/README.md#method-models-and-compatibility) when preparing models. Earlier implementations also supported infographic generation and certification checking; their presence in earlier publications should not be read as a claim of feature parity in this version.

## Getting started

- **For the continuing impact-measurement platform:** visit [Show your Heart](https://showyourheart.sites.uu.nl/).
- **To explore the approach:** read the [2023 language and tool paper](https://doi.org/10.7250/csimq.2023-34.01) and the [modelling-language technical report](https://arxiv.org/abs/2205.15279).
- **To run this research implementation:** follow the [interpreter setup instructions](openESEA_interpreter/README.md#local-development-setup).
- **To investigate method comparison:** use the [model-management documentation](openESEA%20model%20management/README.md) and notebooks.
- **To investigate dashboard recommendations:** consult the [evaluation methodology](RL_Evaluation/METHODOLOGY.md).

## Background and collaboration

openESEA originated at Utrecht University within the Software for Organisational Responsibility research line. Its development combines research on sustainability accounting, conceptual modelling, domain-specific languages and software engineering, with contributions from researchers, students, software developers and practitioners.

The original JavaScript/React and Firebase implementation is available in a [separate repository](https://github.com/sergioespana/open-sea). This repository contains the later Django/Python and Vue.js implementation and related research artefacts. These are distinct implementations, rather than Git branches with identical functionality.

Collaboration with Universitat Politècnica de València was supported by a María Zambrano grant awarded to Sergio España by the Spanish Ministry of Universities, co-funded by the Next Generation EU recovery programme. The research has also been connected to the NWO-funded [SCENTISS project](https://scentiss.nl/).

### From openESEA to Show your Heart

openESEA has joined forces with *Enseña el Corazón* / *Ensenya el Cor*, the impact-measurement platform associated with REAS Red de Redes de Economía Alternativa y Solidaria and Xarxa d'Economia Solidària (XES). The shared project is internationally branded as **Show your Heart**.

The collaboration brings together openESEA's research on conceptual modelling, accounting-method specification, auditing and reporting with an established platform used by social and solidarity economy organisations. The agreed technical direction builds on the Enseña el Corazón platform and technology stack, drawing on openESEA's conceptual foundations and research results to guide its evolution and additional features.

This repository preserves the standalone openESEA implementations and research artefacts. It is not the Show your Heart application codebase, and the transition does not imply that every experimental feature here has already been transferred to the shared platform.

See the [Show your Heart project website](https://showyourheart.sites.uu.nl/), [project history](https://showyourheart.sites.uu.nl/home/history/) and [participating organisations](https://showyourheart.sites.uu.nl/home/stakeholders/) for further information.

## Research and citation

If you use openESEA in research, please cite the language and tool paper, and the publications relevant to the components you use. Record the repository URL and commit identifier for reproducibility.

### Core publications

- Ramautar, V., & España, S. (2023). **The OpenESEA Modeling Language and Tool for Ethical, Social, and Environmental Accounting.** *Complex Systems Informatics and Modeling Quarterly*, 34, 1–29. [DOI](https://doi.org/10.7250/csimq.2023-34.01).
- España, S., Bik, N., & Overbeek, S. (2019). **Model-driven engineering support for social and environmental accounting.** *Research Challenges in Information Science (RCIS).* [DOI](https://doi.org/10.1109/RCIS.2019.8877042).
- España, S., Ramautar, V., Overbeek, S., & Derikx, T. (2022). **Model-driven production of data-centric infographics: An application to the impact measurement domain.** *Research Challenges in Information Science (RCIS)*, 477–494. [DOI](https://doi.org/10.1007/978-3-031-05760-1_28). Describes the infographic work in the earlier implementation.

### Further reading

- España, S., & Ramautar, V. (2024). **The openESEA modelling language for specifying environmental, social and governance accounting methods, version 4.** [Technical report](https://arxiv.org/abs/2205.15279).
- Ramautar, V., España, S., & Brinkkemper, S. (2023). **Task Completeness Assessments in the Evolution of Domain-Specific Modelling Languages.** *CAiSE*, 314–329. [DOI](https://doi.org/10.1007/978-3-031-34560-9_19).
- Ramautar, V., Ritfeld, N., Brinkkemper, S., & España, S. (2024). **Optimising Sustainability Accounting: Using Language Models to Match and Merge Survey Indicators.** *RCIS*, 338–354. [DOI](https://doi.org/10.1007/978-3-031-59465-6_21).
- España, S., Ramautar, V., Martín, S., Thorsteinsdottir, G., Sinaga, Y. A., & Pastor, Ó. (2024). **Why and How Responsible Organisations Are Assessing Their Performance: State of the Practice in Environmental, Social and Governance Accounting.** *Advances in Performance Management and Measurement for Industrial Applications and Emerging Domains*, 13–56. [DOI](https://doi.org/10.1007/978-3-031-59930-9_2).
- Ramautar, V. (2024). **Model-driven sustainability accounting.** Doctoral dissertation, Utrecht University. ISBN 9789039377130.

Related MSc research includes Tijmen Derikx's work on infographic generation; Ties van Dijk's and Artur Moeijes's work on audit workflows and analytical support; Noah Ritfeld's work on method matching and merging; and Marc de Fluiter's work on model-driven dashboards and reinforcement-learning-based recommendations.

## Contributors

The following people and organisations have contributed to the project across its different implementations and research activities. Roles describe their contributions over time.

| Contributor(s) | Contribution |
| --- | --- |
| Sergio España | Project leadership, research direction, requirements engineering and supervision. |
| Vijanti Ramautar | Product ownership, doctoral research, modelling-language development and supervision of extensions. |
| Sietse Overbeek | Research and supervision of several tool features. |
| Óscar Pastor | Scientific advice, requirements engineering and conceptual modelling. |
| Niels Bik | First implementation, including organisations, networks and runtime interpretation of method specifications. |
| Henny Kruiper | Stakeholder survey specification and delivery in the earlier implementation. |
| Tijmen Derikx | Model-driven infographic specification and generation. |
| Diederik van Rijen | Integration of earlier development lines and usability improvements. |
| Ties van Dijk | Audit workflow functionality. |
| Artur Moeijes | Analytical support for auditing accounts. |
| Noah Ritfeld | Automated matching and merging of method models. |
| Marc de Fluiter | Dashboard modelling, rendering and reinforcement-learning-based recommendations. |
| Sara Martín, Yulie Anneria Sinaga and Gudrun Thorsteinsdottir | Domain knowledge on accounting methods, research and valorisation. |
| Competa IT: Jelle Verschragen, Tjeerd Verschragen, Tino Trok, Matthew Kunkeler, Michiel Auerbach and Andy Haxby | Interface design, software development and project support for the later implementation. |

If your contribution is missing or needs correcting, please open an issue.

## Research use and contact

For current development, adoption and collaboration, please refer to [Show your Heart](https://showyourheart.sites.uu.nl/).

For questions about openESEA's research and the artefacts retained here, contact Sergio España at [s.espana@uu.nl](mailto:s.espana@uu.nl). [GitHub issues](https://github.com/sergioespana/openESEA/issues) can be used to document problems reproducing the research implementation.

When reporting a problem, include the component, commit identifier, steps to reproduce it and a small example where possible. Use synthetic or anonymised data in public issues.

## Licensing

Original openESEA source code in this repository, including the modelling-language grammar, interpreter, model-management notebooks and evaluation scripts, is licensed under the **GNU Affero General Public License, version 3** (`AGPL-3.0-only`), except where an applicable file or component notice states otherwise. See [LICENSE](LICENSE) and the [licensing guide](LICENSING.md).

Third-party libraries and other third-party materials retain their own licences and copyright notices. In particular, Apache ECharts is licensed under Apache 2.0; this applies to ECharts, not to the original openESEA frontend code. See the [frontend third-party notices](openESEA_interpreter/frontend/public/THIRD_PARTY_NOTICES.txt) for the charting dependencies and their preserved upstream licence files.
