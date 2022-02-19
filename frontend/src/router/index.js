// Used to Connect files to a specific

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/test/',
        name: 'test-page',
        component: () => import('../components/MethodHeader'),
        meta: {
        requiresLogin: false
        }
    },
    {
        path: '/survey-fill/:uniquetoken',
        name: 'survey-fill-page',
        components: {
        surveyview: () => import('@/views/survey/SurveyFill')
        }
    },
    {
        path: '/survey-thank-you/',
        name: 'survey-thank-you',
        components: {
        surveyview: () => import('@/views/survey/SurveyThankYou')
        }
    },
    {
        path: '/register',
        name: 'register',
        components: {
        anonymousview: () => import('../views/user/Register.vue')
        }
    },
    {
        path: '/login',
        name: 'login',
        components: {
        anonymousview: () => import('../views/user/Login')
        }
    },
    {
        path: '/logout',
        name: 'logout',
        components: {
            anonymousview: () => import('../views/user/Logout.vue')
        }
    },
    {
        path: '/account-recovery',
        name: 'accountrecovery',
        components: {
        anonymousview: () => import('@/views/user/AccountRecovery')
        }
    },
    {
        path: '/',
        name: 'home',
        component: () => import('../views/user/Home.vue'),
        meta: {
        requiresLogin: true
        }
    },
    {
        path: '/users',
        name: 'users',
        component: () => import('../views/user/Users.vue'),
        meta: {
        requiresLogin: true
        }
    },
    {
        path: '/users/:id',
        name: 'userdetails',
        component: () => import('../views/user/UserDetails.vue'),
        meta: {
        requiresLogin: true
        }
    },
    {
        path: '/userprofile',
        name: 'userprofile',
        component: () => import('../views/user/UserProfile.vue'),
        meta: {
        requiresLogin: true
        }
    },
    {
        path: '/networks',
        name: 'networks',
        component: () => import('../views/network/Networks.vue'),
        meta: {
        requiresLogin: true,
        breadcrumb: [{ label: 'networks', to: '/networks' }]
        }
    },
    {
        path: '/network/:NetworkId',
        name: 'network',
        component: () => import('../views/network/Network'),
        children: [
        {
            path: 'overview',
            name: 'networkoverview',
            component: () => import('../views/network/NetworkOverview'),
            meta: {
            requiresLogin: true,
            breadcrumb: [
                { label: 'Networks', to: '/networks' },
                { label: '', to: { name: 'networkoverview', params: { id: '' } } },
                { label: 'Overview', to: { name: 'networkoverview' } }
            ]
            }
        },
        {
            path: 'campaigns',
            name: 'networkcampaigns',
            component: () => import('../views/network/NetworkCampaigns'),
            meta: {
            requiresLogin: true,
            breadcrumb: [
                { label: 'Networks', to: '/networks' },
                { label: '', to: { name: 'networkoverview', params: { id: '' } } },
                { label: 'Campaigns', to: { name: 'networkcampaigns' } }
            ]
            }
        },
        {
            path: 'campaigns/:CampaignId',
            name: 'networkcampaign',
            component: () => import('../views/network/NetworkCampaign'),
            meta: {
            requiresLogin: true,
            breadcrumb: [
                { label: 'Networks', to: '/networks' },
                { label: '', to: { name: 'networkoverview', params: { id: '' } } },
                { label: 'campaign', to: { name: 'networkcampaign' } }
            ]
            }
        },
        {
            path: 'campaigns/:CampaignId/esea-account/:EseaAccountId',
            name: 'networkeseaaccount',
            component: () => import('../views/network/NetworkEseaAccount'),
            meta: {
            requiresLogin: true,
            breadcrumb: [
                { label: 'Networks', to: '/networks' },
                { label: '', to: { name: 'networkoverview', params: { id: '' } } },
                { label: 'campaign', to: { name: 'networkcampaign' } },
                { label: 'EseaAccount', to: { name: 'networkeseaaccount' } }
            ]
            }
        },
        {
            path: 'methods',
            name: 'networkmethods',
            component: () => import('../views/network/NetworkMethods'),
            meta: {
            requiresLogin: true,
            breadcrumb: [
                { label: 'Networks', to: '/networks' },
                { label: '', to: { name: 'networkoverview', params: { id: '' } } },
                { label: 'Methods', to: { name: 'networkmethods' } }
            ]
            }
        },
        {
            path: 'organisations',
            name: 'networkorganisations',
            component: () => import('../views/network/NetworkOrganisations'),
            meta: {
            requiresLogin: true,
            breadcrumb: [
                { label: 'Networks', to: '/networks' },
                { label: '', to: { name: 'networkoverview', params: { id: '' } } },
                { label: 'Organisations', to: { name: 'networkorganisations' } }
            ]
            }
        },
        {
            path: 'team',
            name: 'networkteam',
            component: () => import('../views/network/NetworkTeam'),
            meta: {
            requiresLogin: true,
            breadcrumb: [
                { label: 'Networks', to: '/networks' },
                { label: '', to: { name: 'networkoverview', params: { id: '' } } },
                { label: 'Team', to: { name: 'networkteam' } }
            ]
            }
        },
        {
            path: 'settings',
            name: 'networksettings',
            component: () => import('../views/network/NetworkSettings'),
            meta: {
            requiresLogin: true,
            breadcrumb: [
                { label: 'Networks', to: '/networks' },
                { label: '', to: { name: 'networkoverview', params: { id: '' } } },
                { label: 'Settings', to: { name: 'networksettings' } }
            ]
            }
        }
        ],
        meta: {
        requiresLogin: true,
        breadcrumb: [{ label: 'networks', to: '/networks' }, { label: '', to: { name: 'networkoverview', params: { id: '' } } }]
        }
    },
    {
        path: '/organisation/:OrganisationId',
        name: 'organisation',
        component: () => import('../views/organisation/Organisation'),
        children: [
            {
                path: 'overview',
                name: 'organisationoverview',
                component: () => import('../views/organisation/OrganisationOverview'),
                meta: {
                requiresLogin: true,
                breadcrumb: [
                    { label: 'Organisations', to: '/organisations' },
                    { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
                    { label: 'Overview', to: { name: 'organisationoverview' } }
                ]
                }
            },
            {
                path: 'esea-accounts',
                name: 'organisationeseaaccounts',
                component: () => import('../views/organisation/OrganisationEseaAccounts'),
                meta: {
                    requiresLogin: true,
                    breadcrumb: [
                    { label: 'Organisations', to: '/organisations' },
                    { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
                    { label: 'Esea Accounts', to: { name: 'organisationeseaaccounts' } }
                    ]
                }
            },
            {
                path: 'esea-accounts/:EseaAccountId',
                name: 'organisationeseaaccount',
                component: () => import('../views/organisation/OrganisationEseaAccount'),
                children: [
                    {
                        path: 'auditing-page',
                        name: 'organisationauditing',
                        component: () => import('../views/organisation/OrganisationAuditing.vue'),
                        meta: {
                        requiresLogin: true
                    }
                    // surveys view,
                    // settings view,
                    // report view,
                }
                ],
                meta: {
                    requiresLogin: true,
                    breadcrumb: [
                    { label: 'Organisations', to: '/organisations' },
                    { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
                    { label: 'Esea Accounts', to: { name: 'organisationeseaaccounts' } },
                    { label: 'esea_account', to: { name: 'organisationeseaaccount' } }
                    ]
                }
            },
            {
                path: 'reports',
                name: 'organisationreports',
                component: () => import('../views/organisation/OrganisationReports'),
                meta: {
                    breadcrumb: [
                    { label: 'Organisations', to: '/organisations' },
                    { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
                    { label: 'Reports', to: { name: 'organisationreports' } }
                    ]
                }
            },
            // {
            // path: 'surveys',
            // name: 'organisationsurveys',
            // component: () => import('../views/organisation/OrganisationSurveys'),
            // meta: {
            //     breadcrumb: [
            //     { label: 'Organisations', to: '/organisations' },
            //     { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
            //     { label: 'Surveys', to: { name: 'organisationsurveys' } }
            //     ]
            // }
            // },
            // {
            //     path: 'stakeholders',
            //     name: 'organisationstakeholders',
            //     component: () => import('../views/organisation/OrganisationStakeholders'),
            //     meta: {
            //     breadcrumb: [
            //         { label: 'Organisations', to: '/organisations' },
            //         { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
            //         { label: 'Stakeholders', to: { name: 'organisationstakeholders' } }
            //     ]
            //     }
            // },
            {
                path: 'networks',
                name: 'organisationnetworks',
                component: () => import('../views/organisation/OrganisationNetworks'),
                meta: {
                breadcrumb: [
                    { label: 'Organisations', to: '/organisations' },
                    { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
                    { label: 'Networks', to: { name: 'organisationnetworks' } }
                ]
                }
            },
            {
                path: 'team',
                name: 'organisationteam',
                component: () => import('../views/organisation/OrganisationTeam'),
                meta: {
                requiresLogin: true,
                breadcrumb: [
                    { label: 'Organisations', to: '/organisations' },
                    { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
                    { label: 'Team', to: { name: 'organisationteam' } }
                ]
                }
            },
            {
                path: 'settings',
                name: 'organisationsettings',
                component: () => import('../views/organisation/OrganisationSettings'),
                meta: {
                breadcrumb: [
                    { label: 'Organisations', to: '/organisations' },
                    { label: '', to: { name: 'organisationoverview', params: { id: '' } } },
                    { label: 'Settings', to: { name: 'organisationsettings' } }
                ]
                }
            }
        ],
        meta: {
        breadcrumb: [
            { label: 'Organisations', to: '/organisations' },
            { label: '', to: { name: 'organisation', params: { id: '' } } }
        ]
        }
    },

    // Audit
    {
        path: '/networks/:NetworkId/campaigns/:CampaignId',
        name: 'auditCampaign',
        component: () => import('../views/audit/batch/BatchAudit.vue'),

        children: [
            {
                path: 'batch-audit-organisation-selection',
                name: 'batchauditselection',
                component: () => import('../views/audit/batch/BatchAuditSelection.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'batch-audit-overview',
                name: 'batchauditoverview',
                component: () => import('../views/audit/batch/BatchAuditsOverview.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'batch-audit-results',
                name: 'batchauditresults',
                component: () => import('../views/audit/batch/BatchAuditResults.vue'),
                meta: {
                    requiresLogin: true
                }
            }
        ],
        meta: {
            requiresLogin: true
        }
    },
    {
        path: '/esea-accounts/:EseaAccountId/survey-audit/:SurveyId',
        name: 'auditEseaAccount',
        component: () => import('../views/audit/AuditEseaAccount.vue'),
        children: [
            {
                path: 'single-question-selection',
                name: 'questionselection',
                component: () => import('../views/audit/single/AuditQuestionSelection.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'documentation-request',
                name: 'documentationrequest',
                component: () => import('../views/audit/single/AuditDocumentationRequest.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'documentation-upload',
                name: 'documentationupload',
                component: () => import('../views/audit/single/AuditDocumentationUpload.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'audit-progress',
                name: 'singleauditaudit',
                component: () => import('../views/audit/single/AuditAudit.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'audit-results',
                name: 'singleauditresults',
                component: () => import('../views/audit/single/AuditResults.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'multiple-audit-sampling',
                name: 'multipleauditsampling',
                component: () => import('../views/audit/multiple/AuditMultipleSample.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'multiple-sample-overview',
                name: 'multiplesampleoverview',
                component: () => import('../views/audit/multiple/AuditMultipleSampleOverview.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'multiple-audit',
                name: 'multipleaudit',
                component: () => import('../views/audit/multiple/AuditMultipleAudit.vue'),
                meta: {
                    requiresLogin: true
                }
            },
            {
                path: 'multiple-audit-results',
                name: 'multipleauditresults',
                component: () => import('../views/audit/multiple/AuditMultipleResults.vue'),
                meta: {
                    requiresLogin: true
                }
            }
        ],
        meta: {
            requiresLogin: true
        }
    },
    {
        path: '/audit-question/:QuestionId',
        name: 'singleauditquestion',
        component: () => import('../views/audit/single/AuditQuestion.vue'),
        meta: {
            requiresLogin: true
        }
    },
    {
        path: '/organisations',
        name: 'organisations',
        component: () => import('../views/organisation/Organisations.vue'),
        meta: {
        requiresLogin: true,
        breadcrumb: [
            { label: 'Organisations', to: '/organisations' }
        ]
        }
    },
    {
        path: '/methods',
        name: 'methods',
        component: () => import('../views/method/Methods'),
        meta: {
        requiresLogin: true
        }
    },
    {
        path: '/method-creation',
        name: 'methodcreation',
        component: () => import('../views/method/MethodCreation'),
        meta: {
            requiresLogin: true
        }
    },
    {
        path: '/methods/:id/creation',
        name: 'methodwizard',
        component: () => import('../views/method/Method.vue'),
        meta: {
        requiresLogin: true
        },
        children: [
            {
                path: '/methods/:id/method-general',
                name: 'method-general',
                component: () => import('../views/method/MethodGeneral'),
                meta: {
                requiresLogin: true
                }
            },
            {
                path: '/methods/:id/indicator-creation',
                name: 'method-indicator-creation',
                component: () => import('../views/method/MethodIndicatorCreation'),
                meta: {
                requiresLogin: true
                }
            },
            {
                path: '/methods/:id/topic-creation',
                name: 'method-topic-creation',
                component: () => import('../views/method/MethodTopicCreation'),
                meta: {
                requiresLogin: true
                }
            },
            {
                path: '/method-wizard/:id/surveys',
                name: 'method-wizard-surveys',
                component: () => import('@/components/lists/SurveyList'),
                meta: {
                    requiresLogin: true
                    }
            },
            {
                path: '/method-wizard/:id/surveys/:SurveyId',
                name: 'method-wizard-survey',
                component: () => import('@/views/method/Survey'),
                meta: {
                    requiresLogin: true
                    },
                children: [
                    {
                        path: '/method-wizard/:id/surveys/:SurveyId/settings',
                        name: 'method-wizard-survey-settings',
                        component: () => import('@/views/method/SurveyGeneral'),
                        meta: {
                            requiresLogin: true
                        }
                    },
                    {
                        path: '/method-wizard/:id/surveys/:SurveyId/survey-design',
                        name: 'method-wizard-survey-design',
                        component: () => import('@/views/method/SurveyCreation'),
                        meta: {
                            requiresLogin: true
                        }
                    }
                ]
            },
            {
                path: '/method-wizard/:id/finish',
                name: 'method-wizard-finish',
                component: () => import('@/views/method/MethodFinish'),
                meta: {
                    requiresLogin: true
                    }
            }
        ]
    },
    {
        path: '/newmethods/:id/',
        name: 'newmethoddetails',
        component: () => import('../views/method/NewMethods.vue'),
        meta: {
            requiresLogin: true
        }
    },
    {
        path: '/organisations/:OrganisationId/methods/:id/surveys/:surveyId/',
        name: 'survey-fill',
        component: () => import('../views/survey/SurveyResponse.vue'),
        meta: {
        requiresLogin: true
        }
    },
    {
        path: '/organisations/:OrganisationId/esea-accounts/:EseaAccountId/surveys/:SurveyId/result/',
        name: 'method-survey-result',
        component: () => import('../views/survey/SurveyUserResult.vue'),
        meta: {
        requiresLogin: true
        }
    },
    {
        path: '/organisations/:OrganisationId/esea-accounts/:EseaAccountId/surveys/:SurveyId/results/',
        name: 'survey-results',
        component: () => import('../views/survey/SurveyResults'),
        meta: {
        requiresLogin: true
        }
    },
    {
        path: '/organisations/:OrganisationId/esea-accounts/:EseaAccountId/report',
        name: 'esea-account-report',
        component: () => import('../views/EseaAccountReport.vue'),
        meta: {
        requiresLogin: true
        }
    },

    {
        path: '/:pathMatch(.*)*',
        name: '404',
        component: () => import('../views/user/Logout.vue')
    }
]

const router = createRouter({
history: createWebHistory(), // createWebHashHistory(),
// base: process.env.BASE_url, (?) -------------------------
routes
})

export default router

// let resolved = this.$router.resolve('YOUR URL')
// if(resolved.route.name != '404')
//    // DO SOMETHING
