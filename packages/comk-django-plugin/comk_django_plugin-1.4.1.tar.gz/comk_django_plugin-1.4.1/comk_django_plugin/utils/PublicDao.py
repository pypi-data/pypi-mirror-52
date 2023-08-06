from django.db.models import CharField, TextField, Model


class PublicDao():
    def __init__(self, model: type(Model)):
        self.model = model

    def return_obj(self, data: dict, pk: str = None):
        '''
        返回一个obj实例，不保存

        :param data:
        :param pk:
        :return:
        '''
        result = self.model._meta.get_fields()
        obj = self.model()
        for field in result:
            field_name = field.name
            if isinstance(field, (CharField, TextField)) and not field.primary_key:
                if data.get(field_name):
                    setattr(obj, field_name, data.get(field_name))
        if pk:
            obj.pk = pk

        return obj

    def save_obj(self, data: dict, pk: str = None):
        '''
        保存obj

        :param data:
        :param pk:
        :return:
        '''
        obj = self.return_obj(data, pk)
        obj.save()
        return obj

    def bulk_create(self, obj_list):
        '''
        批量保存objs

        :param obj_list:
        :return:
        '''
        return self.model.objects.bulk_create(obj_list)

    def get_objs(self, key_filter, get_flag=False, for_update=False):
        '''
        查询

        :param key_filter:
        :param get_flag:
        :param for_update:
        :return:
        '''
        manager = self.model.objects
        if for_update:
            manager = manager.select_for_update()
        obg_filter = manager.filter(**key_filter)
        if get_flag and obg_filter:
            return obg_filter[0]
        else:
            return obg_filter

    def get_part_objs_and_count_all(self, key_filter, offset=0, limit=0):
        '''
        根据偏移量进行部分数据查询

        :param key_filter:
        :param offset:
        :param limit:
        :return:
        '''
        obg_filter = self.get_objs(key_filter)
        return obg_filter[offset:offset + limit], obg_filter.count()
