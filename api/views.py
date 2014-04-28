#from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from .serializers import *
from legislator.models import Legislator, LegislatorDetail, Attendance, Platform, PoliticalContributions
from property.models import Stock, Land, Building, Car, Cash, Deposit, Aircraft, Boat
from sittings.models import Sittings
from committees.models import Committees, Legislator_Committees
from vote.models import Vote, Legislator_Vote
from proposal.models import Proposal, Legislator_Proposal
from bill.models import Bill, Legislator_Bill


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_fields = ('legislator', 'name', 'symbol', 'owner', 'quantity', 'face_value', 'currency', 'total')

class LandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Land.objects.all()
    serializer_class = LandSerializer
    filter_fields = ('legislator', 'name', 'area', 'share_portion', 'portion', 'owner', 'register_date', 'register_reason', 'acquire_value', 'total')

class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filter_fields = ('legislator', 'name', 'area', 'share_portion', 'portion', 'owner', 'register_date', 'register_reason', 'acquire_value', 'total')

class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_fields = ('legislator', 'name', 'capacity', 'owner', 'register_date', 'register_reason', 'acquire_value')

class CashViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cash.objects.all()
    serializer_class = CashSerializer
    filter_fields = ('legislator', 'currency', 'owner', 'total')

class DepositViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    filter_fields = ('legislator', 'bank', 'deposit_type', 'currency', 'owner', 'total')

class AircraftViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class BoatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Boat.objects.all()
    serializer_class = BoatSerializer

class PoliticalContributionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PoliticalContributions.objects.all()
    serializer_class = PoliticalContributionsSerializer
    filter_fields = ('legislator',)

class LegislatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator.objects.all()
    serializer_class = LegislatorSerializer
    filter_fields = ('uid', 'name')

class LegislatorDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LegislatorDetail.objects.all()
    serializer_class = LegislatorDetailSerializer
    filter_fields = ('legislator', 'ad', 'name', 'gender', 'party', 'caucus', 'constituency', 'county', 'in_office', 'term_start', 'term_end')

class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_fields = ('legislator', 'sitting', 'category', 'status')

class SittingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sittings.objects.all()
    serializer_class = SittingsSerializer
    filter_fields = ('uid', 'name', 'committee', 'date', 'ad', 'session')

class CommitteesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Committees.objects.all()
    serializer_class = CommitteesSerializer
    filter_fields = ('name', 'category')

class Legislator_CommitteesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Committees.objects.all()
    serializer_class = Legislator_CommitteesSerializer
    filter_fields = ('legislator', 'committee', 'ad', 'session', 'chair')

class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    filter_fields = ('legislator', 'content', 'category', 'party')

class ProposalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    filter_fields = ('proposer', 'uid', 'sitting', 'proposal_seq', 'content')

class Legislator_ProposalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Proposal.objects.all()
    serializer_class = Legislator_ProposalSerializer
    filter_fields = ('legislator', 'proposal', 'priproposer')

class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_fields = ('voter', 'uid', 'sitting', 'vote_seq', 'content')

class Legislator_VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Vote.objects.all()
    serializer_class = Legislator_VoteSerializer
    filter_fields = ('legislator', 'vote', 'decision', 'conflict')

class BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filter_fields = ('proposer', 'uid', 'api_bill_id', 'bill_type', 'sitting_introduced', 'last_action_at', 'last_action')

class Legislator_BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Bill.objects.all()
    serializer_class = Legislator_BillSerializer
    filter_fields = ('legislator', 'bill', 'priproposer', 'petition')
