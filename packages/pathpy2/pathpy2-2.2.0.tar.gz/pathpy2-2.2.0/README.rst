Introduction
============

pathpy is an OpenSource python package for the analysis of time
series data on networks using higher- and multi-order network models.

pathpy is specifically tailored to analyse temporal networks as
well as time series and sequence data that capture multiple short, 
independent paths observed in an underlying graph or network. 
Examples for data that can be analysed with pathpy include time-stamped 
social networks, user click streams in information networks, biological 
pathways, citation networks, or information cascades in social networks. 

Unifying the modelling and analysis of path statistics and temporal networks, 
pathpy provides efficient methods to extract causal or time-respecting paths from 
time-stamped network data. The current package distributed via the PyPI name 
pathpy2 supersedes the packages pyTempnets as well as version 1.0 of pathpy.

pathpy facilitates the analysis of temporal correlations in time
series data on networks. It uses model selection and statistical
learning to generate optimal higher- and multi-order models that capture both
topological and temporal characteristics. It can help to answer the important 
question when a network abstraction of complex systems is
justified and when higher-order representations are needed instead.

The theoretical foundation of this package, higher- and multi-order network
models, was developed in the following published works:

1. I Scholtes: When is a network a network? Multi-Order Graphical Model
   Selection in Pathways and Temporal Networks, In KDD'17 - Proceedings 
   of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and 
   Data Mining, Halifax, Nova Scotia, Canada, August 13-17, 2017
   http://dl.acm.org/citation.cfm?id=3098145
2. I Scholtes, N Wider, A Garas: Higher-Order Aggregate Networks in the
   Analysis of Temporal Networks: Path structures and centralities 
   In The European Physical Journal B, 89:61, March 2016   
   http://dx.doi.org/10.1140/epjb/e2016-60663-0
3. I Scholtes, N Wider, R Pfitzner, A Garas, CJ Tessone, F Schweitzer:
   Causality-driven slow-down and speed-up of diffusion in
   non-Markovian temporal networks, In Nature Communications, 5, September 2014
   http://www.nature.com/ncomms/2014/140924/ncomms6024/full/ncomms6024.html 
4. R Pfitzner, I Scholtes, A Garas, CJ Tessone, F Schweitzer:
   Betweenness preference: Quantifying correlations in the topological
   dynamics of temporal networks, Phys Rev Lett, 110(19), 198701, May 2013
   http://journals.aps.org/prl/abstract/10.1103/PhysRevLett.110.198701

pathpy extends higher-order modelling approaches towards multi-order models
for paths that capture temporal correlations at multiple length scales
simultaneously. All mathematical details of the framework can be found in the 
openly available preprint at https://arxiv.org/abs/1702.05499.

A broader view on higher-order models in the analyis of complex systems can be 
found at https://arxiv.org/abs/1806.05977.

pathpy is fully integrated with jupyter, providing rich and interactive in-line
visualisations of networks, temporal networks, higher-, and multi-order models.
Visualisations can be exported to HTML5 files that can be shared and published
onthe Web.


Download and installation
=========================

pathpy is pure python code. It has no platform-specific dependencies
and should thus work on all platforms. pathpy requires python 3.x. 
It builds on numpy and scipy. The latest release version 2.0 of pathpy
can be installed by typing:

pip install pathpy2

Please make sure that you use the pyPI name pathpy2 as the package name pathpy is currently blocked.

Tutorial
========

A comprehensive 3 hour hands-on tutorial that shows how you can use pathpy 
to analyse data on pathways and temporal networks is available online at:

https://ingoscholtes.github.io/kdd2018-tutorial/

An explanatory video that introduces the science behind pathpy is available here:

https://youtu.be/CxJkVrD2ZlM

A promotional video showcasing some of pathpy's features is available here:

https://youtu.be/QIPqFaR2Z5c 


Documentation
=============

The code is fully documented via docstrings which are accessible through
python's built-in help system. Just type help(SYMBOL_NAME) to see
the documentation of a class or method. A reference manual is available
here https://ingoscholtes.github.io/pathpy/hierarchy.html


Releases and Versioning
=======================

The first public beta release of pathpy (released February 17 2017) is
v1.0-beta. Following versions are named MAJOR.MINOR.PATCH according to semantic
versioning. The current version is 2.0.0.

Known Issues
============

- Depending on whether or not scipy has been compiled 
    with or without the numerics package MKL, considerable 
    numerical differences can occur, e.g. for eigenvalue 
    centralities, PageRank, and other measures that depend 
    on the eigenvectors and eigenvalues of matrices. 
    Please refer to scipy.show_config() to show compilation flags.
- Interactive visualisations in jupyter are currently only 
    supported for juypter notebooks, stand-alone HTML files, 
    and the jupyter display integrated in IDEs like Visual 
    Studio Code (which we highly recommend to work with pathpy). 
    Due to its new widget mechanism, interactive d3js 
    visualisations are currently not available for jupyterLab. 
    Due to the complex document object model generated by 
    jupyter notebooks, visualisation performance is best in 
    stand-alone HTML files and in Visual Studio Code.
- The visualisation of temporal networks currently does 
    not support the drawing of edge arrows for directed 
    edges. However, a powerful templating mechanism is 
    available to support custom interactive and dynamic 
    visualizations of temporal networks.
- The visualisation of paths in terms of alluvial diagrams 
    within jupyter is currently unstable for networks with 
    large delay. This is due to the asynchronous loading of 
    external scripts.


Acknowledgements
================

The research behind this data analysis framework was generously funded by the Swiss
State Secretariate for Education, Research and Innovation via Grant C14.0036. 
The development of the predecessor package pyTempNets was further supported by the MTEC
Foundation in the context of the project "The Influence of Interaction Patterns on
Success in Socio-Technical Systems: From Theory to Practice."

The further development of pathpy is currently supported by the 
Swiss National Science Foundation via Grant 176938. See details at:

http://p3.snf.ch/Project-176938


Contributors
============

Ingo Scholtes (project lead, development)
Luca Verginer (development, test suite integration)


Past Contributors
=================
Roman Cattaneo (development)
Nicolas Wider (testing)


Copyright
=========

pathpy is licensed under the GNU Affero General Public
License. See https://choosealicense.com/licenses/agpl-3.0/

(c) ETH Zürich & University of Zurich, 2015 - 2018
