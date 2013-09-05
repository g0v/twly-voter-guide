from django.contrib.auth.models import User, Group
from rest_framework import serializers
from legislator.models import Legislator,Attendance,Bill,Legislator_Bill,BillDetail,Proposal,Legislator_Proposal,Vote,Legislator_Vote

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
