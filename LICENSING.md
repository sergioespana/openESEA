# Licensing of openESEA

## Original project code

Original openESEA source code is licensed under the GNU Affero General Public License, version 3 (`AGPL-3.0-only`), except where an applicable file or component notice states otherwise. This covers the original modelling-language grammar, interpreter backend and frontend, model-management notebooks and evaluation scripts. The full licence text is in [LICENSE](LICENSE).

This records version 3 of the licence; it does not add permission to use a later licence version. Any existing, explicit permission attached to a particular contribution remains applicable. Copyright remains with the respective rights holders; this clarification does not transfer ownership or replace attribution notices.

## Third-party software

Dependencies, bundled libraries and other third-party materials retain their own licences. The project-wide AGPL statement does not replace their copyright or licence notices. This also applies to the third-party packages in the committed historical Python environment.

Apache ECharts is used by the frontend under Apache License 2.0. The Apache licence formerly placed at `openESEA_interpreter/frontend/LICENSE.txt` was intended to document that dependency, rather than to license the original openESEA frontend under Apache 2.0. The frontend licence file now states the project's AGPL terms, and ECharts' upstream licence, NOTICE and subcomponent licence are preserved under [frontend/public/licenses/echarts/](openESEA_interpreter/frontend/public/licenses/echarts/).

See [frontend third-party notices](openESEA_interpreter/frontend/public/THIRD_PARTY_NOTICES.txt) for the charting packages checked against the lockfile. That document is a scoped record, not an exhaustive inventory of every direct and transitive project dependency.

## Distribution and hosted use

Preserve the applicable licence texts, copyright notices and required third-party notices when distributing source or built applications. Standard Vue CLI builds copy the charting notices and licence files from `frontend/public/` into the output. Retain those files if the build or deployment process is customised.

If you operate a modified version of openESEA that users interact with over a network, prominently offer those users access to the corresponding source of that version, as required by AGPLv3 section 13. A link to this repository is sufficient only if it provides the corresponding source for the version you actually operate; otherwise provide your modified source as well.

## Other materials and successor project

The software licence does not automatically grant rights to third-party accounting-method content, datasets, images, papers or other independently licensed materials. Preserve and consult their individual notices.

These statements concern the code and materials in this repository. The continuing Show your Heart project has its own codebase and applicable licensing notices.
