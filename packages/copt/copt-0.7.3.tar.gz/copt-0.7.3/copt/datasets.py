# python3
import hashlib
import os
import numpy as np
from scipy import misc
from scipy import sparse
import urllib
from sklearn import preprocessing

DATA_DIR = os.environ.get(
    "COPT_DATA_DIR", os.path.join(os.path.expanduser("~"), "copt_data")
)


def load_img1(n_rows=20, n_cols=20):
    """Load sample image."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    grid = np.loadtxt(os.path.join(dir_path, "data", "img1.csv"), delimiter=",")
    dim1 = int(np.sqrt(grid.shape[0]))
    grid = grid.reshape((dim1, dim1))
    return misc.imresize(grid, (n_rows, n_cols))


def load_madelon(md5_check=True, subset="full", standardize=True):
    """Download and return the madelon dataset.

    Properties:
        n_samples: 2600
        n_features: 500

    This is the binary classification version of the dataset as found in the
    LIBSVM dataset project:

        https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#madelon


    Args:
        md5_check: bool
            Whether to do an md5 check on the downloaded files.

        subset: string
            Can be one of 'full' for full dataset, 'train' for only the train set
            or 'test' for only the test set.

        standardize: boolean
            If True, each feature will have zero mean and unit variance.


    Returns:
        data: scipy.sparse CSR
            Return data as CSR sparse matrix of shape=(2600, 500).

        target: array of shape 2600
            Labels, only takes values 0 or 1.
    
    Examples:
        * :ref:`sphx_glr_auto_examples_frank_wolfe_plot_sparse_benchmark.py`
        * :ref:`sphx_glr_auto_examples_frank_wolfe_plot_vertex_overlap.py`
    """
    import h5py

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_path = os.path.join(DATA_DIR, "madelon.hdf5")
    if not os.path.exists(file_path):
        print("Madelon dataset is not present in data folder. Downloading it ...")
        url = "https://s3-eu-west-1.amazonaws.com/copt.bianp.net/datasets/madelon.hdf5"
        urllib.request.urlretrieve(url, file_path)
        print("Finished downloading")
    f = h5py.File(file_path, "r")
    data_train = np.asarray(f["X_train"])
    target_train = np.array(f["y_train"])

    if subset == "train":
        data, target = data_train, target_train

    data_test = np.asarray(f["X_test"])
    target_test = np.array(f["y_test"])

    if subset == "test":
        data, target = data_test, target_test
    elif subset == "full":
        data_full = np.vstack((data_train, data_test))
        target_full = np.concatenate((target_train, target_test))
        data, target = data_full, target_full
    else:
        raise ValueError(
            "subset '%s' not implemented, must be one of ('train', 'test', 'full')."
            % subset
        )
    if standardize:
        data = preprocessing.StandardScaler().fit_transform(data)
    return data, target


def load_rcv1(md5_check=True, subset="full"):
    """Download and return the RCV1 dataset.

  This is the binary classification version of the dataset as found in the
  LIBSVM dataset project:

      https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#rcv1.binary

  Args:
    md5_check: bool
      Whether to do an md5 check on the downloaded files.

    subset: string
      Can be one of 'full' for full dataset, 'train' for only the train set
      or 'test' for only the test set.

  Returns:
    X : scipy.sparse CSR matrix

    y: numpy array
      Labels, only takes values 0 or 1.
    """
    import h5py

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_path = os.path.join(DATA_DIR, "rcv1.hdf5")
    if not os.path.exists(file_path):
        print("RCV1 dataset is not present in data folder. Downloading it ...")
        url = "http://s3-eu-west-1.amazonaws.com/copt.bianp.net/datasets/rcv1.hdf5"
        urllib.request.urlretrieve(url, file_path)
        print("Finished downloading")
    f = h5py.File(file_path, "r")
    data_train = np.asarray(f["X_train.data"])
    data_train_indices = np.array(f["X_train.indices"])
    data_train_indptr = np.array(f["X_train.indptr"])
    target_train = np.array(f["y_train"])
    target_train = ((target_train + 1) // 2).astype(np.int)

    data_train = sparse.csr_matrix((data_train, data_train_indices, data_train_indptr))

    if subset == "train":
        return data_train, target_train

    data_test = np.asarray(f["X_test.data"])
    data_test_indices = np.array(f["X_test.indices"])
    data_test_indptr = np.array(f["X_test.indptr"])
    target_test = np.array(f["y_test"])
    target_test = ((target_test + 1) // 2).astype(np.int)

    data_test = sparse.csr_matrix((data_test, data_test_indices, data_test_indptr))

    if subset == "test":
        return data_test, target_test
    elif subset == "full":
        data_full = sparse.vstack((data_train, data_test))
        target_full = np.concatenate((target_train, target_test))
        return data_full, target_full
    else:
        raise ValueError(
            "subset '%s' not implemented, must be one of ('train', 'test', 'full')."
            % subset
        )


def load_url(md5_check=True):
    """Download and return the URL dataset.

  This is the binary classification version of the dataset as found in the
  LIBSVM dataset project:

      https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#url

  Args:
  md5_check: bool
    Whether to do an md5 check on the downloaded files.

  Returns:
    X : scipy.sparse CSR matrix
    y: numpy array
        Labels, only takes values 0 or 1.
  """
    from sklearn import datasets  # lazy import
    import bz2

    file_path = os.path.join(DATA_DIR, "url_combined.bz2")
    data_path = os.path.join(DATA_DIR, "url_combined.data.npy")
    data_indices = os.path.join(DATA_DIR, "url_combined.indices.npy")
    data_indptr = os.path.join(DATA_DIR, "url_combined.indptr.npy")
    data_target = os.path.join(DATA_DIR, "url_combined.target.npy")

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(file_path):
        print("URL dataset is not present in data folder. Downloading it ...")
        url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/url_combined.bz2"
        urllib.request.urlretrieve(url, file_path)
        print("Finished downloading")
        if md5_check:
            h = hashlib.md5(open(file_path, "rb").read()).hexdigest()
            if not h == "83673b8f4224c81968af2fb6022ee487":
                print("MD5 hash do not coincide")
                print("Removing file and re-downloading")
                os.remove(file_path)
                return load_url()
        zipfile = bz2.BZ2File(file_path)
        data = zipfile.read()
        newfilepath = file_path[:-4]
        open(newfilepath, "wb").write(data)
        X, y = datasets.load_svmlight_file(newfilepath)
        np.save(data_path, X.data)
        np.save(data_indices, X.indices)
        np.save(data_indptr, X.indptr)
        np.save(data_target, y)
    X_data = np.load(data_path)
    X_indices = np.load(data_indices)
    X_indptr = np.load(data_indptr)
    X = sparse.csr_matrix((X_data, X_indices, X_indptr))
    y = np.load(data_target)
    y = ((y + 1) // 2).astype(np.int)
    return X, y


def load_covtype():
    """Download and return the covtype dataset.

  This is the binary classification version of the dataset as found in the
  LIBSVM dataset project:

      https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#covtype


  Returns:
    X : scipy.sparse CSR matrix

  y: numpy array
    Labels, only takes values 0 or 1.
  """
    from sklearn import datasets  # lazy import

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_name = os.path.join(DATA_DIR, "covtype.libsvm.binary.scale.bz2")
    if not os.path.exists(file_name):
        print("Covtype dataset is not present in data folder. Downloading it ...")
        url = "https://s3-eu-west-1.amazonaws.com/copt.bianp.net/datasets/covtype.libsvm.binary.scale.bz2"
        urllib.request.urlretrieve(url, file_name)
        print("Finished downloading")
    X, y = datasets.load_svmlight_file(file_name)
    y -= 1  # original labels are [1, 2]
    return X, y


def load_gisette(standardize=True):
    """Download and return the covtype dataset.

    Properties:
        n_samples: 6000 + 1000 (testing)
        n_features: 5000


    This is the binary classification version of the dataset as found in the
    LIBSVM dataset project:

        https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#gisette

    :Args:
        standardize: boolean
        If True, each feature will have zero mean and unit variance.

    Returns:
        data : scipy.sparse CSR matrix
        target: numpy array
            Labels, only takes values 0 or 1.
  """
    from sklearn import datasets  # lazy import

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_name = os.path.join(DATA_DIR, "gisette_scale.bz2")
    if not os.path.exists(file_name):
        print("Gisette dataset is not present in data folder. Downloading it ...")
        url = "https://s3-eu-west-1.amazonaws.com/copt.bianp.net/datasets/gisette_scale.bz2"
        urllib.request.urlretrieve(url, file_name)
        print("Finished downloading")
    X, y = datasets.load_svmlight_file(file_name)
    # original labels are [-1, 1], put into [0, 1]
    X = X.toarray()  # the dataset is not really sparse
    y += 1
    y /= 2
    if standardize:
        X = preprocessing.StandardScaler().fit_transform(X)
    return X, y


def load_kdd10(md5_check=True):
    """Download and return the KDD10 dataset.

  This is the binary classification version of the dataset as found in the
  LIBSVM dataset project:

      https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#kdd2010
      (bridge to algebra)

  Args:
    md5_check: bool
        Whether to do an md5 check on the downloaded files.

  Returns:
    X : scipy.sparse CSR matrix
    y: numpy array
        Labels, only takes values 0 or 1.
  """
    from sklearn import datasets  # lazy import

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_path = os.path.join(DATA_DIR, "kddb.bz2")
    if not os.path.exists(file_path):
        print("KDD10 dataset is not present in data folder. Downloading it ...")
        url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/kddb.bz2"
        urllib.request.urlretrieve(url, file_path)
        print("Finished downloading")
    if md5_check:
        h = hashlib.md5(open(file_path, "rb").read()).hexdigest()
        if not h == "bc5b630fef6989c2f201039fef497e14":
            print("MD5 hash do not coincide")
            print("Removing file and re-downloading")
            os.remove(file_path)
            return load_kdd10()
    return datasets.load_svmlight_file(file_path)


def load_kdd12(md5_check=True, verbose=0):
    """Download and return the KDD12 dataset.

  This is the binary classification version of the dataset as found in the
  LIBSVM dataset project:

      https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#kdd2012

  Args:
    md5_check: bool
      Whether to do an md5 check on the downloaded files.

  Returns:
    X : scipy.sparse CSR matrix
    y: numpy array
        Labels, only takes values 0 or 1.
  """
    from sklearn import datasets  # lazy import
    import bz2

    file_path = os.path.join(DATA_DIR, "kdd12.bz2")
    data_path = os.path.join(DATA_DIR, "kdd12.data.npy")
    data_indices = os.path.join(DATA_DIR, "kdd12.indices.npy")
    data_indptr = os.path.join(DATA_DIR, "kdd12.indptr.npy")
    data_target = os.path.join(DATA_DIR, "kdd12.target.npy")

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(file_path):
        print("KDD12 dataset is not present in data folder. Downloading it ...")
        url = "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/kdd12.bz2"
        urllib.request.urlretrieve(url, file_path)
        print("Finished downloading")
        if md5_check:
            h = hashlib.md5(open(file_path, "rb").read()).hexdigest()
            if not h == "c6fc57735c3cf687dd182d60a7b51cda":
                print("MD5 hash do not coincide")
                print("Removing file and re-downloading")
                os.remove(file_path)
                return load_url()
        zipfile = bz2.BZ2File(file_path)
        data = zipfile.read()
        newfilepath = file_path[:-4]
        open(newfilepath, "wb").write(data)
        X, y = datasets.load_svmlight_file(newfilepath)
        np.save(data_path, X.data)
        np.save(data_indices, X.indices)
        np.save(data_indptr, X.indptr)
        np.save(data_target, y)
    X_data = np.load(data_path)
    X_indices = np.load(data_indices)
    X_indptr = np.load(data_indptr)
    X = sparse.csr_matrix((X_data, X_indices, X_indptr))
    y = np.load(data_target)
    y = ((y + 1) // 2).astype(np.int)
    return X, y


def load_criteo(md5_check=True):
    """Download and return the criteo dataset.

  This is the binary classification version of the dataset as found in the
  LIBSVM dataset project:

      https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#criteo

  Args:
    md5_check: bool
      Whether to do an md5 check on the downloaded files.

  Returns
    X : scipy.sparse CSR matrix
    y: numpy array
        Labels, only takes values 0 or 1.
  """
    from sklearn import datasets  # lazy import

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_path = os.path.join(DATA_DIR, "criteo.kaggle2014.svm.tar.gz")
    data_path = os.path.join(DATA_DIR, "criteo.kaggle2014.data.npz.npy")
    data_indices = os.path.join(DATA_DIR, "criteo.kaggle2014.indices.npy")
    data_indptr = os.path.join(DATA_DIR, "criteo.kaggle2014.indptr.npy")
    data_target = os.path.join(DATA_DIR, "criteo.kaggle2014.target.npy")
    if not os.path.exists(file_path):
        print("criteo dataset is not present in data folder. Downloading it ...")
        url = "https://s3-us-west-2.amazonaws.com/criteo-public-svm-data/criteo.kaggle2014.svm.tar.gz"
        urllib.request.urlretrieve(url, file_path)
        import tarfile

        tar = tarfile.open(file_path)
        tar.extractall(DATA_DIR)
        print("Finished downloading")
        if md5_check:
            h = hashlib.md5(open(file_path, "rb").read()).hexdigest()
            if not h == "d852b491d1b3afa26c1e7b49594ffc3e":
                print("MD5 hash do not coincide")
                print("Removing file and re-downloading")
                os.remove(file_path)
                return load_criteo()
        X, y = datasets.load_svmlight_file(
            os.path.join(DATA_DIR, "criteo.kaggle2014.train.svm")
        )
        np.save(data_path, X.data)
        np.save(data_indices, X.indices)
        np.save(data_indptr, X.indptr)
        np.save(data_target, y)
        # optionally delete files
    else:
        X_data = np.load(data_path)
        X_indices = np.load(data_indices)
        X_indptr = np.load(data_indptr)
        X = sparse.csr_matrix((X_data, X_indices, X_indptr))
        y = np.load(data_target)
    return X, y
