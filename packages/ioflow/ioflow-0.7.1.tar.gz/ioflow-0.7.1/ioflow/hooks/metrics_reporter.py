import functools

import tensorflow as tf

from ioflow.performance_metrics import BasePerformanceMetrics, get_performance_metrics


class MetricsReporterHook(tf.train.LoggingTensorHook):
    def __init__(self, tensors,
                 performance_metrics: BasePerformanceMetrics,
                 every_n_iter=None,
                 every_n_secs=None,
                 at_end=False):

        self.performance_metrics = performance_metrics

        super().__init__(tensors,
                         every_n_iter,
                         every_n_secs,
                         at_end)

    def _log_tensors(self, tensor_values):
        stats = {}
        elapsed_secs, _ = self._timer.update_last_triggered_step(self._iter_count)
        for tag in self._tag_order:
            stats[tag] = tensor_values[tag]

        self.performance_metrics.send_metrics(stats)


def metrics_report_hook(config):
    pm = get_performance_metrics(config)

    hook = functools.partial(MetricsReporterHook, performance_metrics=pm, every_n_iter=1)
    return hook
