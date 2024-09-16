from server.models import Lead   
from server.serializers.LeadsSerializer import LeadsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
 
# GET method to retrieve all leads
class GetAll(APIView):
    def get(self,request):
        detailsObj=Lead.objects.all()
        dlSerializeObj=LeadsSerializer(detailsObj, many=True)
        return Response(dlSerializeObj.data)
    def post(self,request):
        serializeobj=LeadsSerializer(data=request.data)
        if serializeobj.is_valid():
            serializeobj.save()
            return Response(200)
        return Response(serializeobj.errors)

# FilterByName method filters leads by their name based on the 'name' query parameter.
class FilterByName(APIView):
    def get(self, request):
        # Get the value of the 'name' parameter from query params
        name =request.GET.get('name','')
        # Remove single or double quotes at the beginning and end, if present
        name = name.strip("'\"")
        
        # Filter leads by productName containing the provide
        leads = Lead.objects.filter(productName__icontains=name)
        dlSerializeObj=LeadsSerializer(leads, many=True)
        return Response(dlSerializeObj.data)
   
# POST method for creating a new Data Select
class Create(APIView):
    def post(self, request):
       serializeobj = LeadsSerializer(data=request.data)
       if serializeobj.is_valid():
            serializeobj.save()
            return Response(serializeobj.data, status=201) 
       return Response(serializeobj.errors, status=400)

# PUT method for editing an existing Data Select
class Edit(APIView):
    def put(self, request, pk):
        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            return Response({'error': 'Lead not found'}, status=404)

        serializeobj = LeadsSerializer(lead, data=request.data)
        if serializeobj.is_valid():
            serializeobj.save()
            return Response(serializeobj.data, status=200)
        return Response(serializeobj.errors, status=400)
  