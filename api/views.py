#from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from .serializers import *
from legislator.models import Legislator, LegislatorDetail, Attendance
from candidates.models import Candidates
from sittings.models import Sittings
from committees.models import Committees, Legislator_Committees
from vote.models import Vote, Legislator_Vote
from bill.models import Bill, Legislator_Bill


class LegislatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator.objects.all().prefetch_related('each_terms', 'each_terms__elected_candidate')
    serializer_class = LegislatorSerializer
    filter_fields = ('uid', 'name')

class LegislatorDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LegislatorDetail.objects.all().prefetch_related('legislator', 'elected_candidate')
    serializer_class = LegislatorDetailSerializer
    filter_fields = ('legislator', 'ad', 'name', 'gender', 'party', 'caucus', 'constituency', 'county', 'in_office', 'term_start', 'term_end')

class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all().select_related('sitting', 'legislator')
    serializer_class = AttendanceSerializer
    filter_fields = ('legislator', 'sitting', 'category', 'status')

class CandidatesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Candidates.objects.all().select_related('legislator', 'latest_term')
    serializer_class = CandidatesSerializer
    #filter_fields = ('legislator', 'ad', 'name', 'gender', 'party', 'caucus', 'constituency', 'county', 'in_office', 'term_start', 'term_end')

class SittingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sittings.objects.all().prefetch_related('votes')
    serializer_class = SittingsSerializer
    filter_fields = ('uid', 'name', 'committee', 'date', 'ad', 'session')

class CommitteesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Committees.objects.all()
    serializer_class = CommitteesSerializer
    filter_fields = ('name', 'category')

class Legislator_CommitteesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Committees.objects.all().select_related('committee', 'legislator')
    serializer_class = Legislator_CommitteesSerializer
    filter_fields = ('legislator', 'committee', 'ad', 'session', 'chair')

class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vote.objects.all().select_related('sitting')
    serializer_class = VoteSerializer
    filter_fields = ('voter', 'uid', 'sitting', 'vote_seq', 'content')

class Legislator_VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Vote.objects.all().select_related('vote', 'legislator')
    serializer_class = Legislator_VoteSerializer
    filter_fields = ('legislator', 'vote', 'decision', 'conflict')

class BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bill.objects.all().prefetch_related('proposer')
    serializer_class = BillSerializer
    filter_fields = ('proposer', 'uid', 'api_bill_id', 'bill_type', 'sitting_introduced', 'last_action_at', 'last_action')

class Legislator_BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Bill.objects.all().select_related('bill', 'legislator')
    serializer_class = Legislator_BillSerializer
    filter_fields = ('legislator', 'bill', 'priproposer', 'petition')
