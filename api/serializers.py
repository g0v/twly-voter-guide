#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from legislator.models import Legislator, LegislatorDetail, Attendance, Platform
from sittings.models import Sittings
from committees.models import Committees, Legislator_Committees
from vote.models import Vote, Legislator_Vote
from proposal.models import Proposal, Legislator_Proposal
from bill.models import Bill, Legislator_Bill


class LegislatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator

class LegislatorDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LegislatorDetail

class SittingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sittings

class CommitteesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Committees
        fields = ('category', 'name')

class Legislator_CommitteesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Committees

class Legislator_ProposalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Proposal

class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proposal
        fields = ('proposer', 'uid', 'sitting', 'proposal_seq', 'content')

class Legislator_VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Vote

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ('voter', 'uid', 'sitting', 'vote_seq', 'content')

class Legislator_BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Bill

class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance

class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Platform
