# microcosm-sagemaker
Opinionated machine learning with SageMaker

## Usage
For best practices, see
[`cookiecutter-microcosm-sagemaker`](https://github.com/globality-corp/cookiecutter-microcosm-sagemaker).

## Profiling
Make sure `pyinstrument` is installed, either using `pip install pyinstrument` or by installing `microcosm-sagemaker` with `profiling` extra dependencies:

```
pip install -e '.[profiling]'
```

To enable profiling of the app, use the `--profile` flag with `runserver`:

```
runserver --profile
```

The service will log that it is in profiling mode and announce the directory to which it is exporting. Each call to the endpoint will be profiled and its results with be stored in a time-tagged html file in the profiling directory.