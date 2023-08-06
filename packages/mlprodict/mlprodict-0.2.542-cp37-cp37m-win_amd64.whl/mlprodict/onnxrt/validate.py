"""
@file
@brief Validates runtime for many :scikit-learn: operators.
The submodule relies on :epkg:`onnxconverter_common`,
:epkg:`sklearn-onnx`.
"""
from timeit import Timer
import numpy
import pandas
import sklearn
from sklearn import __all__ as sklearn__all__, __version__ as sklearn_version
from sklearn.model_selection import train_test_split
from .onnx_inference import OnnxInference
from .. import __version__ as ort_version
from .validate_problems import _problems, find_suitable_problem
from .validate_scenarios import _extra_parameters
from .validate_difference import measure_relative_difference
from .validate_helper import (
    _dispsimple, get_opset_number_from_onnx, sklearn_operators,
    to_onnx, _measure_time, _shape_exc, dump_into_folder
)


def _get_problem_data(prob):
    data_problem = _problems[prob]()
    if len(data_problem) == 6:
        X_, y_, init_types, method, output_index, Xort_ = data_problem
        dofit = True
    elif len(data_problem) == 7:
        X_, y_, init_types, method, output_index, Xort_, dofit = data_problem
    else:
        raise RuntimeError(
            "Unable to interpret problem '{}'.".format(prob))
    if y_ is None:
        (X_train, X_test, Xort_train,  # pylint: disable=W0612
            Xort_test) = train_test_split(
                X_, Xort_, random_state=42)
        y_train, y_test = None, None
    else:
        (X_train, X_test, y_train, y_test,  # pylint: disable=W0612
            Xort_train, Xort_test) = train_test_split(
                X_, y_, Xort_, random_state=42)
    if isinstance(init_types, tuple):
        init_types, conv_options = init_types
    else:
        conv_options = None

    if isinstance(method, tuple):
        method_name, predict_kwargs = method
    else:
        method_name = method
        predict_kwargs = {}

    return (X_train, X_test, y_train,
            y_test, Xort_test,
            init_types, conv_options, method_name,
            output_index, dofit, predict_kwargs)


def _dofit_model(dofit, obs, inst, X_train, y_train, X_test, y_test,
                 Xort_test, init_types, store_models,
                 debug, verbose, fLOG):
    if dofit:
        if verbose >= 2 and fLOG is not None:
            fLOG("[enumerate_compatible_opset] fit, type: '{}'".format(type(X_train)))
        try:
            if y_train is None:
                t4 = _measure_time(lambda: inst.fit(X_train))[1]
            else:
                t4 = _measure_time(
                    lambda: inst.fit(X_train, y_train))[1]
        except (AttributeError, TypeError, ValueError,
                IndexError, NotImplementedError, MemoryError) as e:
            if debug:
                raise
            obs["_1training_time_exc"] = str(e)
            return False

        obs["training_time"] = t4
        if store_models:
            obs['MODEL'] = inst
            obs['X_test'] = X_test
            obs['Xort_test'] = Xort_test
            obs['init_types'] = init_types
    else:
        obs["training_time"] = 0.
        if store_models:
            obs['MODEL'] = inst
            obs['init_types'] = init_types

    return True


def _run_skl_prediction(obs, check_runtime, assume_finite, inst,
                        method_name, predict_kwargs, X_test,
                        benchmark, debug, verbose, fLOG):
    if not check_runtime:
        return None
    if verbose >= 2 and fLOG is not None:
        fLOG("[enumerate_compatible_opset] check_runtime SKL {}-{}-{}".format(
            id(inst), method_name, predict_kwargs))
    with sklearn.config_context(assume_finite=assume_finite):
        # compute sklearn prediction
        obs['ort_version'] = ort_version
        try:
            meth = getattr(inst, method_name)
        except AttributeError as e:
            if debug:
                raise
            obs['_2skl_meth_exc'] = str(e)
            return e
        try:
            ypred, t4 = _measure_time(
                lambda: meth(X_test, **predict_kwargs))
            obs['lambda-skl'] = (lambda xo: meth(xo, **predict_kwargs), X_test)
        except (ValueError, AttributeError, TypeError, MemoryError, IndexError) as e:
            if debug:
                raise
            obs['_3prediction_exc'] = str(e)
            return e
        obs['prediction_time'] = t4
        obs['assume_finite'] = assume_finite
        if benchmark and 'lambda-skl' in obs:
            obs['bench-skl'] = benchmark_fct(
                *obs['lambda-skl'], obs=obs)
        if verbose >= 3 and fLOG is not None:
            fLOG("[enumerate_compatible_opset] scikit-learn prediction")
            _dispsimple(ypred, fLOG)
        if verbose >= 2 and fLOG is not None:
            fLOG("[enumerate_compatible_opset] predictions stored")
    return ypred


def enumerate_compatible_opset(model, opset_min=9, opset_max=None,
                               check_runtime=True, debug=False,
                               runtime='python', dump_folder=None,
                               store_models=False, benchmark=False,
                               assume_finite=True, node_time=False,
                               fLOG=print, filter_exp=None,
                               verbose=0, extended_list=False):
    """
    Lists all compatible opsets for a specific model.

    @param      model           operator class
    @param      opset_min       starts with this opset
    @param      opset_max       ends with this opset (None to use
                                current onnx opset)
    @param      check_runtime   checks that runtime can consume the
                                model and compute predictions
    @param      debug           catch exception (True) or not (False)
    @param      runtime         test a specific runtime, by default ``'python'``
    @param      dump_folder     dump information to replicate in case of mismatch
    @param      store_models    if True, the function
                                also stores the fitted model and its conversion
                                into :epkg:`ONNX`
    @param      benchmark       if True, measures the time taken by each function
                                to predict for different number of rows
    @param      fLOG            logging function
    @param      filter_exp      function which tells if the experiment must be run,
                                None to run all, takes *model, problem* as an input
    @param      node_time       collect time for each node in the :epkg:`ONNX` graph
    @param      assume_finite   See `config_context
                                <https://scikit-learn.org/stable/modules/generated/
                                sklearn.config_context.html>`_, If True, validation for finiteness
                                will be skipped, saving time, but leading to potential crashes.
                                If False, validation for finiteness will be performed, avoiding error.
    @param      verbose         verbosity
    @param      extended_list   extends the list to custom converters
                                and problems
    @return                     dictionaries, each row has the following
                                keys: opset, exception if any, conversion time,
                                problem chosen to test the conversion...

    The function requires :epkg:`sklearn-onnx`.
    The outcome can be seen at pages references
    by :ref:`l-onnx-availability`.
    """
    if extended_list:
        from ..onnx_conv.validate_scenarios import find_suitable_problem as fsp_extended
        problems = fsp_extended(model)
        if problems is not None:
            from ..onnx_conv.validate_scenarios import build_custom_scenarios as fsp_scenarios
            extra_parameters = fsp_scenarios()

            if verbose >= 2 and fLOG is not None:
                fLOG(
                    "[enumerate_compatible_opset] found custom for model={}".format(model))
                extras = extra_parameters.get(model, None)
                if extras is not None:
                    fLOG(
                        "[enumerate_compatible_opset] found custom scenarios={}".format(extras))
    else:
        problems = None

    if problems is None:
        # scikit-learn
        extra_parameters = _extra_parameters
        try:
            problems = find_suitable_problem(model)
        except RuntimeError as e:
            yield {'name': model.__name__, 'skl_version': sklearn_version,
                   '_0problem_exc': e}
            problems = []

    extras = extra_parameters.get(model, [('default', {})])

    if opset_max is None:
        opset_max = get_opset_number_from_onnx()
    opsets = list(range(opset_min, opset_max + 1))
    opsets.append(None)

    if extras is None:
        problems = []
        yield {'name': model.__name__, 'skl_version': sklearn_version,
               '_0problem_exc': 'SKIPPED'}

    for prob in problems:
        if filter_exp is not None and not filter_exp(model, prob):
            continue
        if verbose >= 2 and fLOG is not None:
            fLOG("[enumerate_compatible_opset] problem={}".format(prob))

        (X_train, X_test, y_train,
         y_test, Xort_test,
         init_types, conv_options, method_name,
         output_index, dofit, predict_kwargs) = _get_problem_data(prob)

        for scenario_extra in extras:
            if len(scenario_extra) > 2:
                subset_problems = scenario_extra[2]
                if prob not in subset_problems:
                    # Skips unrelated problem for a specific configuration.
                    continue
            scenario, extra = scenario_extra[:2]

            if verbose >= 2 and fLOG is not None:
                fLOG("[enumerate_compatible_opset] ##############################")
                fLOG("[enumerate_compatible_opset] scenario={} extra={} dofit={} (problem={})".format(
                    scenario, extra, dofit, prob))

            # training
            obs = {'scenario': scenario, 'name': model.__name__,
                   'skl_version': sklearn_version, 'problem': prob,
                   'method_name': method_name, 'output_index': output_index,
                   'fit': dofit, 'conv_options': conv_options,
                   'idtype': Xort_test.dtype,
                   'predict_kwargs': predict_kwargs, 'init_types': init_types}
            inst = None
            try:
                inst = model(**extra)
            except TypeError as e:
                if debug:
                    raise
                import pprint
                raise RuntimeError(
                    "Unable to instantiate model '{}'.\nextra=\n{}".format(
                        model.__name__, pprint.pformat(extra))) from e

            if not _dofit_model(dofit, obs, inst, X_train, y_train, X_test, y_test,
                                Xort_test, init_types, store_models,
                                debug, verbose, fLOG):
                yield obs
                continue

            # runtime
            ypred = _run_skl_prediction(
                obs, check_runtime, assume_finite, inst,
                method_name, predict_kwargs, X_test,
                benchmark, debug, verbose, fLOG)
            if isinstance(ypred, Exception):
                yield obs
                continue

            # converting
            for opset in opsets:
                if verbose >= 2 and fLOG is not None:
                    fLOG("[enumerate_compatible_opset] opset={}".format(opset))
                obs_op = obs.copy()
                if opset is not None:
                    obs_op['opset'] = opset

                if len(init_types) != 1:
                    raise NotImplementedError("Multiple types are is not implemented: "
                                              "{}.".format(init_types))

                def fct_conv(itt=inst, it=init_types[0][1], ops=opset, options=conv_options):  # pylint: disable=W0102
                    return to_onnx(itt, it, target_opset=ops, options=options,
                                   dtype=init_types[0][1], rewrite_ops=runtime == "python")

                if verbose >= 2 and fLOG is not None:
                    fLOG("[enumerate_compatible_opset] conversion to onnx")
                try:
                    conv, t4 = _measure_time(fct_conv)
                    obs_op["convert_time"] = t4
                except (RuntimeError, IndexError, AttributeError) as e:
                    if debug:
                        import pprint
                        fLOG("--------------------")
                        fLOG(pprint.pformat(obs_op))
                        raise
                    obs_op["_4convert_exc"] = e
                    yield obs_op
                    continue

                if store_models:
                    obs_op['ONNX'] = conv

                # opset_domain
                for op_imp in list(conv.opset_import):
                    obs_op['domain_opset_%s' % op_imp.domain] = op_imp.version

                # prediction
                if check_runtime:
                    yield _call_runtime(obs_op=obs_op, conv=conv, opset=opset, debug=debug,
                                        runtime=runtime, inst=inst,
                                        X_test=X_test, y_test=y_test,
                                        init_types=init_types,
                                        method_name=method_name,
                                        output_index=output_index,
                                        ypred=ypred, Xort_test=Xort_test,
                                        model=model, dump_folder=dump_folder,
                                        benchmark=benchmark and opset == opsets[-1],
                                        node_time=node_time,
                                        fLOG=fLOG, verbose=verbose,
                                        store_models=store_models)
                else:
                    yield obs_op


def _call_runtime(obs_op, conv, opset, debug, inst, runtime,
                  X_test, y_test, init_types, method_name, output_index,
                  ypred, Xort_test, model, dump_folder,
                  benchmark, node_time, fLOG,
                  verbose, store_models):
    """
    Private.
    """
    ser, t5 = _measure_time(lambda: conv.SerializeToString())
    obs_op['tostring_time'] = t5
    obs_op['runtime'] = runtime

    # load
    if verbose >= 2 and fLOG is not None:
        fLOG("[enumerate_compatible_opset] load onnx")
    try:
        sess, t5 = _measure_time(
            lambda: OnnxInference(ser, runtime=runtime))
        obs_op['tostring_time'] = t5
    except (RuntimeError, ValueError, KeyError, IndexError) as e:
        if debug:
            raise
        obs_op['_5ort_load_exc'] = e
        return obs_op

    # compute batch
    if store_models:
        obs_op['OINF'] = sess
    if verbose >= 2 and fLOG is not None:
        fLOG("[enumerate_compatible_opset] compute batch")

    def fct_batch(se=sess, xo=Xort_test, it=init_types):  # pylint: disable=W0102
        return se.run({it[0][0]: xo},
                      verbose=max(verbose - 1, 1) if debug else 0, fLOG=fLOG)

    try:
        opred, t5 = _measure_time(fct_batch)
        obs_op['ort_run_time_batch'] = t5
        obs_op['lambda-batch'] = (lambda xo: sess.run(
            {init_types[0][0]: xo}, node_time=node_time), Xort_test)
    except (RuntimeError, TypeError, ValueError, KeyError, IndexError) as e:
        if debug:
            raise e
        obs_op['_6ort_run_batch_exc'] = e
    if (benchmark or node_time) and 'lambda-batch' in obs_op:
        try:
            benres = benchmark_fct(
                *obs_op['lambda-batch'], obs=obs_op, node_time=node_time)
            obs_op['bench-batch'] = benres
        except RuntimeError as e:
            if debug:
                raise e
            obs_op['_6ort_run_batch_exc'] = e
            obs_op['_6ort_run_batch_bench_exc'] = e

    # difference
    debug_exc = []
    if verbose >= 2 and fLOG is not None:
        fLOG("[enumerate_compatible_opset] differences")
    if '_6ort_run_batch_exc' not in obs_op:
        if isinstance(opred, dict):
            ch = [(k, v) for k, v in opred.items()]
            opred = [_[1] for _ in ch]

        if output_index != 'all':
            try:
                opred = opred[output_index]
            except IndexError:
                if debug:
                    raise
                obs_op['_8max_rel_diff_batch_exc'] = (
                    "Unable to fetch output {}/{} for model '{}'"
                    "".format(output_index, len(opred),
                              model.__name__))
                opred = None

        if opred is not None:
            if store_models:
                obs_op['skl_outputs'] = ypred
                obs_op['ort_outputs'] = opred
            if verbose >= 3 and fLOG is not None:
                fLOG("[_call_runtime] runtime prediction")
                _dispsimple(opred, fLOG)
            max_rel_diff = measure_relative_difference(
                ypred, opred)
            if max_rel_diff >= 1e9 and debug:
                raise RuntimeError(
                    "Big difference:\n-------\n{}\n--------\n{}".format(
                        ypred, opred))
            if numpy.isnan(max_rel_diff):
                obs_op['_8max_rel_diff_batch_exc'] = (
                    "Unable to compute differences between"
                    " {}-{}\n{}\n--------\n{}".format(
                        _shape_exc(
                            ypred), _shape_exc(opred),
                        ypred, opred))
                if debug:
                    debug_exc.append(RuntimeError(
                        obs_op['_8max_rel_diff_batch_exc']))
            else:
                obs_op['max_rel_diff_batch'] = max_rel_diff
                if dump_folder and max_rel_diff > 1e-5:
                    dump_into_folder(dump_folder, kind='batch', obs_op=obs_op,
                                     X_test=X_test, y_test=y_test, Xort_test=Xort_test)
                if debug and max_rel_diff >= 0.1:
                    import pprint
                    raise RuntimeError("Two big differences {}\n{}\n{}\n{}".format(
                        max_rel_diff, inst, conv, pprint.pformat(obs_op)))

    if debug and len(debug_exc) == 2:
        raise debug_exc[0]
    if debug and verbose >= 2:
        import pprint
        fLOG(pprint.pformat(obs_op))
    if verbose >= 2 and fLOG is not None:
        fLOG("[enumerate_compatible_opset] next...")
    return obs_op


def enumerate_validated_operator_opsets(verbose=0, opset_min=9, opset_max=None,
                                        check_runtime=True, debug=False, runtime='python',
                                        models=None, dump_folder=None, store_models=False,
                                        benchmark=False, skip_models=None,
                                        assume_finite=True, node_time=False,
                                        fLOG=print, filter_exp=None,
                                        versions=False, dtype=numpy.float32,
                                        extended_list=False):
    """
    Tests all possible configuration for all possible
    operators and returns the results.

    @param      verbose         integer 0, 1, 2
    @param      opset_min       checks conversion starting from the opset
    @param      opset_max       checks conversion up to this opset,
                                None means @see fn get_opset_number_from_onnx.
    @param      check_runtime   checks the python runtime
    @param      models          only process a small list of operators,
                                set of model names
    @param      debug           stops whenever an exception
                                is raised
    @param      runtime         test a specific runtime, by default ``'python'``
    @param      dump_folder     dump information to replicate in case of mismatch
    @param      store_models    if True, the function
                                also stores the fitted model and its conversion
                                into :epkg:`ONNX`
    @param      benchmark       if True, measures the time taken by each function
                                to predict for different number of rows
    @param      filter_exp      function which tells if the experiment must be run,
                                None to run all, takes *model, problem* as an input
    @param      skip_models     models to skip
    @param      assume_finite   See `config_context
                                <https://scikit-learn.org/stable/modules/generated/
                                sklearn.config_context.html>`_, If True, validation for finiteness
                                will be skipped, saving time, but leading to potential crashes.
                                If False, validation for finiteness will be performed, avoiding error.
    @param      node_time       measure time execution for every node in the graph
    @param      versions        add columns with versions of used packages,
                                :epkg:`numpy`, :epkg:`scikit-learn`, :epkg:`onnx`,
                                :epkg:`onnxruntime`, :epkg:`sklearn-onnx`
    @param      dtype           force the conversion to use that type
    @param      extended_list   also check models this module implements a converter for
    @param      fLOG            logging function
    @return                     list of dictionaries

    The function is available through command line
    :ref:`validate_runtime <l-cmd-validate_runtime>`.
    """
    ops = [_ for _ in sklearn_operators(extended=extended_list)]

    if models is not None:
        if not all(map(lambda m: isinstance(m, str), models)):
            raise ValueError("models must be a set of strings.")
        ops_ = [_ for _ in ops if _['name'] in models]
        if len(ops) == 0:
            raise ValueError("Parameter models is wrong: {}\n{}".format(
                models, ops[0]))
        ops = ops_
    if skip_models is not None:
        ops = [m for m in ops if m['name'] not in skip_models]

    if verbose > 0:

        def iterate():
            for i, row in enumerate(ops):
                fLOG("{}/{} - {}".format(i + 1, len(ops), row))
                yield row

        if verbose >= 11:
            verbose -= 10
            loop = iterate()
        else:
            try:
                from tqdm import trange

                def iterate_tqdm():
                    with trange(len(ops)) as t:
                        for i in t:
                            row = ops[i]
                            disp = row['name'] + " " * (28 - len(row['name']))
                            t.set_description("%s" % disp)
                            yield row

                loop = iterate_tqdm()

            except ImportError:
                loop = iterate()
    else:
        loop = ops

    if versions:
        from numpy import __version__ as numpy_version
        from onnx import __version__ as onnx_version
        from scipy import __version__ as scipy_version
        from skl2onnx import __version__ as skl2onnx_version
        add_versions = {'v_numpy': numpy_version, 'v_onnx': onnx_version,
                        'v_scipy': scipy_version, 'v_skl2onnx': skl2onnx_version,
                        'v_sklearn': sklearn_version, 'v_onnxruntime': ort_version}
        if "onnxruntime" in runtime:
            from onnxruntime import __version__ as onnxrt_version
            add_versions['v_onnxruntime'] = onnxrt_version
    else:
        add_versions = {}

    current_opset = get_opset_number_from_onnx()
    for row in loop:

        model = row['cl']

        for obs in enumerate_compatible_opset(
                model, opset_min=opset_min, opset_max=opset_max,
                check_runtime=check_runtime, runtime=runtime,
                debug=debug, dump_folder=dump_folder,
                store_models=store_models, benchmark=benchmark,
                fLOG=fLOG, filter_exp=filter_exp,
                assume_finite=assume_finite, node_time=node_time,
                verbose=verbose, extended_list=extended_list):

            if verbose > 1:
                fLOG("  ", obs)
            elif verbose > 0 and "_0problem_exc" in obs:
                fLOG("  ???", obs)

            diff = obs.get('max_rel_diff_batch', None)
            batch = 'max_rel_diff_batch' in obs and diff is not None
            op1 = obs.get('domain_opset_', '')
            op2 = obs.get('domain_opset_ai.onnx.ml', '')
            op = '{}/{}'.format(op1, op2)

            if diff is not None:
                if diff < 1e-5:
                    obs['available'] = 'OK'
                elif diff < 0.0001:
                    obs['available'] = 'e<0.0001'
                elif diff < 0.001:
                    obs['available'] = 'e<0.001'
                elif diff < 0.01:
                    obs['available'] = 'e<0.01'
                elif diff < 0.1:
                    obs['available'] = 'e<0.1'
                else:
                    obs['available'] = "ERROR->=%1.1f" % diff
                obs['available'] += '-' + op
                if not batch:
                    obs['available'] += "-NOBATCH"

            excs = []
            for k, v in sorted(obs.items()):
                if k.endswith('_exc'):
                    excs.append((k, v))
                    break
            if 'opset' not in obs:
                # It fails before the conversion happens.
                obs['opset'] = current_opset
            if obs['opset'] == current_opset and len(excs) > 0:
                k, v = excs[0]
                obs['available'] = 'ERROR-%s' % k
                obs['available-ERROR'] = v

            if 'bench-skl' in obs:
                b1 = obs['bench-skl']
                if 'bench-batch' in obs:
                    b2 = obs['bench-batch']
                else:
                    b2 = None
                if b1 is not None and b2 is not None:
                    for k in b1:
                        if k in b2 and b2[k] is not None and b1[k] is not None:
                            key = 'time-ratio-N=%d' % k
                            obs[key] = b2[k]['average'] / b1[k]['average']

            obs.update(row)
            obs.update(add_versions)
            yield obs


def summary_report(df):
    """
    Finalizes the results computed by function
    @see fn enumerate_validated_operator_opsets.

    @param      df      dataframe
    @return             pivoted dataframe

    The outcome can be seen at page about :ref:`l-onnx-pyrun`.
    """

    def aggfunc(values):
        if len(values) != 1:
            values = [str(_).replace("\n", " ").replace('\r', '').strip(" ")
                      for _ in values]
            values = [_ for _ in values if _]
            vals = set(values)
            if len(vals) != 1:
                return " // ".join(map(str, values))
        val = values.iloc[0] if not isinstance(values, list) else values[0]
        if isinstance(val, float) and numpy.isnan(val):
            return ""
        else:
            return str(val)

    if 'opset' not in df.columns:
        raise RuntimeError("Unable to create sumary (opset missing)\n{}\n--\n{}".format(
            df.columns, df.head()))

    col_values = ["available"]
    for col in ['problem', 'scenario', 'opset']:
        if col not in df.columns:
            df[col] = '' if col != 'opset' else numpy.nan
    piv = pandas.pivot_table(df, values=col_values,
                             index=['name', 'problem', 'scenario'],
                             columns='opset',
                             aggfunc=aggfunc).reset_index(drop=False)

    opmin = min(df['opset'].dropna())
    versions = ["opset%d" % (opmin + t - 1)
                for t in range(1, piv.shape[1] - 2)]
    indices = ["name", "problem", "scenario"]
    cols = list(piv.columns)
    piv.columns = indices + versions
    piv = piv[indices + list(reversed(versions))].copy()

    if "available-ERROR" in df.columns:

        from skl2onnx.common.exceptions import MissingShapeCalculator

        def replace_msg(text):
            if isinstance(text, MissingShapeCalculator):
                return "NO CONVERTER"
            if str(text).startswith("Unable to find a shape calculator for type '"):
                return "NO CONVERTER"
            if str(text).startswith("Unable to find problem for model '"):
                return "NO PROBLEM"
            if "not implemented for float64" in str(text):
                return "NO RUNTIME 64"
            return str(text)

        piv2 = pandas.pivot_table(df, values="available-ERROR",
                                  index=['name', 'problem', 'scenario'],
                                  columns='opset',
                                  aggfunc=aggfunc).reset_index(drop=False)

        col = piv2.iloc[:, piv2.shape[1] - 1]
        piv["ERROR-msg"] = col.apply(replace_msg)

    if "time-ratio-N=1" in df.columns:
        cols = [c for c in df.columns if c.startswith('time-ratio')]
        cols.sort()

        df_sub = df[['name', 'problem', 'scenario'] + cols]
        piv2 = df_sub.groupby(['name', 'problem', 'scenario']).mean()
        piv = piv.merge(piv2, on=['name', 'problem', 'scenario'], how='left')

        def rep(c):
            if 'N=1' in c and 'N=10' not in c:
                return c.replace("time-ratio-", "RT/SKL-")
            else:
                return c.replace("time-ratio-", "")
        cols = [rep(c) for c in piv.columns]
        piv.columns = cols

    def clean_values(value):
        if not isinstance(value, str):
            return value
        if "ERROR->=1000000" in value:
            value = "big-diff"
        elif "ERROR" in value:
            value = value.replace("ERROR-_", "")
            value = value.replace("_exc", "")
            value = "ERR: " + value
        elif "OK-" in value:
            value = value.replace("OK-", "OK ")
        elif "e<" in value:
            value = value.replace("-", " ")
        return value

    for c in piv.columns:
        if "opset" in c:
            piv[c] = piv[c].apply(clean_values)

    # adding versions
    col_versions = [c for c in df.columns if c.startswith("v_")]
    if len(col_versions) > 0:
        for c in col_versions:
            vals = set(df[c])
            if len(vals) != 1:
                raise RuntimeError(
                    "Columns '{}' has multiple values {}.".format(c, vals))
            piv[c] = list(vals)[0]

    return piv


def measure_time(stmt, x, repeat=10, number=50, div_by_number=False):
    """
    Measures a statement and returns the results as a dictionary.

    @param      stmt            string
    @param      x               matrix
    @param      repeat          average over *repeat* experiment
    @param      number          number of executions in one row
    @param      div_by_number   divide by the number of executions
    @return                     dictionary

    See `Timer.repeat <https://docs.python.org/3/library/timeit.html?timeit.Timer.repeat>`_
    for a better understanding of parameter *repeat* and *number*.
    The function returns a duration corresponding to
    *number* times the execution of the main statement.
    """
    if x is None:
        raise ValueError("x cannot be None")

    try:
        stmt(x)
    except RuntimeError as e:
        raise RuntimeError("{}-{}".format(type(x), x.dtype)) from e

    def fct():
        stmt(x)

    tim = Timer(fct)
    res = numpy.array(tim.repeat(repeat=repeat, number=number))
    total = numpy.sum(res)
    if div_by_number:
        res /= number
    mean = numpy.mean(res)
    dev = numpy.mean(res ** 2)
    dev = (dev - mean**2) ** 0.5
    mes = dict(average=mean, deviation=dev, min_exec=numpy.min(res),
               max_exec=numpy.max(res), repeat=repeat, number=number,
               total=total)
    return mes


def benchmark_fct(fct, X, time_limit=4, obs=None, node_time=False):
    """
    Benchmarks a function which takes an array
    as an input and changes the number of rows.

    @param      fct         function to benchmark, signature
                            is fct(xo)
    @param      X           array
    @param      time_limit  above this time, measurement as stopped
    @param      obs         all information available in a dictionary
    @param      node_time   measure time execution for each node in the graph
    @return                 dictionary with the results

    The function uses *obs* to reduce the number of tries it does.
    :epkg:`sklearn:gaussian_process:GaussianProcessRegressor`
    produces huge *NxN* if predict method is called
    with ``return_cov=True``.
    """

    def make(x, n):
        if n < x.shape[0]:
            return x[:n].copy()
        elif len(x.shape) < 2:
            r = numpy.empty((N, ), dtype=x.dtype)
            for i in range(0, N, x.shape[0]):
                end = min(i + x.shape[0], N)
                r[i: end] = x[0: end - i]
        else:
            r = numpy.empty((N, x.shape[1]), dtype=x.dtype)
            for i in range(0, N, x.shape[0]):
                end = min(i + x.shape[0], N)
                r[i: end, :] = x[0: end - i, :]
        return r

    def allow(N, obs):
        if obs is None:
            return True
        prob = obs['problem']
        if "-cov" in prob and N > 1000:
            return False
        return True

    res = {}
    for N in [1, 10, 100, 1000, 10000, 100000]:
        if not allow(N, obs):
            continue
        x = make(X, N)
        if N <= 10:
            repeat = 20
            number = 20
        elif N <= 1000:
            repeat = 5
            number = 5
        elif N <= 10000:
            repeat = 3
            number = 3
        else:
            repeat = 1
            number = 1
        if node_time:
            fct(x)
            main = None
            for __ in range(repeat):
                agg = None
                for _ in range(number):
                    ms = fct(x)[1]
                    if agg is None:
                        agg = ms
                        for row in agg:
                            row['N'] = N
                    else:
                        if len(agg) != len(ms):
                            raise RuntimeError(
                                "Not the same number of nodes {} != {}.".format(len(agg), len(ms)))
                        for a, b in zip(agg, ms):
                            a['time'] += b['time']
                if main is None:
                    main = agg
                else:
                    if len(agg) != len(main):
                        raise RuntimeError(
                            "Not the same number of nodes {} != {}.".format(len(agg), len(main)))
                    for a, b in zip(main, agg):
                        a['time'] += b['time']
                        a['max_time'] = max(
                            a.get('max_time', b['time']), b['time'])
                        a['min_time'] = min(
                            a.get('min_time', b['time']), b['time'])
            for row in main:
                row['repeat'] = repeat
                row['number'] = number
                row['time'] /= repeat * number
                if 'max_time' in row:
                    row['max_time'] /= number
                    row['min_time'] /= number
                else:
                    row['max_time'] = row['time']
                    row['min_time'] = row['time']
            res[N] = main
        else:
            res[N] = measure_time(fct, x, repeat=repeat,
                                  number=number, div_by_number=True)
        if (not node_time and res[N] is not None and
                res[N].get('total', time_limit) >= time_limit):
            # too long
            break
    if node_time:
        rows = []
        for _, v in res.items():
            rows.extend(v)
        return rows
    else:
        return res
