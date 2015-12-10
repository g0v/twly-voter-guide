#from django.contrib.auth.models import User, Group
from rest_framework import serializers

from legislator.models import Legislator, LegislatorDetail, Attendance
from candidates.models import Candidates, Terms
from sittings.models import Sittings
from committees.models import Committees, Legislator_Committees
from vote.models import Vote, Legislator_Vote
from bill.models import Bill, Legislator_Bill


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
    sitting_id = serializers.StringRelatedField()
    class Meta:
        model = Vote
        fields = ('url', 'uid', 'sitting_id', 'vote_seq', 'content', 'conflict', 'results', 'result')

class Legislator_BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator_Bill

class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = ('url', 'uid', 'proposer', 'ad', 'api_bill_id', 'abstract', 'summary', 'bill_type', 'doc', 'proposed_by', 'sitting_introduced', 'last_action_at', 'last_action')

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance

class SittingsSerializer(serializers.HyperlinkedModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)
    class Meta:
        model = Sittings
        fields = ('url', 'uid', 'name', 'committee', 'date', 'ad', 'session', 'links', 'votes')

class LegislatorDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LegislatorDetail
        fields = ('url', 'id', 'legislator', 'ad', 'name', 'gender', 'title', 'party', 'elected_party', 'caucus', 'constituency', 'county', 'district', 'in_office', 'contacts', 'term_start', 'term_end', 'education', 'experience', 'remark', 'image', 'links', 'platform', 'bill_param', 'vote_param', 'attendance_param', 'elected_candidate', )

class CandidatesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidates

class Candidates_TermsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Terms

class LegislatorSerializer(serializers.HyperlinkedModelSerializer):
    each_terms = LegislatorDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Legislator
