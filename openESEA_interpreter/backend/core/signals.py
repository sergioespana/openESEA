from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from .models import EseaAccount, Respondent, Survey, SurveyResponse, Campaign, Membership, NetworkMember, AccountAudit

@receiver(post_save, sender=EseaAccount)
def create_accountant_objects(sender, instance, created, **kwargs):
    if 'raw' in kwargs and kwargs['raw']:
        return

    respondent = Respondent.objects.create(organisation=instance.organisation, email="accountant@mail.com", first_name="Accountant", last_name=f"of {instance.organisation.name}")
    try:
        surveys = instance.method.surveys.all().filter(response_type="single")
    except ObjectDoesNotExist:
        print('No survey with responsetype "SINGLE" was found in the connected method.')
        # instance.delete()
        respondent.delete()
        return
    
    for survey in surveys:
        surveyresponse = SurveyResponse.objects.create(survey=survey, esea_account=instance, respondent=respondent, token="accountant")
    
@receiver(post_save, sender=Campaign)
def create_esea_accounts(sender, instance, created, **kwargs):
    if 'raw' in kwargs and kwargs['raw']:
        return

    for organisation in instance.network.organisations.all():
        eseaaccount, _ = EseaAccount.objects.get_or_create(organisation=organisation, method=instance.method, campaign=instance)
        
    print('campaign saved', instance.organisation_accounts.all())

@receiver(post_save, sender=Membership)
def accept_request(sender, instance, created, **kwargs):
    if 'raw' in kwargs and kwargs['raw']:
        return
        
    if instance.status == ('accepted' or 'denied'):
        network = instance.network
        organisation = instance.organisation
        if organisation not in network.organisations.all():
            network.organisations.add(organisation)
        instance.delete()

# Creates an ESEA ACCOUNT AUDIT object
@receiver(post_save, sender=EseaAccount)
def create_esea_accounts(sender, instance, created, **kwargs):
    if 'raw' in kwargs and kwargs['raw']:
        return

    AccountAudit.objects.create(esea_account=instance)
