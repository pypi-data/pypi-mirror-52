from django.db import models
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal
from dateutil.parser import parse

def group_by_and_aggregate(qs, aggregate_field, aggregation='Sum', default=None):
    '''
    Boils `qs` down to a single valie
    '''
    if default is None: default = Decimal(0)
    key = '{}__{}'.format(aggregate_field, aggregation.lower())
    agg = getattr(models, aggregation)
    return qs.aggregate(agg(aggregate_field)).get(key, default)

def group_by_and_annotate(qs, group_by_field, aggregation='Count'):
    '''
    Perform annotation across `qs` group results by a field
    '''
    agg = getattr(models, aggregation)

    result = qs.values(group_by_field)\
        .annotate(agg(group_by_field))\
        .order_by(group_by_field)

    agg_field = "{}__{}".format(group_by_field, aggregation.lower())
    return { i.get(group_by_field): i.get(agg_field) for i in result }


def pivot_table(qs, pivot_field, serializer_function=None):
    '''
    Given a queryset, group the results by a field and return them as grouped json.

    e.g.:
    joe | 1
    jane | 2
    joe | 3
    joe | 4

    becomes:
    Jane:
      - 2
    Joe:
      - 1
      - 3
      - 4
    '''
    fields = pivot_field.split(",")
    final_field = fields[-1]
    results = {}
    for item in qs:
        base = results
        index = 0
        while fields[index] != final_field:
            field = fields[index]
            field_value = getattr(item, field)
            if base.get(field_value) is None:
                base[field_value] = {}
            base = base[field_value]
            index += 1

        field_value = getattr(item, final_field)
        if base.get(field_value) is None:
            base[field_value] = []

        if serializer_function is not None:
            item = serializer_function(item)
        base[field_value].append(item)

    return results


def get_blank_timeseries(from_date, to_date):
    from dateutil import rrule
    dates = rrule.rrule(
        rrule.DAILY,
        dtstart=parse(from_date),
        until=parse(to_date)
    )
    return [{"x": date.date().isoformat(), "y": 0} for date in dates]

def padd_timeseries(blank_timeseries, populated_timeseries, aggregate_field, aggregation='Sum'):

    value_field = '{}__{}'.format(aggregate_field, aggregation.lower())
    for index, item in enumerate(blank_timeseries):
        try:
            i = populated_timeseries.get(date_only=item.get('x'))
            parsed_item = {
                "x": i.get('date_only').isoformat(),
                "y": float(i.get(value_field))
            }
            blank_timeseries[index] = parsed_item
        except ObjectDoesNotExist:
            pass
    return blank_timeseries

def as_multiple_timeseries(qs, group_by):
    '''Return a number pf series based on the group_by'''
    pass

def as_timeseries(qs, search_field, aggregate_field, aggregation, from_date, to_date):
    agg = getattr(models, aggregation)
    result = qs\
        .annotate(
            date_only=Cast(
                search_field,
                DateField()
            )
        ) \
        .values('date_only') \
        .annotate(agg(aggregate_field)) \
        .order_by('date_only')

    timeseries = get_blank_timeseries(from_date, to_date)
    padd_timeseries(timeseries, result, aggregate_field, aggregation)
    return timeseries

def annotate_context(from_date, to_date, results):
    return {
        "period": {
            "from_date": parse(from_date).date(),
            "to_date": parse(to_date).date()
        },
        "results": results
    }

def periodic_breakdown(qs, field, by='month', aggregate_field='pk', aggregation='Count'):
    """
    periodic_breakdown(Todo.objects.all(), 'date', by='quarter)
    """
    from django.db.models import Count
    from django.db.models.functions import Trunc

    return qs.annotate(
        month=Trunc(field, kind=by)
    ).values(
        'month'
    ).annotate(
        total=getattr(models, aggregation)(aggregate_field)
    )