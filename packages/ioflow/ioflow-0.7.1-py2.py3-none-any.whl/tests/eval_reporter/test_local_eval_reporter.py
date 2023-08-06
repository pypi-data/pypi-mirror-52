from ioflow.eval_reporter import get_eval_reporter


def test_local_eval_reporter():
    config = {
        'eval_reporter_scheme': 'local'
    }

    eval_reporter = get_eval_reporter(config)
    eval_reporter.record_x_and_y('a', 'b')
    eval_reporter.submit()
