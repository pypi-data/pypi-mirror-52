from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.production.models.operations_item import Operations_item, Operations_itemManager


@JsonResponseWithException()
def Operations_item_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Operations_item.objects.
                filter().
                # select_related('item', 'operation').
                get_range_rows1(
                request=request,
                function=Operations_itemManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_item_Add(request):
    return JsonResponse(DSResponseAdd(data=Operations_item.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_item_Update(request):
    return JsonResponse(DSResponseUpdate(data=Operations_item.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_item_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Operations_item.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_item_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Operations_item.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_item_Info(request):
    return JsonResponse(DSResponse(request=request, data=Operations_item.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_item_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Operations_item.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
