#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import fields
from legislator.models import Legislator, LegislatorDetail, Attendance, PoliticalContributions
from sittings.models import Sittings
from committees.models import Committees, Legislator_Committees
from vote.models import Vote, Legislator_Vote
from bill.models import Bill, Legislator_Bill


class PoliticalContributionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PoliticalContributions

class CommitteesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Committees
        fields = ('category', 'name')

class Legislator_CommitteesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Committees

class Legislator_VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Vote

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    results = fields.Field()
    sitting_id = serializers.SlugRelatedField(many=True, read_only=True, slug_field='uid')
    class Meta:
        model = Vote
        fields = ('voter', 'uid', 'sitting', 'vote_seq', 'content', 'conflict', 'results', 'result')

class Legislator_BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Bill

class BillSerializer(serializers.HyperlinkedModelSerializer):
    doc = fields.Field()
    class Meta:
        model = Bill

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance

class SittingsSerializer(serializers.HyperlinkedModelSerializer):
    votes = VoteSerializer(many=True)
    class Meta:
        model = Sittings
        fields = ('uid', 'name', 'committee', 'date', 'ad', 'session', 'votes')

class LegislatorDetailSerializer(serializers.HyperlinkedModelSerializer):
    politicalcontributions = PoliticalContributionsSerializer(many=True)
    #votes = Legislator_VoteSerializer(many=True)
    contacts = fields.Field()
    term_end = fields.Field()
    links = fields.Field()
    bill_param = fields.Field()
    vote_param = fields.Field()
    attendance_param = fields.Field()
    class Meta:
        model = LegislatorDetail

class LegislatorSerializer(serializers.HyperlinkedModelSerializer):
    each_terms = LegislatorDetailSerializer(many=True)
    class Meta:
        model = Legislator
