# Bachelor Thesis Implementation

In this work, a generic interface for the evaluation of medical data is implemented.
It is used in a medical use case. For the evaluation
the health data from the publication of the number of COVID-19 infected
people in the period december of the year 2021 have been used. Each framework receives
this data as input and evaluates it through a DP function. Based on their respective
calculation results, the frameworks are evaluated based on metrics. They include the
categories: privacy compliance, accuracy compliance, and expectation compliance.
If the values of the metrics meet the expectations, the frameworks can be used in the
respective categories. If a framework delivers inaccurate or unexpected
values, this is reflected negatively in its evaluation.
The findings obtained should provide information on the applicability of the frameworks for the privatization of medical data.

The following about implementation:

In the file sourcedata.py the basic data is generated, which is needed for the evaluation. These include neighboring data sets (d1Data.csv & d2Data.csv), the original average of the age values (originMean.csv) and the individual age values (sourcedata.csv).
Through this data, the metrics of each framework can be calculated in snMetrics.py, ibmMetrics.py and Main.java (google). The calculated metrics are stored in snMetrics.csv, ibmMetrics.csv and googleMetric.csv respectively. The data can then be displayed graphically in results.py.

Notice:

To be able to run the Main.java file, the instructions for privacy beam must be followed in the google differential privacy libaries.
