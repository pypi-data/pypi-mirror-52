import logging

from django.db.models import PositiveIntegerField
from django.forms import model_to_dict

from isc_common import delAttr
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsQuerySet, CommonManagetWithLookUpFieldsManager
from isc_common.models.base_ref import Hierarcy
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item
from kaf_pas.production.models.operations import Operations

logger = logging.getLogger(__name__)


class Operations_itemQuerySet(CommonManagetWithLookUpFieldsQuerySet):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Operations_itemManager(CommonManagetWithLookUpFieldsManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'operation_id': record.operation.id,
            'operation__code': record.operation.code,
            'operation__name': record.operation.name,
            'operation__full_name': record.operation.full_name,
            'operation__description': record.operation.description,
            'ed_izm_id': record.ed_izm.id if record.ed_izm else None,
            'ed_izm__code': record.ed_izm.code if record.ed_izm else None,
            'ed_izm__name': record.ed_izm.name if record.ed_izm else None,
            'ed_izm__description': record.ed_izm.description if record.ed_izm else None,
            'qty': record.qty,
            'parent_id': record.parent.id if record.parent else None
        }
        return res

    def get_queryset(self):
        return Operations_itemQuerySet(self.model, using=self._db)

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        delAttr(_data, 'operation__full_name')

        res = super().create(**_data)
        res = model_to_dict(res)

        data.update(res)
        return data

    def updateFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        delAttr(_data, 'operation__full_name')
        super().update_or_create(id=data.get('id'), defaults=_data)

        return data


class Operations_item(Hierarcy):
    item = ForeignKeyProtect(Item)
    operation = ForeignKeyProtect(Operations)
    ed_izm = ForeignKeyProtect(Ed_izm, default=None, null=True, blank=True)
    qty = PositiveIntegerField(default=None, null=True, blank=True)

    objects = Operations_itemManager()

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Кросс таблица'
