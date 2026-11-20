# openESEA interpreter

> **Legacy research implementation.** Development of the standalone openESEA application is being wound down as the project continues through **[Show your Heart](https://showyourheart.sites.uu.nl/)**, following the collaboration with Enseña el Corazón / Ensenya el Cor. This directory preserves the Django/Vue implementation for research and reproducibility. See the [main README](../README.md#from-openesea-to-show-your-heart) for the transition and the relationship between the codebases.

The openESEA interpreter is the web application of the [openESEA framework](../README.md). It turns accounting-method specifications into interfaces for collecting stakeholder responses, calculating indicators and reviewing and reporting an organisation's ethical, social and environmental performance.

This directory contains the Django/Python backend and Vue.js frontend. For the project's motivation, history, publications and contributors, see the [main README](../README.md).

## Functionality

The application contains features for:

- Managing organisations, networks, users and memberships.
- Creating and editing methods, topics, indicators, surveys, sections, questions and explanatory text.
- Importing textual method specifications.
- Managing reporting campaigns and organisations' ESE accounts.
- Delivering stakeholder surveys and storing responses within the application.
- Calculating indirect indicators using formulas and collected responses.
- Supporting account and survey audits, including auditor assignment, sampling, review and assurance declarations.
- Defining, editing, saving and rendering reporting dashboards.
- Generating experimental dashboard-editing recommendations using reinforcement learning.

This is a research implementation. Audit analytics and dashboard recommendations are experimental; their presence in the code does not imply comprehensive validation for operational use. Dashboard recommendations have been evaluated in research, but an improvement in users' comprehension has not been established.

## Architecture and source code

| Location | Contents |
| --- | --- |
| [`backend/`](backend/) | Django application, Django REST Framework API and Python dependencies. |
| [`backend/django_backend/`](backend/django_backend/) | Project settings, top-level URL configuration and server entry points. |
| [`backend/core/models/`](backend/core/models/) | Methods, indicators, organisations, surveys, responses, accounts, audits and dashboards. |
| [`backend/core/views/`](backend/core/views/) | API views, including method import, account auditing and dashboard suggestions. |
| [`backend/core/utils/`](backend/core/utils/) | Method processing, indicator calculations and audit analytics. |
| [`backend/core/DashboardRLModel/`](backend/core/DashboardRLModel/) | Reinforcement-learning environment and recommendation model. |
| [`backend/core/tests/`](backend/core/tests/) | Existing backend tests. |
| [`frontend/`](frontend/) | Vue 3 application, with Vue Router, Vuex and PrimeVue. |
| [`frontend/src/components/dashboard/`](frontend/src/components/dashboard/) | Dashboard rendering, editing and visualisation components. |

The backend uses PostgreSQL and exposes REST endpoints. The frontend communicates with it through Axios; API authentication uses JSON Web Tokens (JWT). Dashboard recommendations use PyTorch in the backend. Chart rendering uses JavaScript charting libraries in the frontend.

## Local development setup

These instructions are for exploring or reproducing this research implementation. The continuing project's information is available at [Show your Heart](https://showyourheart.sites.uu.nl/).

The instructions below describe the configuration expected by the checked-in source. Dependencies span several development iterations and are not fully locked, so installation may require compatibility adjustments. The frontend manifest declares Node.js `16.x` and npm `8.x`; the Python requirements include a pinned PyTorch version alongside minimum versions for many other packages. These do not constitute a verified compatibility matrix for current platforms.

### 1. Get the source

```bash
git clone https://github.com/sergioespana/openESEA.git
cd openESEA/openESEA_interpreter
```

Install PostgreSQL and prepare a Python environment compatible with [`backend/requirements.txt`](backend/requirements.txt). Use the Node.js and npm versions declared in [`frontend/package.json`](frontend/package.json) when reproducing the existing frontend environment.

### 2. Prepare the backend environment

From `openESEA_interpreter/`:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

Create a fresh virtual environment rather than using the committed `venv_esea2` directory.

### 3. Create a PostgreSQL database

Connect to PostgreSQL with an administrator account and create a development role and database. Replace the example password before executing:

```sql
CREATE ROLE esea_user WITH LOGIN PASSWORD 'replace_with_a_local_password';
CREATE DATABASE esea_db OWNER esea_user ENCODING 'UTF8';
```

### 4. Configure the backend

Create `backend/.env` with values for your local environment:

```dotenv
SECRET_KEY=replace_with_a_random_local_secret
DATABASE_URL=postgres://esea_user:replace_with_a_local_password@127.0.0.1:5432/esea_db
```

Use a URL-encoded password in `DATABASE_URL` if it contains reserved URL characters. Keep your local environment files out of version control.

[`django_backend/settings.py`](backend/django_backend/settings.py) loads environment variables with `python-dotenv`. `SECRET_KEY` is required. `DATABASE_URL` overrides the database connection defaults in that file; without it, the code falls back to a local PostgreSQL database named `esea_db` and the hard-coded development credentials.

For local exploration without sending emails, set the following in your local Django settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This prints outgoing email content, including survey invitations, to the backend terminal. If you need actual email delivery, configure your own SMTP service in the settings.

### 5. Initialise and start the backend

With the virtual environment active, from `backend/`:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The backend normally runs at `http://127.0.0.1:8000/`; Django administration is available at `http://127.0.0.1:8000/admin/`.

The repository contains historical data fixtures. Load a fixture only after checking that it matches the current schema and is appropriate for your local database.

### 6. Configure and start the frontend

In a separate terminal, from `openESEA_interpreter/frontend/`, create `.env.local`:

```dotenv
VUE_APP_ROOT_API=http://127.0.0.1:8000/
```

Then install the dependencies and start the development server:

```bash
npm install
npm run serve
```

Open the address printed by the frontend development server, normally `http://localhost:8080/`. Keep the backend running in the other terminal. Restart the frontend server after changing its environment variables.

### Development commands

| Purpose | Directory | Command |
| --- | --- | --- |
| Run the existing backend tests | `backend/` | `python manage.py test` |
| Apply database migrations | `backend/` | `python manage.py migrate` |
| Create migrations after intentional model changes | `backend/` | `python manage.py makemigrations` |
| Build the frontend | `frontend/` | `npm run build` |
| Run the frontend linter, which can modify files | `frontend/` | `npm run lint` |

The checked-in settings contain development defaults, including debug mode and permissive CORS configuration. A frontend build alone is not a production deployment procedure; review the backend settings, credentials, permissions and dependency versions before deploying.

## Method models and compatibility

The framework's [Xtext grammar](../openESEA%20DSL/Dsl.xtext) defines the textual modelling language. The interpreter currently uses its own [textual method processor](backend/core/utils/process_textual_method.py) for method uploads. It does not execute the Xtext grammar directly.

The grammar and importer do not have identical coverage. In particular, the importer processes method metadata, topics, indicators and surveys, while the grammar also contains newer constructs and constraints. Check the importer before assuming that a complete model created for a particular language version will load correctly. Keyword spelling, capitalisation and the order of elements matter to the current processor. It currently decodes uploaded method files as Windows-1252 (`cp1252`).

The framework distinguishes:

- **Direct indicators:** values collected through survey questions.
- **Indirect indicators:** values calculated from direct or other indirect indicators using formulas.
- **Method models:** definitions of what to assess and how to collect and calculate it.
- **ESE accounts:** the application of a method to an organisation for a reporting period, including its collected data and results.

The separate [model-management prototype](../openESEA%20model%20management/README.md) performs method matching and merging through notebooks. It is not an integrated workflow in this web application.

## Dashboards and recommendations

Dashboard specifications are stored as JSON in the backend. The frontend offers visual editing and a YAML-based text-editing interface, as well as dashboard specification import and JSON download.

The dashboard implementation includes multiple overviews, containers, text and visualisations such as tables, single and fractional values, progress indicators, pie charts, bar charts and line charts. The implementation covers a subset of the features described by the broader dashboard model; filters, images and other advanced features should not be assumed to be available.

The experimental recommender proposes modifications such as changing visualisation types and adjusting data-item limits. Its suggestions support user review rather than establishing that a dashboard is optimal. For the recommendation model, reward functions, evaluation scripts and results, see the [evaluation documentation](../RL_Evaluation/README.md) and [methodology](../RL_Evaluation/METHODOLOGY.md).

## Earlier implementations

The original [JavaScript/React and Firebase implementation](https://github.com/sergioespana/open-sea) includes work on infographic generation and certification checking. This Django/Vue implementation has a different architecture and feature set. Consult the relevant implementation when reproducing results from older publications.

## Contributing, citation and licensing

For contributors, research references and collaboration details, see the [main README](../README.md). Report reproducible problems through [GitHub issues](https://github.com/sergioespana/openESEA/issues), indicating the interpreter version or commit and using synthetic or anonymised examples.

Original openESEA interpreter code, including the backend and frontend, is licensed under the **GNU Affero General Public License, version 3** (`AGPL-3.0-only`). See [LICENSE.txt](LICENSE.txt) and the [repository licensing guide](../LICENSING.md).

Apache ECharts and other dependencies retain their own licences. The Apache licence applies to ECharts, not to the original openESEA frontend code. See the [frontend third-party notices](frontend/public/THIRD_PARTY_NOTICES.txt). These notices and the licence files under `frontend/public/licenses/` are copied into standard Vue CLI builds; retain them when distributing the built application.
