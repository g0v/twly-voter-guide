from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import LegislatorSerializer,AttendanceSerializer,BillSerializer,BillDetailSerializer,Legislator_BillSerializer,ProposalSerializer,Legislator_ProposalSerializer,VoteSerializer,Legislator_VoteSerializer
from legislator.models import Legislator,Attendance,Bill,Legislator_Bill,BillDetail,Proposal,Legislator_Proposal,Vote,Legislator_Vote

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
