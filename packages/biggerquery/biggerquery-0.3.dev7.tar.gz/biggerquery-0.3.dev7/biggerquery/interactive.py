from __future__ import absolute_import

from inspect import getargspec
import hashlib

from .configuration import DatasetConfig
from .job import Job
from .job import DEFAULT_RETRY_COUNT
from .job import DEFAULT_RETRY_PAUSE_SEC
from .workflow import Workflow
from .workflow import DEFAULT_SCHEDULE_INTERVAL


def interactive_component(**dependencies):
    def decorator(standard_component):
        return InteractiveComponent(standard_component,
                                    {dep_name: dep.config for dep_name, dep in dependencies.items()})
    return decorator


"""
operation_name: used only to identify the operation inside the component so a user can run or peek the single operation.

internal_tables could be generated automatically
dataset manager add tmp table to internal tables but dataset managers are created on each execution
"""

DEFAULT_OPERATION_NAME = '__auto'
DEFAULT_PEEK_LIMIT = 1000
DEFAULT_RUNTIME = '1970-01-01'


class InteractiveDatasetManager(object):
    """Let's you run operations on a dataset, without the need of creating a component."""

    def __init__(self,
                 project_id,
                 dataset_name,
                 internal_tables=None,
                 external_tables=None,
                 extras=None):
        self.config = DatasetConfig(
            project_id=project_id,
            dataset_name=dataset_name,
            internal_tables=internal_tables,
            external_tables=external_tables,
            extras=extras)

    def write_truncate(self, table_name, sql, partitioned=True):
        method = 'write_truncate'
        return self._tmp_interactive_component_factory(
            self._generate_component_name(method=method, table_name=table_name, sql=sql),
            method,
            table_name,
            sql,
            partitioned=partitioned,
            operation_name=DEFAULT_OPERATION_NAME)

    def write_append(self, table_name, sql, partitioned=True):
        method = 'write_append'
        return self._tmp_interactive_component_factory(
            self._generate_component_name(method=method, table_name=table_name, sql=sql),
            method,
            table_name,
            sql,
            partitioned=partitioned,
            operation_name=DEFAULT_OPERATION_NAME)

    def write_tmp(self, table_name, sql):
        method = 'write_tmp'
        return self._tmp_interactive_component_factory(
            self._generate_component_name(method=method, table_name=table_name, sql=sql),
            method,
            table_name,
            sql,
            operation_name=DEFAULT_OPERATION_NAME)

    def collect(self, sql):
        method = 'collect'
        return self._tmp_interactive_component_factory(
            self._generate_component_name(method=method, table_name='', sql=sql),
            method,
            sql,
            operation_name=DEFAULT_OPERATION_NAME)

    def create_table(self, create_query):
        method = 'create_table'
        return self._tmp_interactive_component_factory(
            self._generate_component_name(method=method, table_name='', sql=create_query),
            method,
            create_query,
            operation_name=DEFAULT_OPERATION_NAME)

    def load_table_from_dataframe(self, table_name, df, partitioned=True):
        method = 'load_table_from_dataframe'
        return self._tmp_interactive_component_factory(
            self._generate_component_name(method=method, table_name=table_name, sql=''),
            method,
            table_name=table_name,
            df=df,
            partitioned=partitioned,
            operation_name=DEFAULT_OPERATION_NAME)

    def _generate_component_name(self, method, table_name, sql):
        component_id = hashlib.sha256()
        component_id.update(sql)
        component_id = component_id.hexdigest()
        return '{}_{}_{}'.format(method, table_name, component_id)

    def _tmp_interactive_component_factory(self, component_name, method, *args, **kwargs):
        @interactive_component(dataset_manager=self)
        def tmp_component(dataset_manager):
            return getattr(dataset_manager, method)(*args, **kwargs)

        tmp_component._standard_component.__name__ = component_name
        return tmp_component


def create_workflow(id, components, schedule_interval=DEFAULT_SCHEDULE_INTERVAL):
    return Workflow(id=id, definition=[c.to_job() for c in components], schedule_interval=schedule_interval)


class InteractiveComponent(object):
    """Let's you run the component for the specific runtime
     and peek the operation results as the pandas.DataFrame."""

    def __init__(self, standard_component, dependency_config):
        self._standard_component = standard_component
        self._dependency_config = dependency_config

    def to_job(self, id=None, retry_count=DEFAULT_RETRY_COUNT, retry_pause_sec=DEFAULT_RETRY_PAUSE_SEC):
        _, component_callable = self._component_callable_factory(operation_name=None)
        return Job(
            component=component_callable,
            id=id,
            retry_count=retry_count,
            retry_pause_sec=retry_pause_sec,
            **self._dependency_config)

    def run(self, runtime=DEFAULT_RUNTIME, operation_name=None):
         _, component_callable = self._component_callable_factory(operation_name=operation_name)
         return Job(component_callable, **self._dependency_config).run(runtime)

    def peek(self, runtime, operation_name=DEFAULT_OPERATION_NAME, limit=DEFAULT_PEEK_LIMIT):
        """Returns the result of the specified operation in the form of the pandas.DataFrame, without really running the
        operation and affecting the table."""
        results_container, component_callable = self._component_callable_factory(operation_name=operation_name,
                                                                                 peek=True, peek_limit=limit)
        Job(component_callable, **self._dependency_config).run(runtime)
        try:
            return results_container[0]
        except IndexError:
            if operation_name != DEFAULT_OPERATION_NAME:
                raise ValueError("Operation '{}' not found".format(operation_name))
            else:
                raise ValueError("You haven't specified operation_name.".format(operation_name))

    def __call__(self, **kwargs):
        _, component_callable = self._component_callable_factory()
        return component_callable(**kwargs)

    def _component_callable_factory(self, operation_name=None, peek=None, peek_limit=None):
        operation_settings = {'operation_name': operation_name, 'peek': peek, 'peek_limit': peek_limit}
        results_container = []

        def component_callable(**kwargs):
            operation_level_dataset_managers = {k: OperationLevelDatasetManager(v, **operation_settings)
                                                for k, v in kwargs.items()}

            component_return_value = self._standard_component(**operation_level_dataset_managers)

            for operation_level_dataset_manager in operation_level_dataset_managers.values():
                if operation_level_dataset_manager.result:
                    results_container.extend(operation_level_dataset_manager.result)

            return component_return_value

        component_callable_with_proper_signature = "def reworked_function({signature}):\n    return original_func({kwargs})\n".format(
            signature=','.join([arg for arg in getargspec(self._standard_component).args]),
            kwargs=','.join(['{arg}={arg}'.format(arg=arg) for arg in getargspec(self._standard_component).args]))
        component_callable_with_proper_signature_code = compile(component_callable_with_proper_signature, "fakesource",
                                                                "exec")
        fake_globals = {}
        eval(component_callable_with_proper_signature_code, {'original_func': component_callable}, fake_globals)

        component_callable = fake_globals['reworked_function']
        component_callable.__name__ = operation_name or self._standard_component.__name__

        return results_container, component_callable


class OperationLevelDatasetManager(object):
    """
    Let's you run specified operation or peek a result of a specified operation.
    """

    def __init__(self, dataset_manager, peek=False, operation_name=None, peek_limit=DEFAULT_PEEK_LIMIT):
        self._dataset_manager = dataset_manager
        self._peek = peek
        self._operation_name = operation_name
        self._peek_limit = peek_limit
        self._results_container = []

    def write_truncate(self, table_name, sql, partitioned=True, custom_run_datetime=None, operation_name=None):
        return self._run_write_operation(
            operation_name=operation_name,
            method=self._dataset_manager.write_truncate,
            sql=sql,
            table_name=table_name,
            partitioned=partitioned,
            custom_run_datetime=custom_run_datetime)

    def write_append(self, table_name, sql, partitioned=True, custom_run_datetime=None, operation_name=None):
        return self._run_write_operation(
            operation_name=operation_name,
            method=self._dataset_manager.write_append,
            sql=sql,
            table_name=table_name,
            partitioned=partitioned,
            custom_run_datetime=custom_run_datetime)

    def write_tmp(self, table_name, sql, custom_run_datetime=None, operation_name=None):
        return self._run_write_operation(
            operation_name=operation_name,
            method=self._dataset_manager.write_tmp,
            sql=sql,
            table_name=table_name,
            custom_run_datetime=custom_run_datetime)

    def collect(self, sql, custom_run_datetime=None, operation_name=None):
        return self._run_write_operation(
            operation_name=operation_name,
            method=self._dataset_manager.collect,
            sql=sql,
            custom_run_datetime=custom_run_datetime)

    def create_table(self, create_query, operation_name=None):
        if self._operation_name == operation_name or self._operation_name is None:
            return self._results_container, self._dataset_manager.create_table(create_query)

    def load_table_from_dataframe(self, table_name, df, partitioned=True, custom_run_datetime=None, operation_name=None):
        if self._should_peek_operation_results(operation_name):
            return df
        elif self._should_run_operation(operation_name):
            return self._dataset_manager.load_table_from_dataframe(
                table_name,
                df,
                custom_run_datetime=custom_run_datetime,
                partitioned=partitioned)

    @property
    def runtime_str(self):
        return self._dataset_manager.runtime_str

    @property
    def result(self):
        return self._results_container

    def _collect_select_result_to_pandas(self, sql):
        sql = sql if 'limit' in sql.lower() else sql + '\nLIMIT {}'.format(str(self._peek_limit))
        return self._dataset_manager.collect(sql)

    def _run_write_operation(self, operation_name, method, sql, *args, **kwargs):
        if self._should_peek_operation_results(operation_name):
            result = self._collect_select_result_to_pandas(sql)
            self._results_container.append(result)
            return result
        elif self._should_run_operation(operation_name):
            return method(*args, sql=sql, **kwargs)

    def _should_peek_operation_results(self, operation_name):
        return self._operation_name == operation_name and self._peek is not None

    def _should_run_operation(self, operation_name):
        return self._operation_name == operation_name or self._operation_name is None