__author__ = 'pilat10'
from base.signal_models import LogEntry, ADD, CHANGE, DELETE


def obj_save(sender, **kwargs):
    obj = kwargs['instance']
    save_model = LogEntry()
    flag = CHANGE
    #flag = LogEntry.ACTION_STATUS['ADD']
    if kwargs['created']:
        flag = ADD
    save_model.action_flag = flag
    save_model.object_id = obj.pk
    save_model.object_descript = obj
    save_model.save()


def obj_delete(sender, **kwargs):
    obj = kwargs['instance']
    save_model = LogEntry()
    flag = DELETE
    save_model.action_flag = flag
    save_model.object_id = obj.pk
    save_model.object_descript = obj
    save_model.save()