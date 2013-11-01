from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import LegislatorSerializer,AttendanceSerializer,PoliticsSerializer,IssueSerializer,BillSerializer,BillDetailSerializer,Legislator_BillSerializer,ProposalSerializer,Legislator_ProposalSerializer,VoteSerializer,Legislator_VoteSerializer
from legislator.models import Legislator,Attendance,Politics
from vote.models import Vote,Legislator_Vote
from proposal.models import Proposal,Legislator_Proposal
from bill.models import Bill,Legislator_Bill,BillDetail
from issue.models import Issue


class LegislatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Legislator.objects.all()
    serializer_class = LegislatorSerializer

class ProposalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
class Legislator_ProposalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Proposal.objects.all()
    serializer_class = Legislator_ProposalSerializer

class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
class Legislator_VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Vote.objects.all()
    serializer_class = Legislator_VoteSerializer

class BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
class Legislator_BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Legislator_Bill.objects.all()
    serializer_class = Legislator_BillSerializer
class BillDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BillDetail.objects.all()
    serializer_class = BillDetailSerializer

class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class PoliticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Politics.objects.all()
    serializer_class = PoliticsSerializer

class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
##class Issue_ProposalViewSet(viewsets.ReadOnlyModelViewSet):
##    queryset = Issue_Proposal.objects.all()
##    serializer_class = Issue_ProposalSerializer
##class Issue_VoteViewSet(viewsets.ReadOnlyModelViewSet):
##    queryset = Issue_Vote.objects.all()
##    serializer_class = Issue_VoteSerializer
##class Issue_BillViewSet(viewsets.ReadOnlyModelViewSet):
##    queryset = Issue_Bill.objects.all()
##    serializer_class = Issue_BillSerializer
