# dj-querytools

A collection of functions to make it a little easier to build aggregation SQL queries for Django projects

## Installation

```
pip install dj-querytools
```

## Usage

### Simple aggregation:

Assuming the following model:

```
class Todo(models.Model):
    owner = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    status = models.CharField(max_length=30, choices=TODO_STATUSES)
    size = models.PositiveIntegerField(default=1)
    due = models.DateField()
    due_time = models.DateTimeField()
```

### `group_by_and_aggregate`

**Example**

```python

group_by_and_aggregate(
    qs,
    'size',
    'Sum'
)
>> 20
```

### `group_by_and_annotate`

Performs the aggregation and groups by the provided field:

**Example**

```python

result = group_by_and_annotate(
    qs,
    'status',
    'Count'
)
>> {'D': 5, 'N': 1, 'P': 8}
```

### `as_timeseries`

```
qs = Todo.objects.filter(owner="Jack")
as_timeseries(
    qs,
    'due_time',
    'id',
    'Count',
    '2018-11-01',
    '2018-11-10'
)
>> [{'x': '2018-11-01', 'y': 3.0}, {'x': '2018-11-02', 'y': 3.0}, {'x': '2018-11-03', 'y': 0}, {'x': '2018-11-04', 'y': 2.0}, {'x': '2018-11-05', 'y': 2.0}, {'x': '2018-11-06', 'y': 0}, {'x': '2018-11-07', 'y': 0}, {'x': '2018-11-08', 'y': 0}, {'x': '2018-11-09', 'y': 0}, {'x': '2018-11-10', 'y': 0}]
```

### `pivot_table`

Given a flat queryset, group it by one or more fields.

* fields are comma seperated
* optionally provide a serializer function to serialize items (otherwise it will just append the queryset row)

```python
result = pivot_table(qs, 'owner,status', serialize_todo)

>> {'Jack': {'N': [{'title': 'Day year outside whatever int'}], 'P': [{'title': 'Answer society close example '}, {'title': 'Raise real individual general'}], 'D': [{'title': 'Number organization particula'}, {'title': 'Least activity herself than c'}, {'title': 'Country local pretty yourself'}]}, 'Jane': {'P': [{'title': 'Prevent do still teacher grou'}, {'title': 'Include they management first'}, {'title': 'Number court few loss sort mu'}, {'title': 'That federal end local dream '}, {'title': 'Able ask listen. Cost ball me'}, {'title': 'Bad know meeting compare room'}], 'D': [{'title': 'Through town stay able car di'}, {'title': 'Tree design candidate because'}]}}
```

## periodic_breakdown

`from querytools.tools import periodic_breakdown`

Provide an aggregation broken down by a period (Trun(kind=)).

See: https://docs.djangoproject.com/en/2.1/ref/models/database-functions/#django.db.models.functions.TruncMonth

**Defaults:**

* `kind='month'`
* `aggregate_field='ok'`
* `aggregation = 'Count'`

```python

# simple case:
result = periodic_breakdown(qs, 'due')

# slighly more fancy:
result = periodic_breakdown(
    qs,
    'due',
    aggregate_field='size',
    aggregation = 'Sum'
)
```


## Other stuff

* For full functionality list, see `spec.txt`
* For examples, check `example_app/tests.py`

## Contributing

**Update the spec:**

```
python manage.py test --testrunner=testreporter.runner.BDDTestRunner
```
