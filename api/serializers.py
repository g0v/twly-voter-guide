from django.contrib.auth.models import User, Group
from rest_framework import serializers
from legislator.models import Legislator,Attendance,Politics
from vote.models import Vote,Legislator_Vote
from proposal.models import Proposal,Legislator_Proposal
from bill.models import Bill,Legislator_Bill,BillDetail
from issue.models import Issue


class LegislatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator
        exclude = ('enableSession',)
        #fields = ('url', 'name', 'party', 'committee')
class Legislator_ProposalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Proposal
class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proposal
        exclude = ('session','hits','likes','dislikes',)

class Legislator_VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Vote
class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        exclude = ('sessionPrd','session','hits','likes','dislikes',)

class Legislator_BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Bill
class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        exclude = ('progress','hits',)
class BillDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BillDetail

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance

class PoliticsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Politics

class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
##class Issue_ProposalSerializer(serializers.HyperlinkedModelSerializer):
##    class Meta:
##        model = Issue_Proposal
##class Issue_VoteSerializer(serializers.HyperlinkedModelSerializer):
##    class Meta:
##        model = Issue_Vote
##class Issue_BillSerializer(serializers.HyperlinkedModelSerializer):
##    class Meta:
##        model = Issue_Bill
