from django.db.models import query
from django.db.models.query import QuerySet

from isc_common import setAttr
from list.listCalendarEvent import LinkedList


class CalendarEvent:
    backgroundColor = None
    borderColor = 'black'
    canDrag = False
    canEdit = False
    canEditLane = False
    canEditSublane = False
    canResize = False
    description = None
    duration = None
    durationUnit = "hour"
    endDate = None
    headerBackgroundColor = None
    headerBorderColor = None
    headerTextColor = None
    id = None
    isholiday = None
    isworkday = None
    isredlabelday = None
    length = None
    lane = None
    name = None
    startDate = None
    styleName = None
    sublane = None
    textColor = None

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v() if callable(v) else v)

    def __str__(self):
        setAttr(self.__dict__, "startDate", str(self.__dict__.get('startDate')))
        setAttr(self.__dict__, "endDate", str(self.__dict__.get('endDate')))
        return f'{str(self.__dict__)}'

    def print(self, comment=''):
        print('\n')
        print(f'{comment}({self.__hash__()}) {str(self)}')

    def copy(self, *args, **kwargs):
        res = CalendarEvent(**self.__dict__)
        for k, v in kwargs.items():
            setattr(res, k, v() if callable(v) else v)
        return res

    def to_json(self):
        return self.__dict__


class CalendarEventLinkedList(LinkedList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs.get('query'):
            query = kwargs.get('query')
            if isinstance(kwargs.get('query'), QuerySet):
                for item in query:
                    self.add(item)

    def fusion(self, fusion_list):
        if not isinstance(fusion_list, CalendarEventLinkedList):
            raise Exception(f'ce is not CalendarEventLinkedList instance')

        relax = fusion_list.first
        while relax:
            shift = self.first
            y = 0
            while shift:
                # shift.item.print('shift')
                # relax.item.print('relax')
                if shift.item.isworkday and shift.item.startDate < relax.item.startDate:
                    if shift.item.endDate > relax.item.startDate:
                        if shift.item.endDate > relax.item.endDate:
                            # self.print('self:')
                            self.replace(y, shift.item.copy(endDate=relax.item.startDate))
                            # self.print('self:')
                            self.insert(y + 1, relax.item.copy())
                            # self.print('self:')
                            self.insert(y + 2, shift.item.copy(startDate=relax.item.endDate))
                            # self.print('self:')
                            break
                        else:
                            raise Exception(f'Unknown case.')
                    else:
                        pass
                else:
                    pass
                shift = shift.next
                y += 1
            relax = relax.next

    def to_json(self):
        res = []

        if self.first != None:
            current = self.first
            res.append(current.item.to_json())

            while current.next != None:
                current = current.next
                res.append(current.item.to_json())

        return res

    def write_2_file(self, filename):
        outF = open(filename, "w")
        if self.first != None:

            current = self.first
            outF.write('shifts_data=')
            outF.write('[')
            outF.write(f'{str(current)},')
            outF.write("\n")

            while current.next != None:
                current = current.next
                outF.write(f'{str(current)},')
                outF.write("\n")
            outF.write(']')

        outF.close()
        print('Запись выполнена.')
