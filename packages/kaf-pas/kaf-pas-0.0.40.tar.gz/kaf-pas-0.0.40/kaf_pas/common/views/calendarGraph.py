from clndr.models.calendars import Calendars
from isc_common.http.DSResponse import DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse


@JsonResponseWithException()
def CalendarGraph_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Calendars.objects.
                filter().
                get_graph(request=request),
            status=RPCResponseConstant.statusSuccess).response)
