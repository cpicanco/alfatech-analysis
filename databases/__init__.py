"""
# you should use python env to install the following packages to avoid dependency conflicts
py -m pip install mysql-connector-python
py -m pip install SQLAlchemy
"""
from sqlalchemy import create_engine

geic_db = create_engine('mysql+mysqlconnector://root:@localhost/geic', echo=True)

alfatech_students_ids = [
    9739,
    8641,
    9839,
    10090,
    10044,
    9755,
    10378,
    10157,
    10187,
    10032,
    10273,
    9932,
    9875,
    10140,
    10100,
    10088,
    10064,
    10062,
    9869,
    9721,
    9657,
    9708,
    9768,
    9650,
    9811,
    9876,
    9718,
    9658,
    10261,
    10153,
    9844,
    9953,
    10053,
    10286,
    8598,
    10107,
    10075,
    9865,
    9838,
    9651,
    10316,
    9659,
    10085,
    9831,
    10323,
    9652,
    10101,
    8642,
    10284,
    10095,
    10141,
    10004,
    9715,
    9858,
    9955,
    9760,
    9885,
    9880,
    9804,
    10312,
    10087,
    10059,
    10050,
    9898,
    9714,
    10005,
    8224,
    9887,
    10105,
    9850,
    10052,
    8621,
    10188,
    9775,
    9777,
    9822,
    8335,
    9660,
    9687,
    9787,
    9733,
    10021,
    9723,
    8002,
    9951,
    9912,
    10109,
    9834,
    9917,
    10091,
    9877,
    9899,
    9847,
    9719,
    9823,
    10111,
    9756,
    9878,
    10110,
    9781,
    10185,
    9757,
    6083,
    9825,
    10307,
    10260,
    9782,
    9812,
    9671,
    10179,
    9661,
    10321,
    9720,
    10175,
    10006,
    9740,
    10305,
    10154,
    10066,
    9734,
    10265,
    9662,
    10320,
    10114,
    10186,
    9904,
    10192,
    10247,
    10096,
    10097,
    9765,
    9663,
    9653,
    9803,
    9670,
    8593,
    10061,
    9806,
    9677,
    10133,
    9672,
    9704,
    10212,
    9703,
    9692,
    9870,
    10276,
    9818,
    10180,
    8072,
    9928,
    10039,
    10017,
    9788,
    9729,
    10086,
    9702,
    10308,
    10306,
    9792,
    9664,
    9678,
    10158,
    10190,
    10116,
    9813,
    10328,
    9819,
    9727,
    10007,
    9900,
    9783,
    9860,
    9705,
    10098,
    10364,
    9893,
    10220,
    10134,
    10297,
    9730,
    9918,
    10372,
    10379,
    10068,
    10304,
    9913,
    9810,
    9851,
    9905,
    9824,
    10362,
    10067,
    10084,
    9676,
    10024,
    10113,
    9911,
    10008,
    10296,
    10040,
    10079,
    9881,
    9731,
    9814,
    9919,
    9901,
    10238,
    9827,
    10144,
    10069,
    9743,
    9826,
    9646,
    10080,
    9920,
    9695,
    9709,
    9679,
    10294,
    10076,
    9921,
    9710,
    10138,
    10025,
    10092,
    9732,
    9665,
    9954,
    10078,
    10318,
    10031,
    10182,
    9735,
    10159,
    8228,
    9654,
    8227,
    8003,
    10115,
    9835,
    10019,
    10063,
    9849,
    9674,
    9864,
    9935,
    9688,
    9828,
    10035,
    9815,
    9891,
    9922,
    10099,
    10283,
    9784,
    9882,
    9871,
    8644,
    10081,
    9736,
    10191,
    9766,
    10117,
    10139,
    9836,
    9888,
    10311,
    9866,
    9673,
    9728,
    10026,
    9842,
    9821,
    10036,
    9716,
    9785,
    8626,
    8647,
    9690,
    10016,
    9737,
    9696,
    8601,
    10202,
    10155,
    9841,
    10047,
    10065,
    9859,
    10363,
    9830,
    10126,
    10201,
    9845,
    9778,
    9889,
    10361,
    10132,
    9689,
    10125,
    10219,
    9680,
    10009,
    10262,
    10022,
    10124,
    9923,
    10010,
    9798,
    9741,
    10203,
    9779,
    10121,
    9807,
    10208,
    9767,
    10136,
    10322,
    9701,
    9655,
    9691,
    9786,
    10360,
    9833,
    10189,
    9861,
    9698,
    10375,
    10118,
    9780,
    9848,
    9711,
    9883,
    10142,
    9801,
    10143,
    9924,
    10275,
    10027,
    9914,
    9802,
    10020,
    9937,
    10071,
    9681,
    9846,
    10160,
    10377,
    10037,
    10184,
    9666,
    10314,
    10033,
    10028,
    9820,
    9697,
    9726,
    9763,
    10103,
    9797,
    9706,
    9908,
    9707,
    9799,
    9936,
    10082,
    9863,
    10029,
    9738,
    10367,
    9789,
    8629,
    9693,
    9694,
    9862,
    10309,
    10058,
    10055,
    10070,
    9725,
    9647,
    9717,
    9790,
    10373,
    9884,
    10313,
    10374,
    9868,
    10102,
    9909,
    10156,
    10177,
    9667,
    8582,
    9925,
    10011,
    9894,
    10018,
    9890,
    9805,
    10104,
    6082,
    8148,
    9761,
    9759,
    10054,
    9713,
    9840,
    8646,
    9682,
    9751,
    9649,
    10317,
    10285,
    10083,
    9668,
    10122,
    10237,
    9867,
    9699,
    10012,
    9750,
    9879,
    10072,
    10013,
    10038,
    9817,
    10123,
    9758,
    8230,
    7973,
    9886,
    8649,
    9895,
    9906,
    10041,
    10282,
    10274,
    10108,
    9742,
    9683,
    9915,
    10268,
    9753,
    10199,
    10365,
    10056,
    9816,
    10060,
    10263,
    8076,
    10023,
    9684,
    10046,
    10131,
    10259,
    9902,
    9791,
    10120,
    9843,
    9832,
    9669,
    10034,
    9939,
    10030,
    9675,
    9754,
    9916,
    9809,
    10178,
    10014,
    6102,
    10093,
    9926,
    8622,
    9896,
    9648,
    9927,
    10094,
    10042,
    10287,
    10077,
    9907,
    9829,
    9903,
    8623,
    10388,
    9700,
    7798,
    10048,
    9800,
    10057,
    8590,
    9722,
    9837,
    10112,
    9685,
    10051,
    9892,
    10015,
    9762,
]