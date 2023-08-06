import mock
from unittest import TestCase

DEFAULT_SCHEDULE_INTERVAL = '@daily'


class Workflow(object):
    def __init__(self, id, definition, schedule_interval=DEFAULT_SCHEDULE_INTERVAL):
        self.definition = definition
        self.id = id
        self.schedule_interval = schedule_interval

    def __call__(self, runtime):
        return self._run(runtime=runtime)

    def _run(self, runtime):
        for job in self:
            job.run(runtime=runtime)

    def __iter__(self):
        for job in self.definition:
            yield job


class WorkflowTestCase(TestCase):
    def test_should_run_jobs(self):
        # given
        definition = [mock.Mock() for i in range(100)]
        workflow = Workflow(id='test_id', definition=definition)

        # when
        workflow('2019-01-01')

        # then
        for step in definition:
            step.assert_called_with(runtime='2019-01-01')

    def test_should_have_id(self):
        # given
        workflow = Workflow(id='test_id', definition=[])

        # expected
        self.assertEqual(workflow.id, 'test_id')