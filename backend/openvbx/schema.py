# import graphene
# from graphene_django import DjangoObjectType
#
# from . import models
#
#
# class VoiceMailType(DjangoObjectType):
#     class Meta:
#         model = models.VoiceMail
#
#
# class Query(graphene.ObjectType):
#     voicemails = graphene.List(VoiceMailType)
#
#     def resolve_voicemails(self, info, **kwargs):
#         return models.VoiceMail.objects.all()
