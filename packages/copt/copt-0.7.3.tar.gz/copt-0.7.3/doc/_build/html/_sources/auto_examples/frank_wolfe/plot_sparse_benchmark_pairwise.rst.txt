.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_frank_wolfe_plot_sparse_benchmark_pairwise.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_frank_wolfe_plot_sparse_benchmark_pairwise.py:


Benchmark of Pairwise Frank-Wolfe variants for sparse logistic regression
=========================================================================

Speed of convergence of different Frank-Wolfe variants on various
problems with a logistic regression loss (:meth:`copt.utils.LogLoss`)
and a L1 ball constraint (:meth:`copt.utils.L1Ball`).



.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/frank_wolfe/images/sphx_glr_plot_sparse_benchmark_pairwise_001.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/frank_wolfe/images/sphx_glr_plot_sparse_benchmark_pairwise_002.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/frank_wolfe/images/sphx_glr_plot_sparse_benchmark_pairwise_003.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/frank_wolfe/images/sphx_glr_plot_sparse_benchmark_pairwise_004.png
            :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Running on the Gisette dataset
    /usr/local/google/home/pedregosa/dev/copt/copt/frank_wolfe.py:115: RuntimeWarning: Exhausted line search iterations in minimize_frank_wolfe
      "Exhausted line search iterations in minimize_frank_wolfe", RuntimeWarning
    Sparsity of solution: 0.0666
    Running on the RCV1 dataset
    Sparsity of solution: 0.0042763993564230674
    Running on the Madelon dataset
    /usr/local/google/home/pedregosa/dev/copt/copt/frank_wolfe.py:115: RuntimeWarning: Exhausted line search iterations in minimize_frank_wolfe
      "Exhausted line search iterations in minimize_frank_wolfe", RuntimeWarning
    Sparsity of solution: 0.002
    Running on the Covtype dataset
    Sparsity of solution: 0.037037037037037035





|


.. code-block:: default

    import matplotlib.pyplot as plt
    import numpy as np
    import copt as cp

    # .. datasets and their loading functions ..
    # .. last value si the regularization parameter ..
    # .. which has been chosen to give 10% feature sparsity ..
    datasets = [
        ("Gisette", cp.datasets.load_gisette, 1e4),
        ("RCV1", cp.datasets.load_rcv1, 1e3),
        ("Madelon", cp.datasets.load_madelon, 1e3),
        ("Covtype", cp.datasets.load_covtype, 1e3),
    ]


    variants_fw = [
        ["adaptive", "adaptive step-size", "s"],
        # ["adaptive2+", "linesearch+ step-size", "s"],
        # ["adaptive3", "adaptive3 step-size", "+"],
        # ["adaptive4", "adaptive4 step-size", "x"],
        ["panj", "panj step-size", ">"],
        ["DR", "Lipschitz step-size", "<"],
        ["adaptive_scipy", "scipy linesearch step-size", "^"],
    ]

    for dataset_title, load_data, alpha in datasets:
        plt.figure()
        print("Running on the %s dataset" % dataset_title)

        X, y = load_data()
        n_samples, n_features = X.shape

        l1_ball = cp.utils.L1Ball(alpha)
        f = cp.utils.LogLoss(X, y)
        x0 = np.zeros(n_features)
        x0[0] = alpha
        active_set = np.zeros(n_features * 2)
        active_set[0] = 1

        for step_size, label, marker in variants_fw:

            cb = cp.utils.Trace(f)
            sol = cp.minimize_pairwise_frank_wolfe(
                f.f_grad,
                x0,
                active_set,
                l1_ball.lmo_pairwise,
                callback=cb,
                step_size=step_size,
                lipschitz=f.lipschitz,
                max_iter=1000,
                tol=0,
            )

            plt.plot(cb.trace_time, cb.trace_fx, label=label, marker=marker, markevery=10)

        print("Sparsity of solution: %s" % np.mean(np.abs(sol.x) > 1e-8))
        plt.legend()
        plt.xlabel("Time (in seconds)")
        plt.ylabel("Objective function")
        plt.title(dataset_title)
        plt.tight_layout()  # otherwise the right y-label is slightly clipped
        #    plt.xlim((0, 0.7 * cb.trace_time[-1]))  # for aesthetics
        plt.grid()
        plt.show()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 100 minutes  34.233 seconds)

**Estimated memory usage:**  1595 MB


.. _sphx_glr_download_auto_examples_frank_wolfe_plot_sparse_benchmark_pairwise.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_sparse_benchmark_pairwise.py <plot_sparse_benchmark_pairwise.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_sparse_benchmark_pairwise.ipynb <plot_sparse_benchmark_pairwise.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
