from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
from rest_registration.api.views import (
    register,
    verify_registration,
    send_reset_password_link,
    reset_password,
    profile,
    change_password,
    register_email,
    verify_email,
)
from .views import (
    organization,
    method,
    topic,
    direct_indicator,
    indirect_indicator,
    user,
    group,
    survey,
    survey_response,
)

router = routers.DefaultRouter()
router.register(
    r'organizations',
    organization.OrganizationViewSet,
    basename='organizations',
)
router.register(r'users', user.UserViewSet, basename='users')
router.register(r'groups', group.GroupViewSet, basename='groups')

organization_router = routers.NestedDefaultRouter(
    router, r'organizations', lookup="organization",
)

organization_router.register(
    r'users',
    organization.OrganizationUserViewSet,
    base_name='organization-users',
)

organization_router.register(
    r'methods', method.MethodViewSet, base_name='organization-methods',
)

method_routes = routers.NestedDefaultRouter(
    organization_router, r'methods', lookup="method",
)

method_routes.register(
    r'topics', topic.TopicViewSet, base_name='topics',
)

method_routes.register(
    r'surveys', survey.SurveyViewSet, base_name='surveys',
)

method_routes.register(
    r'questions',
    direct_indicator.DirectIndicatorViewSet,
    base_name='questions',
)

method_routes.register(
    r'indirect_indicators',
    indirect_indicator.IndirectIndicatorViewSet,
    base_name='indirect_indicators',
)

survey_routes = routers.NestedDefaultRouter(
    method_routes, r'surveys', lookup="survey",
)

survey_routes.register(
    r'responses',
    survey_response.SurveyResponseViewset,
    basename='survey_responses',
)

# public survey routes
router.register(
    r'surveys', survey.PublicSurveyViewSet, basename='public-surveys',
)

public_survey_router = routers.NestedDefaultRouter(
    router, r'surveys', lookup="survey",
)
public_survey_router.register(
    r'responses',
    survey_response.PublicSurveyResponseViewset,
    base_name='survey-responses',
)

registerPatterns = [
    path('register/', register, name='register'),
    path(
        'verify-registration/',
        verify_registration,
        name='verify-registration',
    ),
    path(
        'send-reset-password-link/',
        send_reset_password_link,
        name='send-reset-password-link',
    ),
    path('reset-password/', reset_password, name='reset-password'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change-password'),
    path('register-email/', register_email, name='register-email'),
    path('verify-email/', verify_email, name='verify-email'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(organization_router.urls)),
    path('', include(method_routes.urls)),
    path('', include(survey_routes.urls)),
    path('', include(public_survey_router.urls)),
    path('auth/token', obtain_jwt_token),
    path('auth/refresh', refresh_jwt_token),
    path('auth/verify', verify_jwt_token),
    path('account/', include(registerPatterns)),
]
