from ioflow.model_saver import get_model_saver


def test_local_model_saver():
    config = {
        "model_saver_scheme": "local"
    }

    model_saver = get_model_saver(config)
    model_saver.save_model("path/to/some/where")
