from ioflow.performance_reporter import get_performance_reporter


def test_local_performance_reporter():
    config = {
        'performance_reporter_schema': 'local'
    }

    performance_reporter = get_performance_reporter(config)
    performance_reporter.log_performance('k', 'v')
