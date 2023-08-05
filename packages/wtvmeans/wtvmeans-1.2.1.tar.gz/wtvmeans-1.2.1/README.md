# Whatever-Means

Whatever-Means (`wtvmeans`) is a generic `python3` library which implements k-means wrappers.
It embeds some common k-means wrappers like G-means, X-means and dip-means, but it is designed to easily make new wrappers.
These algorithms are based on the k-means implementation of [scikit-learn](https://scikit-learn.org/stable/index.html)

## k-means wrapping

k-means is a very powerfull and easy to use clustering algorithm. The main problem is that you need to provide the `k`, the number of clusters. 

To improve k-means, some strategies have been developped upon the algorithm to find the `k`. The underlying idea is to increment `k` step by step until the clustering is "acceptable" (meaning that the clusters should not be splitted).

The main difference between the k-means wrappers is the scoring method which assess whether a cluster is acceptable or it should be splitted.


## Install

The package is hosted on pypi.org so you can get it through pip:

```console
pip3 install wtvmeans
```

## Get started

### Implemented wrappers

The `wtvmeans` package implements the well-known G-means and X-means. You can directly use it on data.

```python
from wtvmeans import GMeans
from sklearn.datasets import load_iris

X = load_iris()['data']
GM = GMeans()
labels = GM.fit_predict(X)
print(GM.n_clusters_)
```

As you can see on this little example, the objects of the library have quite the same behavior as the `sklearn` objects.

### Generic wrapper

The package is mainly based on the definition of a general object called `WTVMeans`. This object is designed to implement custom wrappers according to the scoring method you want.

However if you want to develop a new cluster scoring, you must manually add it to the code which is quite ugly.
In the future, this step will be more convenient.


## Related work

[X-means](http://cs.uef.fi/~zhao/Courses/Clustering2012/Xmeans.pdf) Pelleg, D., & Moore, A. W. (2000, June). X-means: Extending k-means with efficient estimation of the number of clusters. In Icml (Vol. 1, pp. 727-734).

[G-means](http://papers.nips.cc/paper/2526-learning-the-k-in-k-means.pdf) Hamerly, G., & Elkan, C. (2004). Learning the k in k-means. In Advances in neural information processing systems (pp. 281-288).

[Bayesian k-means](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.420.5601&rep=rep1&type=pdf) Welling, M., & Kurihara, K. (2006, April). Bayesian K-means as a “maximization-expectation” algorithm. In Proceedings of the 2006 SIAM international conference on data mining (pp. 474-478). Society for Industrial and Applied Mathematics.

[PG-means](http://papers.nips.cc/paper/3080-pg-means-learning-the-number-of-clusters-in-data.pdf) Feng, Y., & Hamerly, G. (2007). PG-means: learning the number of clusters in data. In Advances in neural information processing systems (pp. 393-400).

[Dip-means](https://papers.nips.cc/paper/4795-dip-means-an-incremental-clustering-method-for-estimating-the-number-of-clusters.pdf) Kalogeratos, A., & Likas, A. (2012). Dip-means: an incremental clustering method for estimating the number of clusters. In Advances in neural information processing systems (pp. 2393-2401).

