__author__ = 'pilat10'
from base.signal_models import LogEntry


def obj_save(sender, **kwargs):
    obj = kwargs['instance']
    save_model = LogEntry()
    flag = save_model.get_action_status('change')
    if kwargs['created']:
        flag = save_model.get_action_status('add')
    save_model.action_flag = flag
    save_model.object_id = obj.pk
    save_model.object_descript = obj
    save_model.save()


def obj_delete(sender, **kwargs):
    obj = kwargs['instance']
    save_model = LogEntry()
    flag = save_model.get_action_status('delete')
    save_model.action_flag = flag
    save_model.object_id = obj.pk
    save_model.object_descript = obj
    save_model.save()