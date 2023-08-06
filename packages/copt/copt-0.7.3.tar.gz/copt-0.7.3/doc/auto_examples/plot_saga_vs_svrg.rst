.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_plot_saga_vs_svrg.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_saga_vs_svrg.py:


SAGA vs SVRG
===========================================

A comparison between two variance-reduced stochastic gradient methods:
SAGA (implemented in :func:`copt.minimize_saga`) and SVRG (implemented in
:func:`copt.minimize_svrg`). The problem solved in this case is the sum of a
logistic regression and an L1 norm (sometimes referred to as sparse logistic)



.. image:: /auto_examples/images/sphx_glr_plot_saga_vs_svrg_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

      0%|          | 0/100 [00:00<?, ?it/s]    SAGA:   0%|          | 0/100 [00:00<?, ?it/s]    SAGA:   0%|          | 0/100 [00:00<?, ?it/s, tol=5.67]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=5.67]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=3.23]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=1.93]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.911]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.538]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.258]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.146]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.0786]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.0433]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.0254]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.0152]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.00925]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.0058]     SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.00354]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.00246]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.00159]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.00111]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.000722]    SAGA:   1%|1         | 1/100 [00:00<01:12,  1.37it/s, tol=0.000518]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=0.000518]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=0.000328]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=0.000246]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=0.000153]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=0.000112]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=7.76e-5]     SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=5.33e-5]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=3.79e-5]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=2.58e-5]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=1.78e-5]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=1.18e-5]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=8.51e-6]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=5.81e-6]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=4.23e-6]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=2.88e-6]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=2.02e-6]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=1.31e-6]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=9.87e-7]    SAGA:  19%|#9        | 19/100 [00:00<00:41,  1.95it/s, tol=6.8e-7]     SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=6.8e-7]    SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=4.69e-7]    SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=3.4e-7]     SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=2.38e-7]    SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=1.65e-7]    SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=1.09e-7]    SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=7.98e-8]    SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=5.6e-8]     SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=3.94e-8]    SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=2.78e-8]    SAGA:  37%|###7      | 37/100 [00:00<00:22,  2.77it/s, tol=1.96e-8]    SAGA:  37%|###7      | 37/100 [00:01<00:22,  2.77it/s, tol=1.35e-8]    SAGA:  37%|###7      | 37/100 [00:01<00:22,  2.77it/s, tol=9.65e-9]    SAGA:  37%|###7      | 37/100 [00:01<00:22,  2.77it/s, tol=6.77e-9]    SAGA:  37%|###7      | 37/100 [00:01<00:22,  2.77it/s, tol=4.92e-9]    SAGA:  37%|###7      | 37/100 [00:01<00:22,  2.77it/s, tol=3.35e-9]    SAGA:  37%|###7      | 37/100 [00:01<00:22,  2.77it/s, tol=2.46e-9]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=2.46e-9]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=1.67e-9]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=1.19e-9]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=8.81e-10]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=5.85e-10]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=4.32e-10]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=2.98e-10]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=2.08e-10]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=1.55e-10]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=1.03e-10]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=7.4e-11]     SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=5.27e-11]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=3.69e-11]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=2.71e-11]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=1.87e-11]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=1.33e-11]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=9.27e-12]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=6.86e-12]    SAGA:  53%|#####3    | 53/100 [00:01<00:11,  3.93it/s, tol=4.53e-12]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=4.53e-12]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=3.4e-12]     SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=2.25e-12]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=1.66e-12]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=1.17e-12]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=7.93e-13]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=6.04e-13]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=4.1e-13]     SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=2.93e-13]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=2.01e-13]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=1.4e-13]     SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=9.91e-14]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=6.67e-14]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=4.82e-14]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=3.04e-14]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=1.96e-14]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=1.21e-14]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=7.27e-15]    SAGA:  71%|#######1  | 71/100 [00:01<00:05,  5.56it/s, tol=3.61e-15]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=3.61e-15]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=1.97e-15]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=1.42e-15]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=1.06e-15]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=1.03e-15]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=1.1e-15]     SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=9.91e-16]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=7.85e-16]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=9.36e-16]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=8.42e-16]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=7.54e-16]    SAGA:  89%|########9 | 89/100 [00:01<00:01,  7.83it/s, tol=6.67e-16]    SAGA: 100%|##########| 100/100 [00:01<00:00, 75.86it/s, tol=6.67e-16]
    /usr/local/google/home/pedregosa/anaconda3/lib/python3.6/site-packages/matplotlib/axes/_base.py:3449: MatplotlibDeprecationWarning: 
    The `ymin` argument was deprecated in Matplotlib 3.0 and will be removed in 3.2. Use `bottom` instead.
      alternative='`bottom`', obj_type='argument')





|


.. code-block:: default

    import copt as cp
    import matplotlib.pyplot as plt
    import numpy as np

    # .. construct (random) dataset ..
    n_samples, n_features = 1000, 200
    np.random.seed(0)
    X = np.random.randn(n_samples, n_features)
    y = np.random.rand(n_samples)

    # .. objective function and regularizer ..
    f = cp.utils.LogLoss(X, y)
    g = cp.utils.L1Norm(1.0 / n_samples)

    # .. callbacks to track progress ..
    cb_saga = cp.utils.Trace(lambda x: f(x) + g(x))
    cb_svrg = cp.utils.Trace(lambda x: f(x) + g(x))

    # .. run the SAGA and SVRG algorithms ..
    step_size = 1.0 / (3 * f.max_lipschitz)
    result_saga = cp.minimize_saga(
        f.partial_deriv,
        X,
        y,
        np.zeros(n_features),
        prox=g.prox_factory(n_features),
        step_size=step_size,
        callback=cb_saga,
        tol=0,
        max_iter=100,
    )

    result_svrg = cp.minimize_svrg(
        f.partial_deriv,
        X,
        y,
        np.zeros(n_features),
        prox=g.prox_factory(n_features),
        step_size=step_size,
        callback=cb_svrg,
        tol=0,
        max_iter=100,
    )


    # .. plot the result ..
    fmin = min(np.min(cb_saga.trace_fx), np.min(cb_svrg.trace_fx))
    plt.title("Comparison of full gradient optimizers")
    plt.plot(cb_saga.trace_fx - fmin, lw=4, label="SAGA")
    # .. for SVRG we multiply the number of iterations by two to ..
    # .. account for computation of the snapshot gradient ..
    plt.plot(
        2 * np.arange(len(cb_svrg.trace_fx)), cb_svrg.trace_fx - fmin, lw=4, label="SVRG"
    )
    plt.ylabel("Function suboptimality", fontweight="bold")
    plt.xlabel("number of gradient evaluations", fontweight="bold")
    plt.yscale("log")
    plt.ylim(ymin=1e-16)
    plt.xlim((0, 50))
    plt.legend()
    plt.grid()
    plt.show()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  3.468 seconds)

**Estimated memory usage:**  99 MB


.. _sphx_glr_download_auto_examples_plot_saga_vs_svrg.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_saga_vs_svrg.py <plot_saga_vs_svrg.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_saga_vs_svrg.ipynb <plot_saga_vs_svrg.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
